"""Tests du surveillant (scripts/watchdog.py) et de la grille de l'instantane.

POURQUOI : le surveillant decide seul d'ouvrir une issue, de relancer une collecte
et de faire echouer un job. Chaque regle est prouvee ici sur un cas sain ET sur le
defaut qu'elle doit attraper (fraicheur, contenu vide, bornes, donnees figees,
modeles, relance bornee, fermeture). Aucun acces reseau.
Lancer : python -m unittest discover -s tests -v
"""
import copy
import datetime as dt
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import watchdog as w  # noqa: E402
import fetch_weather_snapshot as fws  # noqa: E402

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 10, 14, 16, 0, tzinfo=UTC)


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def snapshot(gen=NOW - dt.timedelta(hours=1), ncells=112, models=True, grid="node", wind=None, wave=None):
    times = [f"2026-10-14T{h:02d}:00" for h in range(24)] + \
            [f"2026-10-{15 + d}T{h:02d}:00" for d in range(6) for h in range(24)]
    cells = {}
    for i in range(ncells):
        ws = wind if wind is not None else [5 + (i + h) % 20 for h in range(168)]
        wh = wave if wave is not None else [0.2 + ((i + h) % 15) / 10 for h in range(168)]
        cells[f"c{i}"] = {"w": {"wind_speed_10m": list(ws), "wind_direction_10m": [180] * 168,
                                "temperature_2m": [22.5] * 168},
                          "m": {"wave_height": list(wh), "wave_direction": [300] * 168,
                                "sea_surface_temperature": [25.1] * 168}}
    j = {"generated_utc": iso(gen), "hourly_time": times, "cells": cells, "grid": grid}
    if models:
        j["models"] = {"wind": "gfs_seamless", "waves": "ecmwf_wam025", "sky": "best_match", "sst": "best_match"}
    return j


def thermo(updated="2026-10-14", ndays=7, t0=25.0, shift=0.0):
    d0 = dt.date.fromisoformat(updated)
    days = {}
    for k in range(ndays):
        day = (d0 + dt.timedelta(days=k)).isoformat()
        prof = [[z, round(t0 - z / 10 + k * 0.1 + shift, 2)] for z in (1, 10, 20, 30, 40, 50)]
        days[day] = {"levels": {"0": t0, "20": t0 - 2, "30": t0 - 3, "40": t0 - 4},
                     "thermocline_depth": 35.0, "profile": prof}
    return {"updated": updated, "islands": {"m": {"days": days}, "g": {"days": copy.deepcopy(days)}}}


def temoins(gen="2026-10-14T12:00Z", first="2026-10-14T00:00", n=183):
    def series(npts, f):
        return [[f(i, h) for h in range(n)] for i in range(npts)]
    return {"gen": gen, "times": [first] + [f"t{i}" for i in range(1, n)], "layers": {
        "wave": {"pts": [[0, 0]] * 90, "h": series(90, lambda i, h: 50 + (i + h) % 100),
                 "d": series(90, lambda i, h: 300), "p": series(90, lambda i, h: 60 + h % 10)},
        "cur": {"pts": [[0, 0]] * 90, "s": series(90, lambda i, h: 10 + h % 20), "d": series(90, lambda i, h: h % 360)},
        "wind_hr": {"pts": [[0, 0]] * 419, "s": series(419, lambda i, h: 100 + h % 50 if h < 75 else None),
                    "d": series(419, lambda i, h: 10 if h < 75 else None)},
        "wind_lr": {"pts": [[0, 0]] * 34, "s": series(34, lambda i, h: 200 + h % 30), "d": series(34, lambda i, h: 20)},
    }}


