#!/usr/bin/env python3
"""banc_verdict.py : le verdict du banc de fiabilite, lu dans l'archive, jamais suppose.

POURQUOI. Depuis le 17/09 le banc archive chaque jour les previsions de huit modeles
(vent GFS/IFS/ICON-EU/ICON-2I, houle WAM/Meteo-France/GFS-Wave, courant
Meteo-France) et de Copernicus MEDSEA (houle, courant), plus les observations
(vent LMML, courant CALYPSO). Ce script les confronte et designe, par variable, le
modele le plus fiable : c'est ce verdict qui decide quel courant entre dans le Dive
Index. Il tourne apres l'archive, chaque jour, et se recalcule entierement : un
verdict n'est jamais grave.

REGLES (Nicolas, 22 et 23/09, notees dans TODO.md de malta-dive-atlas) :
  1. Seuils « ca compte » : on ne juge un modele que sur les heures ou l'OBSERVATION
     depasse vent 25 km/h, houle 0,5 m, courant 0,25 m/s. La houle est aussi notee
     au seuil 0,8 m, publie a cote, sans peser sur le verdict.
  2. Regle d'arret : 28 jours d'archive ET 30 h qualifiantes par variable et par
     echeance (J+1, J+3, J+6). Si les 30 h manquent au 28e jour, on tranche AU PLUS
     TARD au 45e jour avec ce qu'on a, incertitude ecrite. Verdict recalcule chaque
     jour, publie chaque mois dans METHODE.md.
  3. Un modele par variable pour tout l'archipel ; les scores par facade (nord,
     est, sud) sont calcules et publies, sans designer.
  4. Une observation absente rend « aucun arbitre », jamais un score.

METHODE. Echeance = jour de prevision moins jour d'emission (J+1 : le lendemain de
l'emission, toutes ses heures). Pour chaque heure ou l'observation du point depasse
le seuil : erreur = prevision - observation ; on retient l'erreur absolue moyenne
(MAE) et le biais moyen. Le classement va au MAE le plus bas ; a egalite a 5 % pres,
le biais le plus proche de zero. Observations : vent LMML (METAR, noeuds -> km/h,
moyenne horaire) compare aux modeles au point LMML ; courant CALYPSO (radar HF,
grille ~1 km) : la maille la plus proche de chaque point du banc a moins de 6 km,
vitesse = hypot(EWCT, NSCT), comparee aux modeles au meme point. Houle : aucun
arbitre a ce jour (voir arbitre-houle.txt), la section le dit.

ARBITRES DE HOULE (Nicolas, 17/10, « A + C ») :
  A. l'analyse Copernicus MEDSEA (cmems_mod_med_wav_anfc_4.2km_PT1H-i, valeurs des jours
     passes, archivees par banc_cmems.py dans obs/houle-medsea/) aux 8 points du banc.
     Elle assimile l'altimetrie satellite mais ses vents viennent d'ECMWF : independance
     partielle, ecrite dans le rapport. Elle DESIGNE le modele de houle. La prevision
     Copernicus (copernicus_houle) est scoree pour information mais NE PEUT PAS etre
     designee par sa propre analyse (meme systeme).
  C. l'altimetrie satellite le long des traces (obs/houle-altimetrie/), mesure
     independante : chaque observation a moins de 25 km d'un point du banc compte pour
     ce point a l'heure ronde. CONTROLE publie a cote : elle ne designe pas, elle dit si
     elle confirme le verdict de A (« concordance »), ou si elle a trop peu d'heures.

Usage : python scripts/banc_verdict.py [--date AAAA-MM-JJ]
  --date : verdict tel qu'il aurait ete rendu ce jour-la (n'utilise que les
           archives emises et observees jusqu'a cette date).
Sorties : data/banc/verdict.md, data/banc/verdict.json. Idempotent.
"""
import argparse, csv, datetime as dt, gzip, io, json, math, pathlib, re, sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / "data" / "banc"
SEUILS = {"vent": 25.0, "houle": 0.5, "courant": 0.25}
SEUIL_HOULE_ALT = 0.8
ECHEANCES = [1, 3, 6]
MIN_JOURS, MIN_HEURES, JOUR_LIMITE = 28, 30, 45
FACADE = {"N-Gozo": "nord", "N-Comino": "nord", "N-Qawra": "nord", "N-Valletta": "est",
          "E-Delimara": "est", "S-Zurrieq": "sud", "S-Lapsi": "sud", "S-Gozo": "sud", "LMML": "est"}
