#!/usr/bin/env python3
"""Profils de temperature CMEMS pour Malta Dive Atlas.
Produit data/latest.json + data/YYYY-MM-DD.json (historique pour graphique).
Points: Malte (35.95N 14.40E) et Gozo (36.05N 14.20E), 0-100 m.
Auth: variables COPERNICUSMARINE_SERVICE_USERNAME / _PASSWORD (secrets GitHub).
"""
import json, datetime, pathlib
import numpy as np
import copernicusmarine as cm

# Dataset journalier de temperature du modele Mediterranee (Analysis & Forecast).
# Si l'ID a change, le lister via: cm.describe(contains=["MEDSEA_ANALYSISFORECAST_PHY"])
DATASET = "cmems_mod_med_phy-tem_anfc_4.2km_P1D-m"
POINTS = {"m": (35.95, 14.40), "g": (36.05, 14.20)}
LEVELS = [0, 20, 30, 40]   # lignes meteo: Surface / 20 m / 30 m / 40 m

def profile(ds, lat, lon):
    p = ds["thetao"].sel(latitude=lat, longitude=lon, method="nearest").isel(time=-1)
    p = p.sel(depth=slice(0, 105)).dropna("depth")
    z = p["depth"].values.astype(float)
    t = p.values.astype(float)
    return z, t

def analyse(z, t):
    levels = {str(l): round(float(np.interp(l, z, t)), 1) for l in LEVELS if l <= z.max()}
    grad = np.abs(np.diff(t) / np.diff(z))
    i = int(np.argmax(grad))
    zmid = float((z[i] + z[i+1]) / 2)
    return {
        "levels": levels,                                  # {"0": 26.4, "20": 24.1, ...}
        "thermocline_depth": round(zmid, 1),               # m, gradient vertical max
        "t_above": round(float(t[max(0, i-1)]), 1),
        "t_below": round(float(t[min(len(t)-1, i+2)]), 1),
        "profile": [[round(float(a), 1), round(float(b), 2)] for a, b in zip(z, t)],  # mini-graphe fiche
    }

def main():
    today = datetime.date.today()
    ds = cm.open_dataset(
        dataset_id=DATASET,
        variables=["thetao"],
        minimum_longitude=14.0, maximum_longitude=14.7,
        minimum_latitude=35.7, maximum_latitude=36.2,
        start_datetime=str(today - datetime.timedelta(days=2)),
        end_datetime=str(today),
        minimum_depth=0, maximum_depth=110,
    )
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