class Instantane(unittest.TestCase):
    def test_sain(self):
        r = w.check_snapshot(snapshot(), NOW, None)
        self.assertEqual(r["state"], "ok", r["problems"])

    def test_fraicheur(self):
        self.assertEqual(w.check_snapshot(snapshot(gen=NOW - dt.timedelta(hours=5)), NOW, None)["state"], "retard")
        r = w.check_snapshot(snapshot(gen=NOW - dt.timedelta(hours=10.4)), NOW, None)
        self.assertEqual(r["state"], "panne")   # le trou de 10,4 h du 12/10, manque par l'ancien seuil de 9 h

    def test_modeles_et_grille(self):
        r = w.check_snapshot(snapshot(models=False, grid=None), NOW, None)
        self.assertEqual(r["state"], "retard")
        self.assertTrue(any("gfs_seamless" in p for p in r["problems"]))
        self.assertTrue(any("grille" in p for p in r["problems"]))

    def test_vide_avec_200(self):
        r = w.check_snapshot(snapshot(wind=[None] * 168), NOW, None)
        self.assertEqual(r["state"], "panne")
        self.assertTrue(any("wind_speed_10m vide" in p for p in r["problems"]))
        self.assertEqual(w.check_snapshot(snapshot(ncells=10), NOW, None)["state"], "panne")
        self.assertEqual(w.check_snapshot(None, NOW, None)["state"], "panne")

    def test_bornes(self):
        r = w.check_snapshot(snapshot(wave=[0.5] * 167 + [42.0]), NOW, None)
        self.assertEqual(r["state"], "panne")
        self.assertTrue(any("hors bornes" in p for p in r["problems"]))

    def test_constant(self):
        r = w.check_snapshot(snapshot(wind=[7.0] * 168), NOW, None)
        self.assertTrue(any("vent constant" in p for p in r["problems"]))

    def test_fige(self):
        a = w.check_snapshot(snapshot(gen=NOW - dt.timedelta(hours=1)), NOW, None)
        prev = {"fp": a["fp"], "fp_since": (NOW - dt.timedelta(hours=30)).isoformat(),
                "ts": (NOW - dt.timedelta(hours=4)).isoformat()}
        r = w.check_snapshot(snapshot(gen=NOW - dt.timedelta(hours=1)), NOW, prev)
        self.assertEqual(r["state"], "panne")
        self.assertTrue(any("figees" in p for p in r["problems"]))
        prev["fp_since"] = (NOW - dt.timedelta(hours=6)).isoformat()   # 6 h : normal (pas de nouveau run GFS)
        self.assertEqual(w.check_snapshot(snapshot(gen=NOW - dt.timedelta(hours=1)), NOW, prev)["state"], "ok")


class Thermocline(unittest.TestCase):
    def test_sain(self):
        self.assertEqual(w.check_thermocline(thermo(), NOW, None)["state"], "ok")

    def test_veille_avant_et_apres_l_heure(self):
        y = thermo("2026-10-13")
        self.assertEqual(w.check_thermocline(y, dt.datetime(2026, 10, 14, 3, 30, tzinfo=UTC), None)["state"], "ok")
        self.assertEqual(w.check_thermocline(y, dt.datetime(2026, 10, 14, 5, 0, tzinfo=UTC), None)["state"], "retard")
        # le cas du 14/10 : run 43 en echec, latest.json du 13/10 a 16:25 UTC
        self.assertEqual(w.check_thermocline(y, dt.datetime(2026, 10, 14, 16, 25, tzinfo=UTC), None)["state"], "panne")
        self.assertEqual(w.check_thermocline(thermo("2026-10-11"), NOW, None)["state"], "panne")

    def test_bornes_et_forme(self):
        r = w.check_thermocline(thermo(t0=45.0), NOW, None)
        self.assertEqual(r["state"], "panne")
        r = w.check_thermocline(thermo(ndays=2), NOW, None)
        self.assertTrue(any("2 jours" in p for p in r["problems"]))
        j = thermo()
        del j["islands"]["g"]
        self.assertTrue(any("ile g absente" in p for p in w.check_thermocline(j, NOW, None)["problems"]))

    def test_fige_d_un_jour_a_l_autre(self):
        hier = w.check_thermocline(thermo("2026-10-13"), dt.datetime(2026, 10, 13, 9, tzinfo=UTC), None)
        prev = {"ts": hier["ts"], "days": hier["days"]}
        # Produit du 14 qui recopie exactement les profils du 13 sur les jours communs.
        copie = thermo("2026-10-13")
        for k in ("m", "g"):
            days = copie["islands"][k]["days"]
            days.pop("2026-10-13")
            days["2026-10-20"] = copy.deepcopy(days["2026-10-19"])
        copie["updated"] = "2026-10-14"
        r = w.check_thermocline(copie, NOW, prev)
        self.assertTrue(any("figees" in p for p in r["problems"]), r["problems"])
        # Produit recalcule (valeurs qui bougent) : pas fige.
        r = w.check_thermocline(thermo("2026-10-14", shift=0.03), NOW, prev)
        self.assertFalse(any("figees" in p for p in r["problems"]), r["problems"])

    def test_premier_passage_sans_veille(self):
        """Issue #2 (14/10, 17:26 UTC) : etat vide, puis trois passages le meme jour.
        Le produit du jour ne doit jamais devenir sa propre reference."""
        acts = {"relaunch": False, "issue": None}
        s = {}
        for k in range(3):
            t = NOW + dt.timedelta(minutes=30 * k)
            r = w.check_thermocline(thermo("2026-10-14"), t, s)
            self.assertEqual(r["state"], "ok", (k, r["problems"]))
            s = w.next_state("thermocline", r, s, acts, t)
        self.assertIsNone(s["ts_prev"])
        # Etat deja corrompu par l'ancien code (reference = produit du jour) : ignore.
        bad = dict(s, ts_prev="2026-10-14", days_prev=s["days"])
        self.assertEqual(w.check_thermocline(thermo("2026-10-14"), NOW, bad)["state"], "ok")

    def test_etat_garde_la_veille(self):
        """Deux passages le meme jour puis un le lendemain : on compare toujours au
        produit PRECEDENT, jamais au produit lui-meme."""
        acts = {"relaunch": False, "issue": None}
        r13 = w.check_thermocline(thermo("2026-10-13"), dt.datetime(2026, 10, 13, 9, tzinfo=UTC), None)
        s = w.next_state("thermocline", r13, {}, acts, dt.datetime(2026, 10, 13, 9, tzinfo=UTC))
        r14 = w.check_thermocline(thermo("2026-10-14", shift=0.03), NOW, s)
        s = w.next_state("thermocline", r14, s, acts, NOW)
        self.assertEqual(s["ts_prev"], "2026-10-13")
        again = w.check_thermocline(thermo("2026-10-14", shift=0.03), NOW + dt.timedelta(hours=1), s)
        self.assertEqual(again["state"], "ok", again["problems"])
        s2 = w.next_state("thermocline", again, s, acts, NOW + dt.timedelta(hours=1))
        self.assertEqual(s2["ts_prev"], "2026-10-13")


