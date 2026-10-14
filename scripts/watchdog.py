#!/usr/bin/env python3
"""Surveillant unique de la collecte meteo de Malta Dive Atlas (v1).

POURQUOI (14/10/2026, issue nick0m-0x42/atlas#258, demande de Nicolas) :
le seul surveillant (snapshot-watchdog.yml) ne regardait que l'instantane, avec un
seuil de 9 h alors que son message disait 3 h ; il n'a jamais ouvert d'issue et a
manque un trou de 10,4 h le 12/10. Pendant ce temps la thermocline du 14/10 echouait
sans relance, les temoins echouaient deux fois (authentification Copernicus) et les
crons GitHub se perdaient (instantane 3 passages par jour au lieu de 8 depuis le
06/10, thermocline vers 08-10 h au lieu de 03 h, banc vers 10-13 h au lieu de 05:43).
Rien ne voyait des donnees figees, des valeurs aberrantes, un 200 vide, ni ce que le
site en production lit vraiment.

CE QUE FAIT CE SCRIPT, a chaque passage (cron horaire et fin de chaque collecte) :
1. Lit chaque source PUBLIEE, par l'adresse que lit le site (raw GitHub), jamais la
   copie locale : instantane, thermocline, temoins, banc ; puis le site en
   production (page servie, adresses de donnees qu'il lit, en-tete CORS).
2. Juge le CONTENU, pas le statut : fraicheur selon la periode prevue de la source,
   contenu non vide, valeurs dans des bornes physiques, donnees non figees (empreinte
   des valeurs inchangee au-dela d'un delai ou plusieurs runs de modele auraient du
   la changer), modeles du score pour l'instantane.
3. Trois etats : `ok` ; `retard` (avertissement, relance, pas d'issue) ; `panne`
   (issue ouverte ou commentee dans ce depot, job en echec). Un retard qui dure
   au-dela du seuil de panne devient une panne.
4. Relance d'office, par workflow_dispatch, la collecte d'une source en retard ou en
   panne : jamais si un run de ce workflow est deja en file ou en cours, pas plus
   d'une fois par RELAUNCH_COOLDOWN_MIN minutes, au plus RELAUNCH_MAX_24H fois par
   24 h. C'est ce qui rend la collecte robuste aux crons perdus : le releve n'attend
   plus son cron.
5. Ferme l'issue d'une source quand elle revient a `ok`, avec un commentaire.

Etat entre deux passages (empreintes, relances, problemes deja signales) : un JSON
sur la branche orpheline `watchdog-state`, avec le rapport lisible `rapport.md`
(lisible sans les journaux Actions, regle des sessions). Le script est idempotent :
rejoue sur le meme etat et les memes donnees, il rend les memes decisions et ne
recommente pas un probleme deja signale.

Usage : python scripts/watchdog.py --state etat.json --out-state etat.json
        --report rapport.md [--dry-run]
Variables : GITHUB_TOKEN, GITHUB_REPOSITORY (owner/repo). --dry-run n'ecrit rien sur
GitHub (ni issue ni relance) et imprime les decisions.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
MT = ZoneInfo("Europe/Malta")
RAW = "https://raw.githubusercontent.com/nick0m-0x42/malta-dive-data"
SITE = "https://malta-dive-atlas.netlify.app"
LABEL = "watchdog"
LEGACY_TITLE = "⚠ Weather snapshot en panne"   # titre de snapshot-watchdog.yml, retire le 14/10
RELAUNCH_COOLDOWN_MIN = 100
RELAUNCH_MAX_24H = 6

# Modeles exiges par METHODE.md §2 (atlas v1) pour les deux variables du score.
SCORE_MODELS = {"wind": "gfs_seamless", "waves": "ecmwf_wam025"}

# Periodes et seuils, en heures. POURQUOI des marges : GitHub retarde couramment un
# cron de quelques dizaines de minutes ; un retard au-dela de la marge est un cron
# perdu ou un run en echec. Panne = environ deux periodes manquees.
SOURCES = {
    "instantane": {
        "url": RAW + "/weather-snapshot/data/weather-snapshot.json",
        "workflow": "weather-snapshot.yml", "kind": "periodic",
        "period_h": 3, "late_h": 3.75, "down_h": 7.0, "frozen_h": 24,
    },
    "thermocline": {
        "url": RAW + "/main/data/latest.json",
        "workflow": "thermocline.yml", "kind": "daily",
        "due_utc": (3, 0), "late_after_h": 1.0, "down_after_h": 6.0,
    },
    "temoins": {
        "url": RAW + "/main/data/temoins.json",
        "workflow": "temoins.yml", "kind": "periodic",
        "period_h": 6, "late_h": 6.75, "down_h": 13.0, "frozen_h": 24,
    },
    "banc": {
        "url": RAW + "/main/data/banc/last-run.txt",
        "url_verdict": RAW + "/main/data/banc/verdict.json",
        "workflow": "banc-archive.yml", "kind": "daily",
        "due_utc": (5, 43), "late_after_h": 1.0, "down_after_h": 6.0,
    },
    "site": {"url": SITE + "/", "workflow": None, "kind": "site"},
}

# Bornes physiques (au-dela : valeur aberrante, la source est en panne).
SNAP_BOUNDS = {
    "w": {"wind_speed_10m": (0, 250), "wind_gusts_10m": (0, 350), "wind_direction_10m": (0, 360),
          "temperature_2m": (-15, 50), "apparent_temperature": (-30, 60),
          "relative_humidity_2m": (0, 100), "pressure_msl": (900, 1100),
          "precipitation": (0, 300), "precipitation_probability": (0, 100),
          "weather_code": (0, 99), "cloud_cover": (0, 100), "visibility": (0, 200000)},
    "m": {"wave_height": (0, 20), "wave_direction": (0, 360), "wave_period": (0, 30),
          "wind_wave_height": (0, 20), "wind_wave_direction": (0, 360), "wind_wave_period": (0, 30),
          "swell_wave_height": (0, 20), "swell_wave_direction": (0, 360), "swell_wave_period": (0, 30),
          "sea_surface_temperature": (5, 36)},
}
SNAP_MUST = {"w": ["wind_speed_10m", "wind_direction_10m", "temperature_2m"],
             "m": ["wave_height", "wave_direction"]}
# temoins.json : entiers (houle cm, periode 1/10 s, courant cm/s, vent 1/10 km/h).
TEM_LAYERS = {
    "wave": {"min_pts": 50, "min_fill": 0.8, "bounds": {"h": (0, 2000), "d": (0, 360), "p": (0, 300)}},
    "cur": {"min_pts": 50, "min_fill": 0.8, "bounds": {"s": (0, 500), "d": (0, 360)}},
    "wind_hr": {"min_pts": 100, "min_fill": 0.2, "bounds": {"s": (0, 2500), "d": (0, 360)}},
    "wind_lr": {"min_pts": 10, "min_fill": 0.8, "bounds": {"s": (0, 2500), "d": (0, 360)}},
}
THERMO_T = (10, 33)        # degC en mer autour de Malte, 0 a 110 m
THERMO_Z = (0, 120)        # m


# ---------------------------------------------------------------- utilitaires
def parse_utc(s):
    """'2026-10-14T14:31:44Z' ou '2026-10-14T12:00Z' -> datetime UTC, sinon None."""
    if not isinstance(s, str):
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return dt.datetime.strptime(s, fmt).replace(tzinfo=UTC)
        except ValueError:
            pass
    return None


def fp(obj):
    return hashlib.sha1(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]


def hours(a, b):
    return (a - b).total_seconds() / 3600.0


def bounds_violations(values, lo, hi):
    return sum(1 for v in values if v is not None and not (lo <= v <= hi))


def freshness_periodic(cfg, ts, now):
    """(etat, texte) d'une source a periode fixe, d'apres l'horodatage du produit."""
    if ts is None:
        return "panne", "horodatage illisible"
    age = hours(now, ts)
    if age < -0.5:
        return "panne", f"horodatage dans le futur ({ts:%Y-%m-%d %H:%M} UTC)"
    txt = f"age {age:.1f} h (periode {cfg['period_h']} h, retard au-dela de {cfg['late_h']} h, panne au-dela de {cfg['down_h']} h)"
    if age <= cfg["late_h"]:
        return "ok", txt
    if age <= cfg["down_h"]:
        return "retard", txt
    return "panne", txt


