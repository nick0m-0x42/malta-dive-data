#!/usr/bin/env python3
"""banc_cmems.py : Copernicus dans le banc, et recherche d'un arbitre de houle.

POURQUOI (Nicolas, 17/09 soir) :
  (1) ajouter la houle et le courant Copernicus MEDSEA (1/24 deg, ceux qui font
      la carte a temoins) a l'archive quotidienne du banc, pour qu'ils aient le
      meme recul que GFS, IFS, WAM, Meteo-France et ICON-2I a la mi-octobre ;
  (2) trouver un arbitre de HOULE : aucun jeu de vagues CALYPSO n'est ouvert sur
      l'ERDDAP EuroGOOS (constat du 17/09). On interroge donc le catalogue
      Copernicus plutot que la memoire : altimetrie satellite (hauteur
      significative le long des traces) et bouees in situ de Mediterranee.
Le rapport dit ce qui a ete trouve ET ce qui manque ; rien n'est retenu sur la
foi d'un simple 200, on compte les valeurs non vides et les mailles marines.
Sorties : data/banc/prev-cmems/<date>.json.gz, data/banc/obs/houle-*/<date>.csv.gz
et data/banc/arbitre-houle.txt.
Idempotent : une date deja archivee est reecrite.
"""
import datetime as dt, gzip, json, pathlib, subprocess, sys, time, traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "banc"
TODAY = dt.datetime.utcnow().strftime("%Y-%m-%d")
LOG, PB = [], []
def say(s): print(s, flush=True); LOG.append(str(s))
def pb(s): say("PROBLEME " + str(s)); PB.append(str(s))

POINTS = {  # memes points que banc_archive.py
    "N-Gozo": (36.1200, 14.2500), "N-Comino": (36.0600, 14.3400),
    "N-Qawra": (36.0000, 14.4300), "N-Valletta": (35.9600, 14.5400),
    "E-Delimara": (35.8300, 14.6000), "S-Zurrieq": (35.7900, 14.4400),
    "S-Lapsi": (35.8100, 14.3500), "S-Gozo": (35.9900, 14.2400),
}
BOX = dict(minimum_longitude=14.10, maximum_longitude=14.66,
           minimum_latitude=35.74, maximum_latitude=36.14)

def rapport(nom, lignes):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / nom).write_text("\n".join(lignes) + "\n", encoding="utf-8")

try:
    import copernicusmarine, numpy as np
except Exception as e:
    pb("copernicusmarine indisponible : %r" % (e,))
    rapport("cmems-run.txt", LOG); sys.exit(1)

t0 = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
t1 = t0 + dt.timedelta(days=7)

# --- 1. archive des previsions Copernicus aux points du banc -----------------
JEUX = [("houle", "cmems_mod_med_wav_anfc_4.2km_PT1H-i", ["VHM0", "VMDR", "VTPK"]),
        ("courant", "cmems_mod_med_phy-cur_anfc_4.2km-2D_PT1H-m", ["uo", "vo"])]
arch = {"emis": t0.strftime("%Y-%m-%dT%H:%MZ"), "points": POINTS, "jeux": {}}
for couche, ds_id, vars_ in JEUX:
    try:
        ds = copernicusmarine.open_dataset(dataset_id=ds_id, variables=vars_,
            start_datetime=t0.strftime("%Y-%m-%dT%H:%M:%S"), end_datetime=t1.strftime("%Y-%m-%dT%H:%M:%S"), **BOX)
        temps = [str(x)[:16] for x in ds["time"].values]
        rec, nonvides, total = {}, 0, 0
        for nom, (la, lo) in POINTS.items():
            pt = ds.sel(latitude=la, longitude=lo, method="nearest")
            g = [float(pt["latitude"].values), float(pt["longitude"].values)]
            vals = {}
            for v in vars_:
                a = pt[v]
                if "depth" in a.dims: a = a.isel(depth=0)
                x = [None if np.isnan(float(y)) else round(float(y), 3) for y in a.values]
                vals[v] = x; total += len(x); nonvides += sum(1 for y in x if y is not None)
            rec[nom] = {"grid": g, "hourly": vals}
        arch["jeux"][ds_id] = {"couche": couche, "times": temps, "data": rec}
        say("archive %-45s %d/%d valeurs non vides, %d heures" % (ds_id, nonvides, total, len(temps)))
        if not nonvides: pb("%s : aucune valeur" % ds_id)
    except Exception as e:
        pb("%s : %r" % (ds_id, e))