class Temoins(unittest.TestCase):
    def test_sain(self):
        r = w.check_temoins(temoins(), NOW, None)
        self.assertEqual(r["state"], "ok", r["problems"])

    def test_fenetre_et_fraicheur(self):
        self.assertEqual(w.check_temoins(temoins(first="2026-10-14T14:00"), NOW, None)["state"], "panne")
        self.assertEqual(w.check_temoins(temoins(gen="2026-10-14T05:00Z", first="2026-10-14T00:00"), NOW, None)["state"], "retard")
        self.assertEqual(w.check_temoins(temoins(gen="2026-10-13T12:00Z", first="2026-10-13T00:00"), NOW, None)["state"], "panne")

    def test_couche_vide(self):
        j = temoins()
        j["layers"]["cur"]["s"] = [[None] * 183 for _ in range(90)]
        r = w.check_temoins(j, NOW, None)
        self.assertEqual(r["state"], "panne")
        j = temoins()
        del j["layers"]["wave"]
        self.assertEqual(w.check_temoins(j, NOW, None)["state"], "panne")

    def test_bornes(self):
        j = temoins()
        j["layers"]["wave"]["h"][0][5] = 99999
        self.assertTrue(any("hors" in p for p in w.check_temoins(j, NOW, None)["problems"]))


class Banc(unittest.TestCase):
    def test_cas(self):
        ok = "OK 2026-10-14T10:36Z · 0 probleme(s)\n"
        self.assertEqual(w.check_banc(ok, {"date": "2026-10-14"}, NOW, None)["state"], "ok")
        self.assertEqual(w.check_banc("ECHEC 2026-10-14T10:36Z · x", {"date": "2026-10-14"}, NOW, None)["state"], "panne")
        hier = "OK 2026-10-13T10:36Z · 0 probleme(s)"
        self.assertEqual(w.check_banc(hier, {"date": "2026-10-13"}, dt.datetime(2026, 10, 14, 7, 0, tzinfo=UTC), None)["state"], "retard")
        self.assertEqual(w.check_banc(hier, {"date": "2026-10-13"}, NOW, None)["state"], "panne")
        self.assertEqual(w.check_banc("", None, NOW, None)["state"], "panne")


class Site(unittest.TestCase):
    def test_site(self):
        js = " ".join(w.SOURCES[n]["url"] for n in ("instantane", "thermocline", "temoins"))
        self.assertEqual(w.check_site(200, "<html>", js, {"instantane": True})["state"], "ok")
        self.assertEqual(w.check_site(503, "", None, {})["state"], "panne")
        r = w.check_site(200, "<html>", js.replace("latest.json", "x.json"), {})
        self.assertTrue(any("ne lit plus" in p for p in r["problems"]))
        self.assertEqual(w.check_site(200, "<html>", js, {"temoins": False})["state"], "panne")