def freshness_daily(cfg, data_date, now):
    """(etat, texte) d'une source quotidienne : le produit du jour est attendu apres
    l'heure prevue du cron (UTC) ; tant que l'heure n'est pas passee, celui de la
    veille suffit."""
    if data_date is None:
        return "panne", "date du produit illisible"
    today = now.date()
    h, m = cfg["due_utc"]
    due = dt.datetime(today.year, today.month, today.day, h, m, tzinfo=UTC)
    late_at = due + dt.timedelta(hours=cfg["late_after_h"])
    down_at = due + dt.timedelta(hours=cfg["down_after_h"])
    txt = f"produit du {data_date}, attendu chaque jour apres {h:02d}:{m:02d} UTC"
    if data_date >= today:
        return "ok", txt
    if data_date == today - dt.timedelta(days=1):
        if now < late_at:
            return "ok", txt + " (celui du jour n'est pas encore du)"
        if now < down_at:
            return "retard", txt + f", celui du jour manque depuis {hours(now, due):.1f} h"
        return "panne", txt + f", celui du jour manque depuis {hours(now, due):.1f} h"
    return "panne", txt + f", {(today - data_date).days} jours de retard"


def worst(*states):
    order = {"ok": 0, "retard": 1, "panne": 2}
    return max(states, key=lambda s: order[s])