if arch["jeux"]:
    p = OUT / "prev-cmems" / (TODAY + ".json.gz")
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=9, mtime=0) as f:
        f.write(json.dumps(arch, separators=(",", ":")).encode("utf-8"))
    say("ecrit %s" % p.name)
rapport("cmems-run.txt", [("OK " if not PB else "ECHEC ") + t0.strftime("%Y-%m-%dT%H:%MZ")] + LOG)

# --- 2. arbitre de houle : que propose le catalogue Copernicus ? -------------
AR = ["Recherche d'un arbitre de houle, %s UTC" % t0.strftime("%Y-%m-%d %H:%M"),
      "Contexte : aucun jeu de vagues CALYPSO ouvert sur l'ERDDAP EuroGOOS (17/09)."]
def ar(s): print(s, flush=True); AR.append(str(s))

def describe(motif):
    r = subprocess.run(["copernicusmarine", "describe", "--contains", motif, "--disable-progress-bar"],
                       capture_output=True, text=True, timeout=600)
    try:
        return json.loads(r.stdout)
    except Exception:
        ar("  describe %s : sortie non JSON (%s)" % (motif, (r.stderr or r.stdout)[:200])); return {}

def ids(cat):
    out = []
    def walk(o):
        if isinstance(o, dict):
            if "dataset_id" in o: out.append(o["dataset_id"])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(cat); return sorted(set(out))

for motif, quoi in (("WAVE_GLO_PHY_SWH", "altimetrie satellite, hauteur significative le long des traces"),
                    ("INSITU_MED", "observations in situ de Mediterranee, bouees comprises")):
    js = ids(describe(motif))
    ar("%s (%s) : %d jeux" % (motif, quoi, len(js)))
    for j in js[:12]: ar("  - " + j)
    if not js: ar("  aucun jeu : a chercher hors Copernicus")

# Ces jeux sont tabulaires (sqlite), pas en grille : read_dataframe, pas
# open_dataset (constat du run de 18:00). On archive ce qui tombe sur la zone.
def tableau(ds_id, jours, **extra):
    return copernicusmarine.read_dataframe(
        dataset_id=ds_id,
        start_datetime=(t0 - dt.timedelta(days=jours)).strftime("%Y-%m-%dT%H:%M:%S"),
        end_datetime=t0.strftime("%Y-%m-%dT%H:%M:%S"), **dict(BOX, **extra))

ARB = [("altimetrie", "cmems_obs-wave_glo_phy-swh_nrt_al-l3_PT1S", 2),
       ("bouees", "cmems_obs-ins_med_phybgcwav_mynrt_na_irr", 2)]
for tag, ds_id, jours in ARB:
    try:
        df = tableau(ds_id, jours)
        n = len(df)
        cols = [c for c in df.columns if str(c).upper().startswith(("VHM0", "SWH", "WAVE"))]
        ar("%s %s : %d lignes sur la zone en %d jours, colonnes de houle : %s"
           % (tag, ds_id, n, jours, ", ".join(map(str, cols)) or "aucune"))
        if n and cols:
            d = OUT / "obs" / ("houle-" + tag); d.mkdir(parents=True, exist_ok=True)
            with open(d / (TODAY + ".csv.gz"), "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=9, mtime=0) as f:
                f.write(df.to_csv(index=False).encode("utf-8"))
            ar("  -> archive : obs/houle-%s/%s.csv.gz" % (tag, TODAY))
        else:
            ar("  -> rien a archiver (aucune ligne ou aucune colonne de houle)")
    except Exception as e:
        ar("%s %s : ECHEC %s" % (tag, ds_id, repr(e)[:220]))
rapport("arbitre-houle.txt", AR)
sys.exit(1 if PB else 0)
