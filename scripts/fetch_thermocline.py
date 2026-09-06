#!/usr/bin/env python3
"""Profils de temperature CMEMS pour Malta Dive Atlas.
Produit data/latest.json + data/YYYY-MM-DD.json (historique pour graphique).
Points vises: Malte NE (35.98N 14.55E) et Gozo NW (36.10N 14.20E), en mer;
le script cherche la cellule oceanique valide la plus proche dans un rayon de 0.25 deg.
Auth: variables COPERNICUSMARINE_SERVICE_USERNAME / _PASSWORD (secrets GitHub).
"""
import json, os, sys, datetime, pathlib, traceback
import numpy as np
import copernicusmarine as cm

DATASET = "cmems_mod_med_phy-tem_anfc_4.2km_P1D-m"
POINTS = {"m": (35.98, 14.55), "g": (36.10, 14.20)}
LEVELS = [0, 20, 30, 40]   # lignes meteo: Surface / 20 m / 30 m / 40 m

def check_env():
    missing = [v for v in ("COPERNICUSMARINE_SERVICE_USERNAME", "COPERNICUSMARINE_SERVICE_PASSWORD")
               if not os.environ.get(v)]
    if missing:
        print("FATAL: variables manquantes:", ", ".join(missing))
        sys.exit(2)

def open_ds(today):
    try:
        return cm.open_dataset(
            dataset_id=DATASET,
            variables=["thetao"],
            minimum_longitude=13.8, maximum_longitude=14.9,
            minimum_latitude=35.6, maximum_latitude=36.4,
            start_datetime=str(today - datetime.timedelta(days=2)),
            end_datetime=str(today),
            minimum_depth=1, maximum_depth=110,
        )
    except Exception:
        print("FATAL: echec open_dataset sur", DATASET)
        traceback.print_exc()
        sys.exit(3)

def profile(ds, lat, lon):
    """Colonne d'eau valide la plus proche du point vise (cellules terre = NaN)."""
    da = ds["thetao"].isel(time=-1).sel(depth=slice(0, 105))
    box = da.sel(latitude=slice(lat - 0.25, lat + 0.25),
                 longitude=slice(lon - 0.25, lon + 0.25)).transpose("depth", "latitude", "longitude")
    surf = box.isel(depth=0)
    lats, lons = surf["latitude"].values, surf["longitude"].values
    cand = [(abs(la - lat) + abs(lo - lon), la, lo)
            for i, la in enumerate(lats) for j, lo in enumerate(lons)
            if np.isfinite(surf.values[i, j])]
    if not cand:
        raise RuntimeError(f"aucune cellule mer dans un rayon de 0.25 deg autour de {lat},{lon}")
    _, la, lo = min(cand)
    p = box.sel(latitude=la, longitude=lo).dropna("depth")
    print(f"point vise {lat},{lon} -> cellule mer {float(la):.3f},{float(lo):.3f}, {p.sizes['depth']} niveaux")
    return p["depth"].values.astype(float), p.values.astype(float)

def analyse(z, t):
    levels = {str(l): round(float(np.interp(l, z, t)), 1) for l in LEVELS if l <= z.max()}
    grad = np.abs(np.diff(t) / np.diff(z))
    i = int(np.argmax(grad))
    zmid = float((z[i] + z[i+1]) / 2)
    return {
        "levels": levels,
        "thermocline_depth": round(zmid, 1),
        "t_above": round(float(t[max(0, i-1)]), 1),
        "t_below": round(float(t[min(len(t)-1, i+2)]), 1),
        "profile": [[round(float(a), 1), round(float(b), 2)] for a, b in zip(z, t)],
    }

def main():
    check_env()
    today = datetime.date.today()
    ds = open_ds(today)
    out = {"updated": today.isoformat(), "source": "Copernicus Marine MEDSEA_ANALYSISFORECAST_PHY", "islands": {}}
    for k, (lat, lon) in POINTS.items():
        z, t = profile(ds, lat, lon)
        out["islands"][k] = analyse(z, t)
    d = pathlib.Path("data"); d.mkdir(exist_ok=True)
    (d / "latest.json").write_text(json.dumps(out, separators=(",", ":")))
    (d / f"{today.isoformat()}.json").write_text(json.dumps(out, separators=(",", ":")))
    print("OK", out["islands"]["m"]["thermocline_depth"], "m")

if __name__ == "__main__":
    main()