# ---------------------------------------------------------------- controles
def check_snapshot(j, now, prev):
    """Controle de l'instantane. Rend dict(state, problems, fp, ts)."""
    cfg = SOURCES["instantane"]
    probs, soft = [], []
    if not isinstance(j, dict):
        return {"state": "panne", "problems": ["reponse non JSON ou vide"], "fp": None, "ts": None}
    ts = parse_utc(j.get("generated_utc"))
    state, ftxt = freshness_periodic(cfg, ts, now)
    if state != "ok":
        (soft if state == "retard" else probs).append(ftxt)
    cells = j.get("cells") or {}
    times = j.get("hourly_time") or []
    if len(cells) < 100:
        probs.append(f"{len(cells)} cellules (100 attendues au moins)")
    if len(times) < 160:
        probs.append(f"{len(times)} heures (160 attendues au moins)")
    elif ts is not None and not str(times[0]).startswith(ts.astimezone(MT).strftime("%Y-%m-%d")):
        probs.append(f"premiere heure {times[0]} hors du jour de generation")
    if j.get("grid") != "node":
        soft.append("grille d'ancien format (centre de maille, pas le noeud de l'atlas)")
    models = j.get("models") or {}
    for var, want in SCORE_MODELS.items():
        if models.get(var) != want:
            soft.append(f"{var} sur {models.get(var) or 'modele non dit'} au lieu de {want}")
    n = len(cells) or 1
    for block, keys in SNAP_MUST.items():
        for k in keys:
            empty = sum(1 for c in cells.values() if not any(v is not None for v in (c.get(block) or {}).get(k) or []))
            if empty / n > 0.10:
                probs.append(f"{k} vide sur {empty}/{len(cells)} cellules")
    for block, b in SNAP_BOUNDS.items():
        for k, (lo, hi) in b.items():
            bad = sum(bounds_violations((c.get(block) or {}).get(k) or [], lo, hi) for c in cells.values())
            if bad:
                probs.append(f"{k} : {bad} valeur(s) hors bornes [{lo}, {hi}]")
    ws = [v for c in cells.values() for v in (c.get("w") or {}).get("wind_speed_10m") or [] if v is not None]
    wh = [v for c in cells.values() for v in (c.get("m") or {}).get("wave_height") or [] if v is not None]
    if ws and len(set(ws)) < 5:
        probs.append("vent constant sur toute la grille et les 7 jours")
    if wh and len(set(wh)) < 5:
        probs.append("houle constante sur toute la grille et les 7 jours")
    vfp = fp({k: (c.get("w", {}).get("wind_speed_10m"), c.get("m", {}).get("wave_height")) for k, c in cells.items()})
    probs += frozen(prev, vfp, ts, now, cfg["frozen_h"])
    st = "panne" if probs else ("retard" if soft else "ok")
    return {"state": st, "problems": probs + soft, "fp": vfp, "ts": ts.isoformat() if ts else None}