VAR_MODELE = {"vent": ("wind_speed_10m", 1.0), "houle": ("wave_height", 1.0), "courant": ("ocean_current_velocity", 1 / 3.6)}
# Copernicus : houle VHM0 (m), courant uo/vo (m/s) ; Meteo-France currents : km/h -> m/s.

ap = argparse.ArgumentParser()
ap.add_argument("--date", default=None)
args = ap.parse_args()
AUJ = dt.date.fromisoformat(args.date) if args.date else dt.date.today()

def jours(d):
    out = {}
    if d.exists():
        for f in d.iterdir():
            m = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
            if m and dt.date.fromisoformat(m.group(1)) <= AUJ:
                out[dt.date.fromisoformat(m.group(1))] = f
    return dict(sorted(out.items()))

def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 6371 * math.acos(min(1, math.sin(la1) * math.sin(la2) + math.cos(la1) * math.cos(la2) * math.cos(lo2 - lo1)))

# --- previsions : (variable, modele, point, heure UTC) -> valeur, avec le jour d'emission
prev = defaultdict(dict)   # cle (var, modele) -> {(point, heure): (valeur, jour_emis)}
points = {}
for j, f in jours(B / "prev").items():
    d = json.load(gzip.open(f))
    points.update(d.get("points", {}))
    for mod, v in d["modeles"].items():
        var = v["couche"]
        champ, fac = VAR_MODELE.get(var, (None, 1))
        for pt, rec in v["data"].items():
            h = rec["hourly"]
            if champ not in h: continue
            for t, x in zip(h["time"], h[champ]):
                if x is None: continue
                k = (pt, t[:13])
                # une heure est prevue par plusieurs emissions : on garde, par echeance,
                # l'emission dont l'echeance correspond (traitement plus bas), donc on
                # stocke toutes les emissions.
                prev[(var, mod)].setdefault(k, []).append((float(x) * fac, j))
for j, f in jours(B / "prev-cmems").items():
    d = json.load(gzip.open(f))
    for ds, v in d["jeux"].items():
        var = v["couche"]; mod = "copernicus_" + var
        for pt, rec in v["data"].items():
            h = rec["hourly"]
            for i, t in enumerate(v["times"]):
                if var == "houle":
                    x = h.get("VHM0", [None] * len(v["times"]))[i]
                    val = None if x is None else float(x)
                else:
                    u = h.get("uo", [None])[i] if i < len(h.get("uo", [])) else None
                    w = h.get("vo", [None])[i] if i < len(h.get("vo", [])) else None
                    val = None if u is None or w is None else math.hypot(float(u), float(w))
                if val is None: continue
                prev[(var, mod)].setdefault((pt, t[:13]), []).append((val, j))

# --- observations : (variable, point, heure) -> valeur
obs = {"vent": {}, "houle": {}, "courant": {}}
acc = defaultdict(list)
for j, f in jours(B / "obs" / "lmml").items():
    for row in csv.DictReader(io.TextIOWrapper(gzip.open(f), encoding="utf-8")):
        try: kt = float(row["sknt"])
        except (ValueError, KeyError): continue
        if math.isnan(kt): continue
        acc[("LMML", row["valid"][:13].replace(" ", "T"))].append(kt * 1.852)
