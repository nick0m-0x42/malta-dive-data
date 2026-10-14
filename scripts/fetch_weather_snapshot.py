#!/usr/bin/env python3
"""Instantane Open-Meteo (meteo + mer) de l'archipel maltais.

Repli de Malta Dive Atlas quand Open-Meteo est injoignable depuis le navigateur.

POURQUOI (revu le 2026-10-14, issue nick0m-0x42/atlas#258) :

1. MEMES MODELES QUE LE SCORE. Le Dive Index de l'atlas lit le vent sur
   `gfs_seamless` et la houle sur `ecmwf_wam025` (METHODE.md §2, verdict du banc
   du 14/10 pour le vent). Jusqu'au 14/10 l'instantane demandait le modele par
   defaut : un repli donnait un score calcule sur d'autres modeles que ceux de la
   methode, sans le dire. Desormais :
   - vent (wind_speed_10m, wind_gusts_10m, wind_direction_10m) : gfs_seamless ;
   - houle (wave_*, wind_wave_*, swell_wave_*) : ecmwf_wam025 ;
   - ciel, air, pluie, pression : modele par defaut, comme l'atlas (METHODE §2) ;
   - temperature de mer : requete dediee SANS modele, un modele de vagues la rend
     vide avec un 200 (lecon du 11/09).
   Une requete a modele explicite qui echoue ou rend une colonne vide est rejouee
   sans modele ; le repli est ECRIT dans `models` (« best_match (repli) ») et dans
   `fallbacks`, jamais muet. L'atlas compare `models` a ce qu'exige la methode et
   affiche le repli.

2. MEME POINT QUE L'ATLAS. L'atlas rattache un site au NOEUD de grille
   round(coord*20)/20 et interroge Open-Meteo a ce noeud (app.js, cellKey). Jusqu'au
   14/10 l'instantane interrogeait le CENTRE de la maille (noeud + 0,025 deg), soit
   un decalage d'une demi-maille (2,8 km en latitude, 2,3 km en longitude) entre le
   direct et le repli. La cle reste « LAT,LON » sur deux decimales, mais elle
   designe desormais le noeud lui-meme, et la requete part de ce point. Le champ
   `grid` vaut « node ».

3. CONTROLE DE CONTENU. Un 200 ne prouve rien : le script echoue (code 1, rien
   de publie) si une variable qui fait le score est vide sur plus de 10 % des
   cellules. Le surveillant (scripts/watchdog.py) refait ces controles sur ce qui
   est publie.

Sortie : data/weather-snapshot.json (axes de temps partages, valeurs a deux
decimales). Noms de variables identiques a l'API Open-Meteo.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

STEP = 0.05
LAT0, LAT1 = 35.75, 36.15   # noeuds 35.75 .. 36.10
LON0, LON1 = 14.10, 14.80   # noeuds 14.10 .. 14.75 (epaves est jusqu'a 14.71)
CHUNK = 25
RETRIES = 3

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"

# Modeles exiges par METHODE.md §2 pour les deux variables du score.
WIND_MODEL = "gfs_seamless"
WAVE_MODEL = "ecmwf_wam025"
DEFAULT = "best_match"

WIND_HOURLY = ["wind_speed_10m", "wind_gusts_10m", "wind_direction_10m"]
SKY_HOURLY = [
    "temperature_2m", "apparent_temperature", "relative_humidity_2m", "pressure_msl",
    "precipitation", "precipitation_probability", "weather_code", "cloud_cover",
    "visibility",
]
WEATHER_HOURLY = SKY_HOURLY + WIND_HOURLY
WEATHER_DAILY = ["sunrise", "sunset"]
WAVE_HOURLY = [
    "wave_height", "wave_direction", "wave_period",
    "wind_wave_height", "wind_wave_direction", "wind_wave_period",
    "swell_wave_height", "swell_wave_direction", "swell_wave_period",
]
SST_HOURLY = ["sea_surface_temperature"]
MARINE_HOURLY = WAVE_HOURLY + SST_HOURLY

# Variables dont l'absence rend l'instantane inutile pour le score ou l'affichage.
MUST = {"w": ["wind_speed_10m", "wind_direction_10m", "temperature_2m"],
        "m": ["wave_height", "wave_direction"]}
MAX_EMPTY_SHARE = 0.10


def nodes(a, b):
    """Noeuds n*STEP de a (inclus) a b (exclu), arrondis a 2 decimales."""
    n0 = round(a / STEP)
    n1 = round(b / STEP)
    return [round(n * STEP, 2) for n in range(n0, n1)]


def node_key(lat, lon):
    """Cle d'un point : son noeud round(coord/STEP)*STEP, comme cellKey d'app.js."""
    f = lambda v: f"{round(round(v / STEP) * STEP, 2):.2f}"
    return f"{f(lat)},{f(lon)}"


def cells():
    """[(cle, lat, lon)] : la requete part du noeud lui-meme (point 2 du POURQUOI)."""
    out = []
    for la in nodes(LAT0, LAT1):
        for lo in nodes(LON0, LON1):
            out.append((f"{la:.2f},{lo:.2f}", la, lo))
    return out


def http_json(url, params):
    qs = urllib.parse.urlencode(params, safe=",")
    req = urllib.request.Request(
        url + "?" + qs,
        headers={"User-Agent": "malta-dive-atlas-snapshot/1.1 (github.com/nick0m-0x42/malta-dive-data)"},
    )
    last = None
    for i in range(RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (2 ** i))
    raise last


def rnd(x):
    return round(x, 2) if isinstance(x, float) else x


def has_values(rows, var):
    """Vrai si au moins une ligne porte au moins une valeur non nulle de var."""
    return any(r and isinstance(r.get("hourly", {}).get(var), list)
               and any(v is not None for v in r["hourly"][var]) for r in rows)


def fetch_batch(url, batch, hourly_vars, daily_vars=None, model=None):
    params = {
        "latitude": ",".join(str(c[1]) for c in batch),
        "longitude": ",".join(str(c[2]) for c in batch),
        "hourly": ",".join(hourly_vars),
        "forecast_days": 7,
        "timezone": "Europe/Malta",
    }
    if daily_vars:
        params["daily"] = ",".join(daily_vars)
    if model:
        params["models"] = model
    if url == MARINE_URL:
        # Cellule MER la plus proche : un noeud peut tomber a terre dans le masque
        # du modele de vagues (meme correctif qu'app.js, 07/09/2026).
        params["cell_selection"] = "sea"
    data = http_json(url, params)
    if isinstance(data, dict):
        data = [data]
    if len(data) != len(batch):
        raise RuntimeError(f"{url} : {len(data)} reponses pour {len(batch)} points")
    return data


def fetch_model(url, batch, hourly_vars, model, probe_var, fallbacks, label, daily_vars=None):
    """Modele explicite, puis repli SANS modele s'il echoue ou rend probe_var vide.
    Rend (lignes, modele effectivement servi)."""
    why = None
    try:
        rows = fetch_batch(url, batch, hourly_vars, daily_vars, model)
        if has_values(rows, probe_var):
            return rows, model
        why = f"{probe_var} vide sur {model}"
    except Exception as e:  # noqa: BLE001
        why = f"{model} : {e}"
    fallbacks.append({"var": label, "batch": batch[0][0], "why": why})
    return fetch_batch(url, batch, hourly_vars, daily_vars, None), DEFAULT + " (repli)"


def fetch_marine_one_by_one(batch, hourly_vars, model):
    out = []
    for c in batch:
        try:
            out.append(fetch_batch(MARINE_URL, [c], hourly_vars, None, model)[0])
        except Exception:  # noqa: BLE001
            out.append(None)
    return out


def compact(hourly, keys):
    return {k: [rnd(v) for v in hourly.get(k, [])] for k in keys if k in (hourly or {})}


def content_problems(result):
    """Liste des variables vides sur plus de MAX_EMPTY_SHARE des cellules."""
    probs = []
    n = len(result["cells"]) or 1
    for block, keys in MUST.items():
        for k in keys:
            empty = sum(1 for c in result["cells"].values()
                        if not any(v is not None for v in c.get(block, {}).get(k, [])))
            if empty / n > MAX_EMPTY_SHARE:
                probs.append(f"{k} vide sur {empty}/{n} cellules")
    return probs


def main():
    all_cells = cells()
    fallbacks = []
    served = {"wind": set(), "waves": set()}
    result = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "open-meteo.com (snapshot differe via GitHub Actions)",
        "grid_step": STEP,
        "grid": "node",
        "timezone": "Europe/Malta",
        "models": None,
        "fallbacks": fallbacks,
        "hourly_time": None,
        "marine_time": None,
        "daily_time": None,
        "cells": {},
    }
    for i in range(0, len(all_cells), CHUNK):
        batch = all_cells[i:i + CHUNK]
        sky = fetch_batch(WEATHER_URL, batch, SKY_HOURLY, WEATHER_DAILY)
        wind, wm = fetch_model(WEATHER_URL, batch, WIND_HOURLY, WIND_MODEL, "wind_speed_10m", fallbacks, "wind")
        served["wind"].add(wm)
        try:
            waves, mm = fetch_model(MARINE_URL, batch, WAVE_HOURLY, WAVE_MODEL, "wave_height", fallbacks, "waves")
        except Exception as e:  # noqa: BLE001
            fallbacks.append({"var": "waves", "batch": batch[0][0], "why": f"lot refuse ({e}), point par point"})
            waves, mm = fetch_marine_one_by_one(batch, WAVE_HOURLY, WAVE_MODEL), WAVE_MODEL
        served["waves"].add(mm)
        try:
            sst = fetch_batch(MARINE_URL, batch, SST_HOURLY)
        except Exception:  # noqa: BLE001
            sst = fetch_marine_one_by_one(batch, SST_HOURLY, None)
        for j, (key, _la, _lo) in enumerate(batch):
            k, w, m, s = sky[j], wind[j], waves[j], sst[j]
            if result["hourly_time"] is None:
                result["hourly_time"] = k["hourly"]["time"]
                result["daily_time"] = k.get("daily", {}).get("time")
            cell = {"w": {**compact(k.get("hourly"), SKY_HOURLY), **compact(w.get("hourly"), WIND_HOURLY)}}
            if "daily" in k:
                cell["d"] = {d: k["daily"].get(d) for d in WEATHER_DAILY}
            mh = {}
            if m and "hourly" in m:
                if result["marine_time"] is None:
                    result["marine_time"] = m["hourly"]["time"]
                mh.update(compact(m["hourly"], WAVE_HOURLY))
            if s and "hourly" in s:
                mh.update(compact(s["hourly"], SST_HOURLY))
            if mh:
                cell["m"] = mh
            result["cells"][key] = cell
        time.sleep(1)

    def one(vals, want):
        return want if vals == {want} else " + ".join(sorted(vals))
    result["models"] = {"wind": one(served["wind"], WIND_MODEL),
                        "waves": one(served["waves"], WAVE_MODEL),
                        "sky": DEFAULT, "sst": DEFAULT}
    probs = content_problems(result)
    if probs:
        print("ECHEC contenu, rien n'est publie : " + " ; ".join(probs))
        return 1
    with open("data/weather-snapshot.json", "w", encoding="utf-8") as f:
        json.dump(result, f, separators=(",", ":"), ensure_ascii=False)
    kb = len(json.dumps(result, separators=(",", ":"))) // 1024
    marine_cells = sum(1 for c in result["cells"].values() if "m" in c)
    print(f"OK: {len(result['cells'])} cellules ({marine_cells} avec mer), ~{kb} kB, "
          f"modeles {result['models']}, {len(fallbacks)} repli(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