def frozen(prev, vfp, ts, now, limit_h):
    """Valeurs identiques depuis plus de limit_h alors que l'horodatage a change."""
    if not prev or not vfp or prev.get("fp") != vfp or not prev.get("fp_since"):
        return []
    since = dt.datetime.fromisoformat(prev["fp_since"])
    if prev.get("ts") != (ts.isoformat() if ts else None) and hours(now, since) > limit_h:
        return [f"donnees figees : memes valeurs depuis {hours(now, since):.0f} h malgre de nouveaux horodatages"]
    return []


def check_thermocline(j, now, prev):
    cfg = SOURCES["thermocline"]
    probs, soft = [], []
    if not isinstance(j, dict):
        return {"state": "panne", "problems": ["reponse non JSON ou vide"], "fp": None, "ts": None, "days": {}}
    try:
        d = dt.date.fromisoformat(j.get("updated", ""))
    except (TypeError, ValueError):
        d = None
    state, ftxt = freshness_daily(cfg, d, now)
    if state != "ok":
        (soft if state == "retard" else probs).append(ftxt)
    hashes = {}
    isl = j.get("islands") or {}
    for k in ("m", "g"):
        x = isl.get(k)
        if not x:
            probs.append(f"ile {k} absente")
            continue
        days = x.get("days") or {}
        if len(days) < 5:
            probs.append(f"ile {k} : {len(days)} jours (5 attendus au moins)")
        if d and days and min(days) != d.isoformat():
            probs.append(f"ile {k} : premier jour {min(days)} au lieu de {d}")
        profs = set()
        for day, v in days.items():
            lv = v.get("levels") or {}
            if "0" not in lv or "20" not in lv:
                probs.append(f"ile {k} {day} : niveaux 0 et 20 m absents")
            temps = list(lv.values()) + [p[1] for p in v.get("profile") or [] if len(p) == 2]
            bad = bounds_violations(temps, *THERMO_T)
            if bad:
                probs.append(f"ile {k} {day} : {bad} temperature(s) hors [{THERMO_T[0]}, {THERMO_T[1]}] degC")
            z = v.get("thermocline_depth")
            if z is None or not (THERMO_Z[0] <= z <= THERMO_Z[1]):
                probs.append(f"ile {k} {day} : profondeur de thermocline {z} hors bornes")
            if len(v.get("profile") or []) < 3:
                probs.append(f"ile {k} {day} : profil de moins de 3 points")
            h = fp(v.get("profile"))
            profs.add(h)
            hashes[f"{k}|{day}"] = h
        if len(days) >= 3 and len(profs) == 1:
            probs.append(f"ile {k} : profil identique tous les jours")
    # Figee : une prevision CMEMS est recalculee chaque jour ; si le produit d'un
    # nouveau jour rend, a la decimale pres, les memes profils que la veille sur tous
    # les jours communs (3 au moins), le flux recopie au lieu de recalculer.
    ref_ts, old = None, {}
    if prev and d:
        if prev.get("ts") and prev["ts"] != d.isoformat():
            ref_ts, old = prev["ts"], prev.get("days") or {}
        elif prev.get("ts_prev"):
            ref_ts, old = prev["ts_prev"], prev.get("days_prev") or {}
    if ref_ts and ref_ts != d.isoformat():   # jamais le produit contre lui-meme (issue #2)
        common = [k for k in hashes if k in old]
        if len(common) >= 6 and all(hashes[k] == old[k] for k in common):
            probs.append(f"donnees figees : {len(common)} profils identiques a ceux du produit du {ref_ts}")
    st = "panne" if probs else ("retard" if soft else "ok")
    return {"state": st, "problems": probs + soft, "fp": fp(hashes), "ts": d.isoformat() if d else None, "days": hashes}