for k, xs in acc.items(): obs["vent"][k] = sum(xs) / len(xs)
acc = defaultdict(list); maille = {}
for j, f in jours(B / "obs" / "calypso-courant").items():
    rows = list(csv.reader(io.TextIOWrapper(gzip.open(f), encoding="utf-8")))[2:]
    for r in rows:
        try:
            t, la, lo, u, v = r[0][:13], float(r[2]), float(r[3]), float(r[4]), float(r[5])
        except (ValueError, IndexError): continue
        if math.isnan(u) or math.isnan(v): continue   # CALYPSO ecrit NaN hors couverture
        if not points: break
        for pt, (pla, plo) in points.items():
            if pt == "LMML": continue
            dkm = hav((pla, plo), (la, lo))
            if dkm <= 6:
                if pt not in maille or dkm < maille[pt][0]: maille[pt] = (dkm, (la, lo))
                if maille[pt][1] == (la, lo): acc[(pt, t)].append(math.hypot(u, v))
for k, xs in acc.items(): obs["courant"][k] = sum(xs) / len(xs)

# --- houle, arbitre A : analyse MEDSEA aux points du banc (ARBITRE-HOULE-2026-10-17)
JEU_A = "cmems_mod_med_wav_anfc_4.2km_PT1H-i"
for j, f in jours(B / "obs" / "houle-medsea").items():
    d = json.load(gzip.open(f))
    for pt, xs in d.get("VHM0", {}).items():
        for t, x in zip(d.get("times", []), xs):
            if x is not None: obs["houle"][(pt, t[:13])] = float(x)

# --- houle, controle C : altimetrie a moins de 25 km d'un point, a l'heure ronde
RAYON_ALT_KM = 25
obs_alt = {}
acc = defaultdict(list); cols_alt = set()
for j, f in jours(B / "obs" / "houle-altimetrie").items():
    for row in csv.DictReader(io.TextIOWrapper(gzip.open(f), encoding="utf-8")):
        if "variable" in row and "value" in row:   # format long de read_dataframe
            if (row["variable"] or "").upper() not in ("VAVH", "VHM0", "SWH"): continue
            cle = row["variable"]; brut = row["value"]
        else:
            cle = next((c for c in row if c.upper() in ("VAVH", "VHM0", "SWH")), None)
            if not cle: continue
            brut = row[cle]
        cols_alt.add(cle)
        try:
            x, la, lo = float(brut), float(row.get("latitude", "nan")), float(row.get("longitude", "nan"))
        except (ValueError, TypeError): continue
        if any(math.isnan(v) for v in (x, la, lo)): continue
        t = (row.get("time") or "").replace(" ", "T")[:13]
        if len(t) < 13: continue
        best = min(((hav((pla, plo), (la, lo)), pt) for pt, (pla, plo) in points.items() if pt != "LMML"), default=None)
        if best and best[0] <= RAYON_ALT_KM: acc[(best[1], t)].append(x)
for k, xs in acc.items(): obs_alt[k] = sum(xs) / len(xs)

# --- scores
jours_prev = jours(B / "prev")
debut = min(jours_prev) if jours_prev else None
n_jours = (AUJ - debut).days + 1 if debut else 0

def scores(var, seuil, O=None):
    """{modele: {echeance: {facade|'archipel': [n, mae, biais]}}} ; O : observations (defaut obs[var])"""
    O = obs[var] if O is None else O
    out = {}
    for (v, mod), table in prev.items():
        if v != var: continue
        res = {}
        for ech in ECHEANCES:
            agg = defaultdict(lambda: [0, 0.0, 0.0])
            for (pt, h), emissions in table.items():
                o = O.get((pt, h))
                if o is None or o <= seuil: continue
                hj = dt.date.fromisoformat(h[:10])
                for x, j in emissions:
                    if (hj - j).days != ech: continue
                    for cle in ("archipel", FACADE.get(pt, "?")):
                        a = agg[cle]; a[0] += 1; a[1] += abs(x - o); a[2] += (x - o)
            res[ech] = {cle: [n, s / n, b / n] for cle, (n, s, b) in agg.items() if n}
        out[mod] = res
    return out