class Decisions(unittest.TestCase):
    R_PANNE = {"state": "panne", "problems": ["age 8.1 h"], "fp": None, "ts": None}
    R_OK = {"state": "ok", "problems": [], "fp": None, "ts": None}

    def test_relance_bornee(self):
        a = w.decide("instantane", self.R_PANNE, {}, NOW, running=False)
        self.assertTrue(a["relaunch"])
        self.assertEqual(a["issue"], "open")
        self.assertFalse(w.decide("instantane", self.R_PANNE, {}, NOW, running=True)["relaunch"])
        recent = {"relaunches": [(NOW - dt.timedelta(minutes=30)).isoformat()]}
        self.assertFalse(w.decide("instantane", self.R_PANNE, recent, NOW, running=False)["relaunch"])
        many = {"relaunches": [(NOW - dt.timedelta(hours=3 * k + 2)).isoformat() for k in range(6)]}
        self.assertFalse(w.decide("instantane", self.R_PANNE, many, NOW, running=False)["relaunch"])
        self.assertFalse(w.decide("site", self.R_PANNE, {}, NOW, running=False)["relaunch"])

    def test_issue_sans_bavardage(self):
        s = w.next_state("instantane", self.R_PANNE, {}, {"relaunch": True, "issue": "open"}, NOW, 7)
        self.assertTrue(s["issue_open"])
        r2 = dict(self.R_PANNE, problems=["age 9.1 h"])           # meme nature, autre chiffre
        self.assertIsNone(w.decide("instantane", r2, s, NOW, running=True)["issue"])
        r3 = dict(self.R_PANNE, problems=["wind_speed_10m vide sur 112/112 cellules"])
        self.assertEqual(w.decide("instantane", r3, s, NOW, running=True)["issue"], "comment")
        self.assertEqual(w.decide("instantane", self.R_OK, s, NOW, running=False)["issue"], "close")
        s2 = w.next_state("instantane", self.R_OK, s, {"relaunch": False, "issue": "close"}, NOW)
        self.assertFalse(s2["issue_open"])

    def test_escalade(self):
        r = {"state": "retard", "problems": ["wind sur modele non dit au lieu de gfs_seamless"], "fp": None, "ts": None}
        self.assertEqual(w.escalate("instantane", r, {}, NOW)["state"], "retard")
        old = {"bad_since": (NOW - dt.timedelta(hours=8)).isoformat()}
        self.assertEqual(w.escalate("instantane", r, old, NOW)["state"], "panne")

    def test_idempotent(self):
        s = w.next_state("instantane", self.R_PANNE, {}, {"relaunch": True, "issue": "open"}, NOW, 7)
        a1 = w.decide("instantane", self.R_PANNE, s, NOW, running=False)
        a2 = w.decide("instantane", self.R_PANNE, s, NOW, running=False)
        self.assertEqual(a1, a2)
        self.assertIsNone(a1["issue"])   # deja signale
        self.assertFalse(a1["relaunch"])  # relance du meme instant : delai de garde


class GrilleInstantane(unittest.TestCase):
    def test_noeuds(self):
        cells = fws.cells()
        self.assertEqual(len(cells), 8 * 14)
        for key, la, lo in cells:
            self.assertEqual(key, f"{la:.2f},{lo:.2f}")   # la requete part du noeud, plus du centre
        keys = {c[0] for c in cells}
        # Les 36 noeuds des sites de l'atlas (round(coord*20)/20) : de 35.80 a 36.10, de 14.20 a 14.70.
        for la in (35.80, 36.10):
            for lo in (14.20, 14.70):
                self.assertIn(f"{la:.2f},{lo:.2f}", keys)
        self.assertIn("36.05,14.25", keys)   # banniere Gozo de l'atlas, 36.05 / 14.24

    def test_controle_de_contenu(self):
        res = {"cells": {"a": {"w": {"wind_speed_10m": [None], "wind_direction_10m": [1], "temperature_2m": [1]},
                               "m": {"wave_height": [1], "wave_direction": [1]}}}}
        self.assertTrue(any("wind_speed_10m" in p for p in fws.content_problems(res)))

    def test_repli_de_modele_ecrit(self):
        calls = []

        def fake(url, batch, hv, dv=None, model=None):
            calls.append(model)
            if model:
                return [{"hourly": {"wind_speed_10m": [None]}}]
            return [{"hourly": {"wind_speed_10m": [3.0]}}]
        orig = fws.fetch_batch
        fws.fetch_batch = fake
        try:
            fb = []
            rows, served = fws.fetch_model(fws.WEATHER_URL, [("k", 1, 2)], ["wind_speed_10m"],
                                           "gfs_seamless", "wind_speed_10m", fb, "wind")
        finally:
            fws.fetch_batch = orig
        self.assertEqual(calls, ["gfs_seamless", None])
        self.assertEqual(served, "best_match (repli)")
        self.assertEqual(fb[0]["var"], "wind")


if __name__ == "__main__":
    unittest.main()