def check_temoins(j, now, prev):
    cfg = SOURCES["temoins"]
    probs, soft = [], []
    if not isinstance(j, dict):
        return {"state": "panne", "problems": ["reponse non JSON ou vide"], "fp": None, "ts": None}
    ts = parse_utc(j.get("gen"))
    state, ftxt = freshness_periodic(cfg, ts, now)
    if state != "ok":
        (soft if state == "retard" else probs).append(ftxt)
    times = j.get("times") or []
    if len(times) < 150:
        probs.append(f"{len(times)} heures (150 attendues au moins)")
    if ts and times and times[0] != ts.astimezone(MT).strftime("%Y-%m-%dT00:00"):
        probs.append(f"fenetre ouverte a {times[0]} au lieu de minuit local du jour de generation")
    layers = j.get("layers") or {}
    for name, spec in TEM_LAYERS.items():
        L = layers.get(name)
        if not L:
            probs.append(f"couche {name} absente")
            continue
        pts = L.get("pts") or []
        if len(pts) < spec["min_pts"]:
            probs.append(f"couche {name} : {len(pts)} points ({spec['min_pts']} attendus au moins)")
        for var, (lo, hi) in spec["bounds"].items():
            series = L.get(var) or []
            vals = [v for s in series for v in (s or [])]
            if series and any(len(s or []) != len(times) for s in series):
                probs.append(f"couche {name}.{var} : series de longueur differente de la fenetre")
            bad = bounds_violations(vals, lo, hi)
            if bad:
                probs.append(f"couche {name}.{var} : {bad} valeur(s) hors [{lo}, {hi}]")
            filled = sum(1 for v in vals if v is not None)
            if vals and filled / len(vals) < spec["min_fill"]:
                probs.append(f"couche {name}.{var} : {100 * filled / len(vals):.0f} % renseigne ({100 * spec['min_fill']:.0f} % attendus)")
            if var in ("h", "s") and filled and len(set(v for v in vals if v is not None)) < 3:
                probs.append(f"couche {name}.{var} : valeur constante")
    vfp = fp({n: (layers.get(n) or {}).get("h") or (layers.get(n) or {}).get("s") for n in TEM_LAYERS})
    probs += frozen(prev, vfp, ts, now, cfg["frozen_h"])
    st = "panne" if probs else ("retard" if soft else "ok")
    return {"state": st, "problems": probs + soft, "fp": vfp, "ts": ts.isoformat() if ts else None}


RUN_LINE = re.compile(r"^(OK|ECHEC)\s+(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})Z")


def check_banc(text, verdict, now, prev):
    cfg = SOURCES["banc"]
    probs, soft = [], []
    first = (text or "").splitlines()[0] if text else ""
    m = RUN_LINE.match(first)
    if not m:
        return {"state": "panne", "problems": [f"last-run.txt illisible : {first[:80]!r}"], "fp": None, "ts": None}
    d = dt.date.fromisoformat(m.group(2))
    state, ftxt = freshness_daily(cfg, d, now)
    if state != "ok":
        (soft if state == "retard" else probs).append(ftxt)
    if m.group(1) == "ECHEC":
        probs.append("dernier run du banc en ECHEC : " + first[:160])
    if not isinstance(verdict, dict) or not verdict.get("date"):
        probs.append("verdict.json absent ou illisible")
    elif verdict["date"] != d.isoformat():
        soft.append(f"verdict.json du {verdict['date']}, archive du {d}")
    st = "panne" if probs else ("retard" if soft else "ok")
    return {"state": st, "problems": probs + soft, "fp": None, "ts": d.isoformat()}


def check_site(status, html, app_js, cors):
    """Ce que le site en production lit : page servie, adresses de donnees presentes
    dans le code servi, en-tete CORS sur chaque flux (sans lui, le navigateur rejette
    la donnee et le visiteur voit le repli)."""
    probs = []
    if status != 200 or not html:
        return {"state": "panne", "problems": [f"page d'accueil HTTP {status}"], "fp": None, "ts": None}
    if app_js is None:
        probs.append("app.js introuvable depuis la page d'accueil")
    else:
        for name in ("instantane", "thermocline", "temoins"):
            if SOURCES[name]["url"] not in app_js:
                probs.append(f"le site ne lit plus {SOURCES[name]['url']} (surveillance a revoir)")
    for name, ok in (cors or {}).items():
        if not ok:
            probs.append(f"{name} : pas d'en-tete Access-Control-Allow-Origin, le navigateur rejettera le flux")
    return {"state": "panne" if probs else "ok", "problems": probs, "fp": None, "ts": None}