def designe(sc):
    """Un modele pour l'archipel, si chaque echeance a >= MIN_HEURES ; sinon None + manque."""
    cand = {}
    manque = {}
    for mod, res in sc.items():
        ns = [res.get(e, {}).get("archipel", [0])[0] for e in ECHEANCES]
        manque[mod] = ns
        if all(n >= MIN_HEURES for n in ns):
            cand[mod] = sum(res[e]["archipel"][1] for e in ECHEANCES) / len(ECHEANCES), \
                        sum(abs(res[e]["archipel"][2]) for e in ECHEANCES) / len(ECHEANCES)
    if not cand: return None, manque
    best = min(cand.items(), key=lambda kv: kv[1][0])
    proches = [m for m, (mae, b) in cand.items() if mae <= best[1][0] * 1.05]
    if len(proches) > 1:
        best = min(((m, cand[m]) for m in proches), key=lambda kv: kv[1][1])
    return best[0], manque

L = ["# Verdict du banc de fiabilite", "",
     "Genere le %s par scripts/banc_verdict.py%s. Chiffres lus dans data/banc/, jamais supposes." % (AUJ.isoformat(), " (--date)" if args.date else ""), ""]
J = {"date": AUJ.isoformat(), "debut": debut.isoformat() if debut else None, "jours": n_jours, "variables": {}}
if not debut:
    L += ["**Aucune prevision archivee.**"]
