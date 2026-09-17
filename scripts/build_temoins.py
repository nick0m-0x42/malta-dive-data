#!/usr/bin/env python3
"""build_temoins.py : flux dense des temoins houle / courant / vent pour la carte.

POURQUOI : 17/09, Nicolas juge la beta des temoins inutilisable (5 a 18 points par
couche, modeles a 9-28 km). La sonde CMEMS (data/banc/cmems-probe.txt) donne
153 mailles marines reelles pour la houle et le courant autour de Malte, maille
1/24 deg (~4,6 km), 169 h, completude 100 %. Pour le vent, ICON-2I (ItaliaMeteo,
~2 km) couvre Malte sur ~3 jours ; IFS 9 km prend le relais au-dela (decision
17/09 : densite qui baisse visiblement apres J2). REGLE : uniquement des points
de grille reels, coordonnees de la source, aucune interpolation ; toute valeur
absente reste null. Ce flux sert l'AFFICHAGE ; le Dive Index ne bascule que sur
verdict du banc de fiabilite.

FENETRE (17/09 soir, demande de Nicolas) : le flux commence a MINUIT LOCAL du
jour en cours, plus 168 h a partir de l'heure courante. Motif : il commencait a
l'heure de generation, donc les creneaux deja ecoules du jour (06-10, 10-14)
n'avaient aucune heure et l'atlas affichait un tiret sur la ligne d'aujourd'hui.
Nicolas a tranche « on n'affiche qu'une donnee valide » : plutot que d'inventer
un repli cote atlas, le flux porte les heures ecoulees du jour, qui sont de
l'analyse pour Copernicus et de l'observe-analyse pour Open-Meteo. Cout : au
plus 23 heures de plus, soit environ 14 % de taille en fin de journee.

Sortie : data/temoins.json (raw public, lu par l'atlas), heures locales Malte.
Encodage entier : houle en cm, periode en dixiemes de s, vitesses en cm/s pour
le courant et en dixiemes de km/h pour le vent, directions en degres (houle et
vent : d'ou ca vient ; courant : ou ca va).
Code de sortie 1 si une couche est vide (le workflow commite quand meme le
rapport data/temoins-run.txt).
"""
import datetime as dt, json, math, pathlib, sys, time, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "temoins.json"
REP = ROOT / "data" / "temoins-run.txt"
MT = ZoneInfo("Europe/Malta")
BOX = dict(minimum_longitude=14.10, maximum_longitude=14.66, minimum_latitude=35.74, maximum_latitude=36.14)
LOG, PB = [], []
def say(s): print(s, flush=True); LOG.append(s)
def pb(s): say("PROBLEME " + s); PB.append(s)