# ---------------------------------------------------------------- decisions
def decide(name, res, prev, now, running):
    """Actions pour une source : relance, issue (ouvrir, commenter, fermer).
    prev : etat precedent de la source ; running : run du workflow en file ou en cours."""
    cfg = SOURCES[name]
    acts = {"relaunch": False, "issue": None, "why_no_relaunch": None}
    st = res["state"]
    if st != "ok" and cfg.get("workflow"):
        recent = [dt.datetime.fromisoformat(t) for t in (prev or {}).get("relaunches", [])
                  if hours(now, dt.datetime.fromisoformat(t)) < 24]
        if running:
            acts["why_no_relaunch"] = "un run est deja en file ou en cours"
        elif recent and hours(now, max(recent)) * 60 < RELAUNCH_COOLDOWN_MIN:
            acts["why_no_relaunch"] = f"derniere relance il y a moins de {RELAUNCH_COOLDOWN_MIN} min"
        elif len(recent) >= RELAUNCH_MAX_24H:
            acts["why_no_relaunch"] = f"deja {len(recent)} relances en 24 h"
        else:
            acts["relaunch"] = True
    signature = sig(res["problems"])
    if st == "panne":
        if not (prev or {}).get("issue_open"):
            acts["issue"] = "open"
        elif (prev or {}).get("signalled") != signature:
            acts["issue"] = "comment"
    elif st == "ok" and (prev or {}).get("issue_open"):
        acts["issue"] = "close"
    return acts


def escalate(name, res, prev, now):
    """Un retard (ou un repli de modele) qui dure devient une panne : sans cela un
    defaut leger mais permanent ne serait jamais signale a personne."""
    if res["state"] != "retard":
        return res
    since = dt.datetime.fromisoformat(prev["bad_since"]) if (prev or {}).get("bad_since") else now
    limit = SOURCES[name].get("down_h", 12.0)
    if hours(now, since) > limit:
        res = dict(res, state="panne",
                   problems=res["problems"] + [f"etat degrade depuis {hours(now, since):.0f} h (seuil {limit:.0f} h)"])
    return res


def next_state(name, res, prev, acts, now, issue_number=None):
    prev = prev or {}
    s = {"state": res["state"], "ts": res.get("ts"), "checked": now.isoformat(),
         "problems": res["problems"],
         "bad_since": None if res["state"] == "ok" else (prev.get("bad_since") or now.isoformat())}
    if res.get("fp") is not None:
        s["fp"] = res["fp"]
        s["fp_since"] = prev["fp_since"] if prev.get("fp") == res["fp"] and prev.get("fp_since") else now.isoformat()
    if name == "thermocline":
        # On garde les profils du produit PRECEDENT tant que le jour n'a pas change,
        # pour comparer le produit du lendemain a celui de la veille.
        # Correctif du 14/10 (issue #2, fausse alerte « donnees figees ») : meme jour, la
        # reference de la veille est gardee TELLE QUELLE, meme absente ; avant, un premier
        # passage sans veille rangeait le produit du jour comme sa propre reference.
        if prev.get("ts") == res.get("ts"):
            s["days_prev"], s["ts_prev"] = prev.get("days_prev"), prev.get("ts_prev")
        else:
            s["days_prev"], s["ts_prev"] = prev.get("days"), prev.get("ts")
        s["days"] = res.get("days") or {}
    rel = [t for t in prev.get("relaunches", []) if hours(now, dt.datetime.fromisoformat(t)) < 24]
    if acts["relaunch"]:
        rel.append(now.isoformat())
    s["relaunches"] = rel
    s["issue_open"] = acts["issue"] in ("open", "comment") or (prev.get("issue_open") and acts["issue"] != "close")
    s["issue_number"] = issue_number or (prev.get("issue_number") if s["issue_open"] else None)
    s["signalled"] = sig(res["problems"]) if res["state"] == "panne" else (prev.get("signalled") if s["issue_open"] else None)
    return s


def sig(problems):
    """Signature stable d'une liste de constats : les chiffres (ages, comptes) sont
    neutralises, pour ne commenter l'issue que quand la NATURE du probleme change."""
    return " | ".join(re.sub(r"\d+([.,]\d+)?", "#", p) for p in problems)


