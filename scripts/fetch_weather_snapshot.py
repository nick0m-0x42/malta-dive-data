#!/usr/bin/env python3
"""Snapshot Open-Meteo forecasts (weather + marine) for the Maltese archipelago.

Fallback data source for Malta Dive Atlas when live Open-Meteo is unreachable.
Grid: 0.05 deg cells covering Malta/Gozo/Comino/Filfla with margin.
Cell key convention: origin of the cell, floor(coord/0.05)*0.05, 2 decimals,
format "LAT,LON" (e.g. "35.95,14.30"). The client must use the same key.

Output: data/weather-snapshot.json (compact, shared time axes, values rounded
to 2 decimals). Variable names are identical to the Open-Meteo API so the
client-side adapter is a 1:1 mapping.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

STEP = 0.05
LAT0, LAT1 = 35.75, 36.15   # cell origins 35.75 .. 36.10
LON0, LON1 = 14.10, 14.65   # cell origins 14.10 .. 14.60
CHUNK = 25
RETRIES = 3

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"

WEATHER_HOURLY = [
    "temperature_2m", "apparent_temperature", "relative_humidity_2m", "pressure_msl",
    "precipitation", "precipitation_probability", "weather_code", "cloud_cover",
    "visibility", "wind_speed_10m", "wind_gusts_10m", "wind_direction_10m",
]
WEATHER_DAILY = ["sunrise", "sunset"]
MARINE_HOURLY = [
    "wave_height", "wave_direction", "wave_period",
    "wind_wave_height", "wind_wave_direction", "wind_wave_period",
    "swell_wave_height", "swell_wave_direction", "swell_wave_period",
    "sea_surface_temperature",
]


def grid_origins(a, b):
    n0 = round(a / STEP)
    n1 = round(b / STEP)
    return [round(n * STEP, 2) for n in range(n0, n1)]


def cells():
    out = []
    for la in grid_origins(LAT0, LAT1):
        for lo in grid_origins(LON0, LON1):
            key = f"{la:.2f},{lo:.2f}"
            out.append((key, round(la + STEP / 2, 3), round(lo + STEP / 2, 3)))
    return out


def http_json(url, params):
    qs = urllib.parse.urlencode(params, safe=",")
    req = urllib.request.Request(
        url + "?" + qs,
        headers={"User-Agent": "malta-dive-atlas-snapshot/1.0 (github.com/nick0m-0x42/malta-dive-data)"},
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


def compact(hourly, keys):
    return {k: [rnd(v) for v in hourly.get(k, [])] for k in keys if k in hourly}


def fetch_batch(url, batch, hourly_vars, daily_vars=None):
    params = {
        "latitude": ",".join(str(c[1]) for c in batch),
        "longitude": ",".join(str(c[2]) for c in batch),
        "hourly": ",".join(hourly_vars),
        "forecast_days": 7,
        "timezone": "Europe/Malta",
    }
    if daily_vars:
        params["daily"] = ",".join(daily_vars)
    data = http_json(url, params)
    if isinstance(data, dict):
        data = [data]
    return data


def fetch_marine(batch):
    """Marine model may reject some inland points: fall back per cell."""
    try:
        out = fetch_batch(MARINE_URL, batch, MARINE_HOURLY)
        if len(out) == len(batch):
            return out
    except Exception:  # noqa: BLE001
        pass
    out = []
    for c in batch:
        try:
            out.append(fetch_batch(MARINE_URL, [c], MARINE_HOURLY)[0])
        except Exception:  # noqa: BLE001
            out.append(None)
    return out


def main():
    all_cells = cells()
    result = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "open-meteo.com (snapshot differe via GitHub Actions)",
        "grid_step": STEP,
        "timezone": "Europe/Malta",
        "hourly_time": None,
        "marine_time": None,
        "daily_time": None,
        "cells": {},
    }
    for i in range(0, len(all_cells), CHUNK):
        batch = all_cells[i:i + CHUNK]
        wx = fetch_batch(WEATHER_URL, batch, WEATHER_HOURLY, WEATHER_DAILY)
        if len(wx) != len(batch):
            raise RuntimeError(f"weather batch size mismatch: {len(wx)} != {len(batch)}")
        mr = fetch_marine(batch)
        for j, (key, _la, _lo) in enumerate(batch):
            w = wx[j]
            if result["hourly_time"] is None:
                result["hourly_time"] = w["hourly"]["time"]
                result["daily_time"] = w.get("daily", {}).get("time")
            m = mr[j] if j < len(mr) else None
            if m is not None and result["marine_time"] is None and "hourly" in m:
                result["marine_time"] = m["hourly"]["time"]
            cell = {"w": compact(w["hourly"], WEATHER_HOURLY)}
            if "daily" in w:
                cell["d"] = {k: w["daily"].get(k) for k in WEATHER_DAILY}
            if m is not None and "hourly" in m:
                cell["m"] = compact(m["hourly"], MARINE_HOURLY)
            result["cells"][key] = cell
        time.sleep(1)
    with open("data/weather-snapshot.json", "w", encoding="utf-8") as f:
        json.dump(result, f, separators=(",", ":"), ensure_ascii=False)
    kb = len(json.dumps(result, separators=(",", ":"))) // 1024
    marine_cells = sum(1 for c in result["cells"].values() if "m" in c)
    print(f"OK: {len(result['cells'])} cells ({marine_cells} with marine), ~{kb} kB")


if __name__ == "__main__":
    sys.exit(main() or 0)
