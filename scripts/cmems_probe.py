#!/usr/bin/env python3
"""cmems_probe.py : densite et completude des previsions Copernicus Mediterranee.

POURQUOI : 17/09, Nicolas juge la beta des temoins inutilisable : 5 a 18 points
par couche ne donnent pas la situation sur les sites. La source la plus fine
accessible sans frais pour la houle et le courant est Copernicus Marine,
Mediterranee, maille 1/24 deg (~4,6 km), et les identifiants existent deja
(cron thermocline). Cette sonde, en lecture seule :
  1. liste les jeux des produits vagues (006_017) et physique (006_013) ;
  2. choisit les jeux horaires (vagues : VHM0/VMDR/VTM10 ; courants : uo/vo) ;
  3. extrait 7 jours sur la zone Malte-Gozo-Comino et compte, par variable,
     les mailles marines renseignees et la part d'heures non vides.
Un jeu qui s'ouvre sans valeur ne compte pas. Sortie : data/banc/cmems-probe.txt.
"""
import datetime as dt, json, pathlib, subprocess, sys, traceback

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "banc" / "cmems-probe.txt"
L = []
def say(s): print(s, flush=True); L.append(str(s))

BOX = dict(minimum_longitude=14.05, maximum_longitude=14.70, minimum_latitude=35.70, maximum_latitude=36.20)
t0 = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
t1 = t0 + dt.timedelta(days=7)
PRODUITS = {
    "MEDSEA_ANALYSISFORECAST_WAV_006_017": ("vagues", ["VHM0", "VMDR", "VTM10", "VTPK"]),
    "MEDSEA_ANALYSISFORECAST_PHY_006_013": ("courant", ["uo", "vo"]),
}

def datasets(prod):
    r = subprocess.run(["copernicusmarine", "describe", "--product-id", prod, "--show-datasets",
                        "--disable-progress-bar"], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        r = subprocess.run(["copernicusmarine", "describe", "--product-id", prod],
                           capture_output=True, text=True, timeout=300)
    try:
        cat = json.loads(r.stdout)
    except Exception:
        say("describe %s : sortie non JSON (%s)" % (prod, (r.stderr or r.stdout)[:300])); return []
    ids = []
    def walk(o):
        if isinstance(o, dict):
            if "dataset_id" in o: ids.append(o["dataset_id"])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(cat)
    return sorted(set(ids))

try:
    import copernicusmarine, numpy as np
    say("Sonde CMEMS %s UTC, fenetre %s -> %s" % (t0.isoformat(), t0.isoformat(), t1.isoformat()))
    for prod, (tag, want) in PRODUITS.items():
        ids = datasets(prod)
        say("%s : %d jeux : %s" % (prod, len(ids), ", ".join(ids)))
        horaires = [i for i in ids if "PT1H" in i and ("wav" in i or "cur" in i)]
        say("  jeux horaires retenus : %s" % (", ".join(horaires) or "aucun"))
        for ds_id in horaires:
            try:
                ds = copernicusmarine.open_dataset(dataset_id=ds_id, start_datetime=t0.isoformat(),
                                                   end_datetime=t1.isoformat(),
                                                   minimum_depth=0, maximum_depth=2, **BOX)
                vars_ = [v for v in want if v in ds.data_vars]
                say("  %s : variables %s, dims %s" % (ds_id, vars_, dict(ds.sizes)))
                for v in vars_:
                    a = ds[v]
                    if "depth" in a.dims: a = a.isel(depth=0)
                    arr = a.values  # (time, lat, lon)
                    sea = ~np.all(np.isnan(arr), axis=0)
                    nt = arr.shape[0]
                    frac = (np.sum(~np.isnan(arr[:, sea])) / max(1, nt * int(sea.sum())))
                    tmin = str(a.time.values.min())[:16] if nt else "-"
                    tmax = str(a.time.values.max())[:16] if nt else "-"
                    say("    %-6s mailles marines %4d / %d, heures %d (%s .. %s), completude %.0f %%"
                        % (v, int(sea.sum()), sea.size, nt, tmin, tmax, 100 * frac))
                    if int(sea.sum()) == 0:
                        say("    PROBLEME %s : aucune valeur" % v)
                lat = ds["latitude"].values
                if len(lat) > 1: say("    pas de grille %.4f deg" % abs(lat[1] - lat[0]))
            except Exception as e:
                say("  %s : ECHEC %s" % (ds_id, repr(e)[:300]))
except Exception:
    say("ECHEC general : " + traceback.format_exc()[-600:])

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(L) + "\nFin du rapport.\n", encoding="utf-8")
sys.exit(0)