else:
    j28 = debut + dt.timedelta(days=MIN_JOURS - 1); j45 = debut + dt.timedelta(days=JOUR_LIMITE - 1)
    L += ["Archive depuis le **%s** : **%d** jour(s) d'emissions. 28 jours le **%s**, borne des 45 jours le **%s**." % (debut, n_jours, j28, j45),
          "Seuils « ca compte » : vent > %g km/h, houle > %g m (et %g m publie a cote), courant > %g m/s." % (SEUILS["vent"], SEUILS["houle"], SEUIL_HOULE_ALT, SEUILS["courant"]),
          "Echeances : J+%s. Il faut %d h qualifiantes par echeance." % (", J+".join(map(str, ECHEANCES)), MIN_HEURES), ""]
    for var in ("vent", "houle", "courant"):
        L += ["## %s" % var.capitalize()]
        if not obs[var]:
            L += ["**Aucun arbitre** : aucune observation de %s dans l'archive. Aucun score n'est calcule, aucun modele n'est designe." % var,
                  "Voir data/banc/arbitre-houle.txt (analyse MEDSEA et altimetrie : archive pas encore remplie)." if var == "houle" else "", ""]
            J["variables"][var] = {"arbitre": False}
            continue
        sc = scores(var, SEUILS[var])
        # La prevision Copernicus ne peut pas etre designee par sa propre analyse (meme systeme).
        best, manque = designe({m: r for m, r in sc.items() if not (var == "houle" and m == "copernicus_houle")})
        nq = len([1 for o in obs[var].values() if o > SEUILS[var]])
        L += ["Arbitre : %s, %d heures observees dont **%d** au-dessus du seuil." % (
              "LMML (METAR)" if var == "vent" else
              ("analyse Copernicus MEDSEA %s, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable)" % JEU_A) if var == "houle" else
              "CALYPSO radar HF, mailles a %s" % ", ".join("%s %.1f km" % (p, d) for p, (d, _) in sorted(maille.items())),
              len(obs[var]), nq)]
        if n_jours >= MIN_JOURS and best:
            L += ["**Verdict : %s** (28 jours et 30 h atteints)." % best]
        elif n_jours >= JOUR_LIMITE:
            # borne des 45 jours : on designe sur ce qu'on a, incertitude ecrite
            cand = {m: r for m, r in sc.items() if any(r.get(e, {}).get("archipel") for e in ECHEANCES)}
            if cand:
                b2 = min(cand, key=lambda m: sum(r["archipel"][1] for r in cand[m].values() if "archipel" in r) / max(1, len(cand[m])))
                L += ["**Verdict force a la borne des 45 jours : %s**, avec MOINS de 30 h qualifiantes sur au moins une echeance : incertitude elevee, a recalculer chaque mois." % b2]
                best = b2
            else:
                L += ["Borne des 45 jours atteinte sans aucune heure qualifiante : **aucun verdict possible**."]
        else:
            L += ["**En attente** : %s." % ("28 jours non atteints (%d/%d)" % (n_jours, MIN_JOURS) if n_jours < MIN_JOURS
                   else "moins de %d h qualifiantes sur au moins une echeance, borne le %s" % (MIN_HEURES, j45))]
        L += ["", "| modele | echeance | heures | MAE | biais | nord | est | sud |", "|---|---|---|---|---|---|---|---|"]
        unite = {"vent": "km/h", "houle": "m", "courant": "m/s"}[var]
        for mod, res in sorted(sc.items()):
            for e in ECHEANCES:
                a = res.get(e, {}).get("archipel")
                fac = lambda f: ("%.2f" % res[e][f][1]) if e in res and f in res[e] else "—"
                L.append("| %s | J+%d | %s | %s | %s | %s | %s | %s |" % (
                    mod, e, a[0] if a else 0, ("%.2f %s" % (a[1], unite)) if a else "—", ("%+.2f" % a[2]) if a else "—",
                    fac("nord"), fac("est"), fac("sud")))
        L.append("")
        J["variables"][var] = {"arbitre": True, "heures_qualifiantes": nq, "verdict": best,
                               "scores": {m: {str(e): r.get(e, {}) for e in ECHEANCES} for m, r in sc.items()}}
        if var == "houle":
            sc2 = scores(var, SEUIL_HOULE_ALT); b2, _ = designe({m: r for m, r in sc2.items() if m != "copernicus_houle"})
            L += ["Au seuil %g m (publie, ne pese pas) : %s." % (SEUIL_HOULE_ALT, ("meilleur %s" % b2) if b2 else "pas assez d'heures"), ""]
            J["variables"][var]["seuil_alt"] = {"seuil": SEUIL_HOULE_ALT, "verdict": b2}
            # Controle C : altimetrie, mesure independante, ne designe pas.
            nqa = len([1 for o in obs_alt.values() if o > SEUILS[var]])
            # meme ensemble designable que le verdict, pour que la concordance compare des choses comparables
            sca = scores(var, SEUILS[var], obs_alt); bc, _ = designe({m: r for m, r in sca.items() if m != "copernicus_houle"})
            if not obs_alt:
                conc = "aucune observation d'altimetrie a moins de %d km des points" % RAYON_ALT_KM
            elif not bc:
                conc = "trop peu d'heures pour juger (%d h au-dessus du seuil, %d h exigees par echeance)" % (nqa, MIN_HEURES)
            else:
                conc = "meilleur %s ; concordance avec le verdict : %s" % (bc, "OUI" if bc == best else "NON")
            L += ["### Controle independant : altimetrie satellite (< %d km d'un point)" % RAYON_ALT_KM,
                  "%d heure(s) observee(s) dont %d au-dessus du seuil ; colonnes lues : %s. %s." % (len(obs_alt), nqa, ", ".join(sorted(cols_alt)) or "aucune", conc[0].upper() + conc[1:]), ""]
            if obs_alt:
                L += ["| modele | echeance | heures | MAE | biais |", "|---|---|---|---|---|"]
                for mod, res in sorted(sca.items()):
                    for e in ECHEANCES:
                        a = res.get(e, {}).get("archipel")
                        L.append("| %s | J+%d | %s | %s | %s |" % (mod, e, a[0] if a else 0, ("%.2f m" % a[1]) if a else "—", ("%+.2f" % a[2]) if a else "—"))
                L.append("")
            J["variables"][var]["controle_altimetrie"] = {"heures": len(obs_alt), "heures_qualifiantes": nqa, "meilleur": bc,
                                                           "concordance": (bc == best) if bc else None}
    L += ["## Lecture", "Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud",
          "donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.",
          "Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois."]
B.mkdir(parents=True, exist_ok=True)
(B / "verdict.md").write_text("\n".join(L) + "\n", encoding="utf-8")
(B / "verdict.json").write_text(json.dumps(J, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n".join(L))