t0u = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
t1u = t0u + dt.timedelta(hours=168)
# Debut de fenetre : minuit LOCAL du jour en cours, pour que les creneaux deja
# ecoules de la journee aient leurs heures.
tsu = dt.datetime.now(MT).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(dt.timezone.utc)
def loc(tu): return tu.astimezone(MT).strftime("%Y-%m-%dT%H:00")
N = int((t1u - tsu).total_seconds() // 3600) + 1
TIMES = [loc(tsu + dt.timedelta(hours=i)) for i in range(N)]
IDX = {t: i for i, t in enumerate(TIMES)}
say("fenetre : %s -> %s, %d heures (dont %d deja ecoulees)" % (TIMES[0], TIMES[-1], N, N - 169))

def rnd(x, k):
    if x is None: return None
    try:
        if math.isnan(x): return None
    except TypeError:
        return None
    return int(round(x * k))

out = {"v": 1, "gen": t0u.strftime("%Y-%m-%dT%H:%MZ"), "times": TIMES, "layers": {}}

# ---- 1. Copernicus : houle et courant --------------------------------------
try:
    import copernicusmarine, numpy as np
    def cm(ds_id, variables):
        ds = copernicusmarine.open_dataset(dataset_id=ds_id, variables=variables,
            start_datetime=tsu.strftime("%Y-%m-%dT%H:%M:%S"), end_datetime=t1u.strftime("%Y-%m-%dT%H:%M:%S"), **BOX)
        return ds
    def series(ds, v):
        a = ds[v]
        if "depth" in a.dims: a = a.isel(depth=0)
        return a.transpose("time", "latitude", "longitude").values
    def tindex(ds):
        res = []
        for tv in ds["time"].values:
            tu = dt.datetime.utcfromtimestamp(int(tv.astype("datetime64[s]").astype(int))).replace(tzinfo=dt.timezone.utc)
            res.append(IDX.get(loc(tu)))
        return res

    w = cm("cmems_mod_med_wav_anfc_4.2km_PT1H-i", ["VHM0", "VMDR", "VTPK"])
    H, D, P = series(w, "VHM0"), series(w, "VMDR"), series(w, "VTPK")
    ti = tindex(w); lats = w["latitude"].values; lons = w["longitude"].values
    pts, hh, dd, pp = [], [], [], []
    for j, la in enumerate(lats):
        for i, lo in enumerate(lons):
            col = H[:, j, i]
            if np.all(np.isnan(col)): continue
            pts.append([round(float(la), 4), round(float(lo), 4)])
            rh, rd, rp = [None] * N, [None] * N, [None] * N
            for k, t in enumerate(ti):
                if t is None: continue
                rh[t] = rnd(float(H[k, j, i]), 100); rd[t] = rnd(float(D[k, j, i]), 1); rp[t] = rnd(float(P[k, j, i]), 10)
            hh.append(rh); dd.append(rd); pp.append(rp)
    nn = sum(1 for r in hh for x in r if x is not None)
    say("houle CMEMS : %d points, %d valeurs" % (len(pts), nn))
    if not nn: pb("houle CMEMS vide")
    out["layers"]["wave"] = {"src": "Copernicus Marine MEDSEA 1/24\u00b0", "pts": pts, "h": hh, "d": dd, "p": pp}

    c = cm("cmems_mod_med_phy-cur_anfc_4.2km-2D_PT1H-m", ["uo", "vo"])
    U, V = series(c, "uo"), series(c, "vo")
    ti = tindex(c); lats = c["latitude"].values; lons = c["longitude"].values
    pts, ss, dd = [], [], []
    for j, la in enumerate(lats):
        for i, lo in enumerate(lons):
            if np.all(np.isnan(U[:, j, i])): continue
            pts.append([round(float(la), 4), round(float(lo), 4)])
            rs, rd = [None] * N, [None] * N
            for k, t in enumerate(ti):
                if t is None: continue
                u, v = float(U[k, j, i]), float(V[k, j, i])
                if math.isnan(u) or math.isnan(v): continue
                rs[t] = int(round(100 * math.hypot(u, v)))
                rd[t] = int(round(math.degrees(math.atan2(u, v)) % 360))  # vers ou va le courant
            ss.append(rs); dd.append(rd)
    nn = sum(1 for r in ss for x in r if x is not None)
    heures_cur = sum(1 for i in range(N) if any(r[i] is not None for r in ss))
    say("courant CMEMS : %d points, %d valeurs, %d heures couvertes sur %d" % (len(pts), nn, heures_cur, N))
    if not nn: pb("courant CMEMS vide")
    out["layers"]["cur"] = {"src": "Copernicus Marine MEDSEA 1/24\u00b0", "pts": pts, "s": ss, "d": dd}
except Exception as e:
    pb("Copernicus : %r" % (e,))

# ---- 2. Vent : ICON-2I (~2 km) puis IFS 9 km --------------------------------
def om_grid(step):
    la, lo = [], []
    y = BOX["minimum_latitude"]
    while y <= BOX["maximum_latitude"] + 1e-9:
        x = BOX["minimum_longitude"]
        while x <= BOX["maximum_longitude"] + 1e-9:
            la.append(round(y, 3)); lo.append(round(x, 3)); x += step
        y += step
    return la, lo

def om_wind(model, step):
    la, lo = om_grid(step)
    seen, pts, ss, dd = set(), [], [], []
    for b in range(0, len(la), 80):
        q = urllib.parse.urlencode({"latitude": ",".join(map(str, la[b:b+80])), "longitude": ",".join(map(str, lo[b:b+80])),
            "hourly": "wind_speed_10m,wind_direction_10m", "models": model, "forecast_days": 8,
            "timezone": "Europe/Malta", "wind_speed_unit": "kmh"})
        body = None
        for essai in range(3):
            try:
                with urllib.request.urlopen("https://api.open-meteo.com/v1/forecast?" + q, timeout=90) as r:
                    body = json.loads(r.read()); break
            except Exception as e:
                last = e; time.sleep(5 * (essai + 1))
        if body is None:
            pb("vent %s : lot %d en echec (%r)" % (model, b, last)); continue
        for L in (body if isinstance(body, list) else [body]):
            key = (round(L["latitude"], 3), round(L["longitude"], 3))
            if key in seen: continue
            seen.add(key)
            h = L.get("hourly", {}); tt = h.get("time", [])
            rs, rd = [None] * N, [None] * N
            for k, t in enumerate(tt):
                i = IDX.get(t)
                if i is None: continue
                rs[i] = rnd(h["wind_speed_10m"][k], 10); rd[i] = rnd(h["wind_direction_10m"][k], 1)
            pts.append([round(L["latitude"], 4), round(L["longitude"], 4)]); ss.append(rs); dd.append(rd)
        time.sleep(1)
    nn = sum(1 for r in ss for x in r if x is not None)
    heures = sum(1 for i in range(N) if any(r[i] is not None for r in ss))
    say("vent %s : %d points, %d heures couvertes, %d valeurs" % (model, len(pts), heures, nn))
    return {"pts": pts, "s": ss, "d": dd, "hours": heures, "n": nn}

hr = om_wind("italia_meteo_arpae_icon_2i", 0.02)
lr = om_wind("ecmwf_ifs", 0.04)
if not lr["n"]: pb("vent IFS vide")
if not hr["n"]: say("ALERTE vent ICON-2I vide : IFS seul")
out["layers"]["wind_hr"] = dict(src="ItaliaMeteo ICON-2I (~2 km)", **{k: hr[k] for k in ("pts", "s", "d")})
out["layers"]["wind_lr"] = dict(src="ECMWF IFS (9 km)", **{k: lr[k] for k in ("pts", "s", "d")})

# ---- sortie ------------------------------------------------------------------
if all(k in out["layers"] for k in ("wave", "cur")) or not PB:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    say("ecrit %s : %d octets" % (OUT.name, OUT.stat().st_size))
tete = ("OK " if not PB else "ECHEC ") + t0u.strftime("%Y-%m-%dT%H:%MZ") + " · %d probleme(s)" % len(PB)
REP.write_text(tete + "\n" + "\n".join(LOG) + "\n", encoding="utf-8")
print(tete)
sys.exit(1 if PB else 0)