# ---------------------------------------------------------------- reseau, GitHub
def http(url, method="GET", data=None, token=None, headers=None, timeout=60):
    h = {"User-Agent": "malta-dive-data-watchdog/1.0", "Cache-Control": "no-cache"}
    if token:
        h.update({"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                  "X-GitHub-Api-Version": "2022-11-28"})
    h.update(headers or {})
    body = json.dumps(data).encode() if data is not None else None
    if body is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read() if e.fp else b""
    except Exception as e:  # noqa: BLE001
        return None, {}, str(e).encode()


def get_json(url):
    st, hd, body = http(url, headers={"Origin": SITE})
    cors = any(k.lower() == "access-control-allow-origin" for k in hd)
    if st != 200:
        return None, cors, f"HTTP {st}"
    try:
        return json.loads(body.decode("utf-8")), cors, None
    except Exception as e:  # noqa: BLE001
        return None, cors, f"JSON illisible ({e})"


class GitHub:
    def __init__(self, repo, token, dry):
        self.api = f"https://api.github.com/repos/{repo}"
        self.token, self.dry, self.log = token, dry, []

    def _call(self, method, path, data=None):
        if self.dry and method != "GET":
            self.log.append(f"[dry-run] {method} {path} {json.dumps(data)[:200] if data else ''}")
            return 200, {}
        st, _, body = http(self.api + path, method, data, self.token)
        try:
            return st, json.loads(body.decode() or "{}")
        except Exception:  # noqa: BLE001
            return st, {}

    def running(self, wf):
        n = 0
        for status in ("queued", "in_progress"):
            st, j = self._call("GET", f"/actions/workflows/{wf}/runs?status={status}&per_page=5")
            if st == 200:
                n += j.get("total_count", 0)
        return n > 0

    def dispatch(self, wf):
        st, _ = self._call("POST", f"/actions/workflows/{wf}/dispatches", {"ref": "main"})
        return st in (200, 204)

    def open_issues(self):
        st, j = self._call("GET", f"/issues?state=open&labels={LABEL}&per_page=100")
        return {i["title"]: i["number"] for i in j} if st == 200 and isinstance(j, list) else {}

    def create_issue(self, title, body):
        st, j = self._call("POST", "/issues", {"title": title, "body": body, "labels": [LABEL]})
        return j.get("number") if isinstance(j, dict) else None

    def comment(self, num, body):
        self._call("POST", f"/issues/{num}/comments", {"body": body})

    def close(self, num, body):
        self.comment(num, body)
        self._call("PATCH", f"/issues/{num}", {"state": "closed", "state_reason": "completed"})


def title_of(name):
    return f"⚠ Watchdog collecte : {name}"


def issue_body(name, res, acts, now):
    cfg = SOURCES[name]
    lines = [f"Surveillant {now:%Y-%m-%d %H:%M} UTC : **{name}** en panne.", ""]
    lines += [f"- {p}" for p in res["problems"]]
    lines += ["", f"Flux surveille : {cfg['url']}"]
    if cfg.get("workflow"):
        if acts["relaunch"]:
            lines.append(f"Relance automatique de `{cfg['workflow']}` demandee.")
        elif acts["why_no_relaunch"]:
            lines.append(f"Pas de relance : {acts['why_no_relaunch']}.")
    lines += ["", "Impact : l'atlas sert un repli ou un tiret, signale par son badge. "
              "Cette issue se ferme seule quand la source revient a la normale.",
              "Rapport complet : branche `watchdog-state`, fichier `rapport.md`."]
    return "\n".join(lines)


def collect(now, state):
    """Lit les sources publiees et rend {source: resultat}."""
    out, cors = {}, {}
    j, cors["instantane"], err = get_json(SOURCES["instantane"]["url"])
    out["instantane"] = check_snapshot(j, now, state.get("instantane")) if j else \
        {"state": "panne", "problems": [f"instantane injoignable ({err})"], "fp": None, "ts": None}
    j, cors["thermocline"], err = get_json(SOURCES["thermocline"]["url"])
    out["thermocline"] = check_thermocline(j, now, state.get("thermocline")) if j else \
        {"state": "panne", "problems": [f"latest.json injoignable ({err})"], "fp": None, "ts": None, "days": {}}
    j, cors["temoins"], err = get_json(SOURCES["temoins"]["url"])
    out["temoins"] = check_temoins(j, now, state.get("temoins")) if j else \
        {"state": "panne", "problems": [f"temoins.json injoignable ({err})"], "fp": None, "ts": None}
    st, _, body = http(SOURCES["banc"]["url"])
    verdict, _, _ = get_json(SOURCES["banc"]["url_verdict"])
    out["banc"] = check_banc(body.decode("utf-8", "replace") if st == 200 else "", verdict, now, state.get("banc")) \
        if st == 200 else {"state": "panne", "problems": [f"last-run.txt HTTP {st}"], "fp": None, "ts": None}
    st, _, body = http(SOURCES["site"]["url"])
    html = body.decode("utf-8", "replace") if st == 200 else ""
    app_js = None
    m = re.search(r'<script[^>]+src="/?(app\.js[^"]*)"', html)
    if m:
        st2, _, b2 = http(SITE + "/" + m.group(1))
        app_js = b2.decode("utf-8", "replace") if st2 == 200 else None
    out["site"] = check_site(st, html, app_js, cors)
    return out


def report(results, decisions, now):
    rows = [f"# Surveillant de la collecte, {now:%Y-%m-%d %H:%M} UTC", "",
            "| Source | Etat | Produit | Relance | Issue | Constats |", "|---|---|---|---|---|---|"]
    for name, res in results.items():
        a = decisions[name]
        rel = "oui" if a["relaunch"] else (a["why_no_relaunch"] or "")
        rows.append(f"| {name} | {res['state']} | {res.get('ts') or ''} | {rel} | {a['issue'] or ''} | "
                    + ("<br>".join(res["problems"]) or "") + " |")
    return "\n".join(rows) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", default="watchdog-state.json")
    ap.add_argument("--out-state", default="watchdog-state.json")
    ap.add_argument("--report", default="rapport.md")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    now = dt.datetime.now(UTC).replace(microsecond=0)
    try:
        state = json.load(open(a.state, encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    gh = GitHub(os.environ.get("GITHUB_REPOSITORY", "nick0m-0x42/malta-dive-data"),
                os.environ.get("GITHUB_TOKEN"), a.dry_run)
    results = collect(now, state)
    issues = gh.open_issues()
    decisions, new_state = {}, {}
    for name, res in results.items():
        prev = dict(state.get(name) or {})
        # L'etat garde n'est pas la verite : une issue fermee a la main ou ouverte
        # par un autre passage se relit sur GitHub.
        num = issues.get(title_of(name))
        prev["issue_open"], prev["issue_number"] = bool(num), num
        res = results[name] = escalate(name, res, prev, now)
        wf = SOURCES[name].get("workflow")
        acts = decide(name, res, prev, now, gh.running(wf) if (wf and res["state"] != "ok") else False)
        if acts["relaunch"] and not gh.dispatch(wf):
            acts["relaunch"], acts["why_no_relaunch"] = False, "workflow_dispatch refuse par l'API"
        if acts["issue"] == "open":
            num = gh.create_issue(title_of(name), issue_body(name, res, acts, now))
        elif acts["issue"] == "comment":
            gh.comment(num, issue_body(name, res, acts, now))
        elif acts["issue"] == "close":
            gh.close(num, f"Retabli le {now:%Y-%m-%d %H:%M} UTC : {name} a nouveau conforme"
                          f" (produit {res.get('ts') or 'present'}).")
            num = None
        decisions[name] = acts
        new_state[name] = next_state(name, res, prev, acts, now, num)
    legacy = issues.get(LEGACY_TITLE)
    if legacy and results["instantane"]["state"] == "ok":
        gh.close(legacy, "Remplace par le surveillant unique (watchdog.yml) le 14/10/2026 ; instantane conforme.")
    text = report(results, decisions, now)
    with open(a.report, "w", encoding="utf-8") as f:
        f.write(text)
    with open(a.out_state, "w", encoding="utf-8") as f:
        json.dump(new_state, f, indent=1, sort_keys=True)
    print(text)
    for line in gh.log:
        print(line)
    down = [n for n, r in results.items() if r["state"] == "panne"]
    if down:
        print("PANNE : " + ", ".join(down))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
