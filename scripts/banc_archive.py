#!/usr/bin/env python3
"""banc_archive.py : archive quotidienne du banc de fiabilite des modeles (etape 2).

POURQUOI : Malta Dive Atlas veut une carte a temoins vent / houle / courant et
un Dive Index fondes sur le modele le PLUS FIABLE, pas le plus dense. La
fiabilite se mesure en prevision, contre des observations reelles, sur au moins
28 jours et 30 h au-dessus des seuils par variable et par echeance (regle du
17/09, TODO du depot prive). Ce script tourne chaque jour et archive :
  - les previsions 7 jours, horaires, de chaque modele candidat, aux points
    d'observation (Luqa pour le vent, points marins dans la couverture radar) ;
  - les observations : METAR LMML (IEM) et radar HF CALYPSO, courants et, si un
    jeu ouvert existe, vagues (ERDDAP EuroGOOS HFR Node, CC BY 4.0, citation
    obligatoire).
Il ne calcule aucun verdict : il amasse. Le verdict est un script separe.
Regle du projet : un 200 ne prouve rien, on compte les valeurs non vides, et
tout manque est ecrit dans le rapport, jamais masque.
Sortie : data/banc/prev/<date>.json.gz, data/banc/obs/<source>/<date>.*.gz,
data/banc/last-run.txt (une ligne OK/ECHEC puis le detail).
Idempotent : une date deja archivee est reecrite a l'identique ou completee.
17/09 soir : aucun rapport n'avait jamais ete commite. Cause trouvee par un
essai a blanc : gzip.open() refuse le parametre mtime, le script plantait juste
apres les previsions, avant tout fichier ; le job n'avait rien a commiter.
L'hypothese precedente (depassement des 30 min) etait fausse ; la recherche
des vagues reste bornee par prudence. Desormais le rapport est ecrit apres
chaque etape, toute exception imprevue l'ecrit aussi, et une alarme arrete le
script proprement a 20 min en disant ou il s'est arrete.
"""
import datetime as dt, gzip, io, json, pathlib, signal, sys, time
import urllib.request, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "banc"
TODAY = dt.datetime.utcnow().strftime("%Y-%m-%d")
LOG, PROBLEMES = [], []
def say(s): print(s, flush=True); LOG.append(s)
def pb(s): say("PROBLEME " + s); PROBLEMES.append(s)
T0 = time.time()
def report(etape):
    say("-- etape %s terminee a %.0f s" % (etape, time.time() - T0))
    tete = ("OK " if not PROBLEMES else "ECHEC ") + dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ") + \
           " · %d probleme(s) · derniere etape : %s" % (len(PROBLEMES), etape)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "last-run.txt").write_text(tete + "\n" + "\n".join(LOG) + "\n", encoding="utf-8")
def alarme(signum, frame):
    pb("delai de 20 min depasse, arret propre")
    report("interrompu")
    sys.exit(1)
def imprevu(tp, val, tb):
    import traceback
    pb("exception imprevue : " + "".join(traceback.format_exception_only(tp, val)).strip())
    say("".join(traceback.format_tb(tb))[-800:])
    report("exception")
    sys.exit(1)
sys.excepthook = imprevu
signal.signal(signal.SIGALRM, alarme)
signal.alarm(20 * 60)

def get(url, timeout=120, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "malta-dive-atlas-banc/1 (non-commercial)"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            last = (e.code, e.read()[:300])
            if e.code in (400, 404):
                return last
        except Exception as e:
            last = (0, repr(e).encode()[:300])
        if i < tries - 1:
            time.sleep(5 * (i + 1))
    return last

def wgz(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    # 17/09 : gzip.open() n'accepte pas mtime ; ce TypeError tuait chaque run
    # avant le premier fichier, donc sans rien a commiter ni rapport.
    with open(path, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=9, mtime=0) as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))

# --- points ---------------------------------------------------------------
# LMML : station METAR de Luqa. Points marins : dans la couverture CALYPSO
# (canal Malte-Sicile au nord, grappe sud Ta' Cenc / Ghar Lapsi).
POINTS = {
    "LMML":      (35.8575, 14.4775),
    "N-Gozo":    (36.1200, 14.2500),
    "N-Comino":  (36.0600, 14.3400),
    "N-Qawra":   (36.0000, 14.4300),
    "N-Valletta":(35.9600, 14.5400),
    "E-Delimara":(35.8300, 14.6000),
    "S-Zurrieq": (35.7900, 14.4400),
    "S-Lapsi":   (35.8100, 14.3500),
    "S-Gozo":    (35.9900, 14.2400),
}
names = list(POINTS)
lats = ",".join(str(POINTS[n][0]) for n in names)
lons = ",".join(str(POINTS[n][1]) for n in names)

FC = "https://api.open-meteo.com/v1/forecast"
MA = "https://marine-api.open-meteo.com/v1/marine"
MODELES = [
    ("vent", FC, "gfs_seamless", "wind_speed_10m,wind_direction_10m,wind_gusts_10m", {}),
    ("vent", FC, "ecmwf_ifs", "wind_speed_10m,wind_direction_10m,wind_gusts_10m", {}),
    ("vent", FC, "icon_eu", "wind_speed_10m,wind_direction_10m,wind_gusts_10m", {}),
    ("vent", FC, "italia_meteo_arpae_icon_2i", "wind_speed_10m,wind_direction_10m,wind_gusts_10m", {}),
    ("houle", MA, "ecmwf_wam025", "wave_height,wave_direction,wave_period", {"cell_selection": "sea"}),
    ("houle", MA, "meteofrance_wave", "wave_height,wave_direction,wave_period", {"cell_selection": "sea"}),
    ("houle", MA, "ncep_gfswave016", "wave_height,wave_direction,wave_period", {"cell_selection": "sea"}),
    ("courant", MA, "meteofrance_currents", "ocean_current_velocity,ocean_current_direction", {"cell_selection": "sea"}),
]

# --- 1. previsions ----------------------------------------------------------
prev = {"emis": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"), "points": POINTS, "modeles": {}}
for couche, url, model, hourly, extra in MODELES:
    p = {"latitude": lats, "longitude": lons, "hourly": hourly, "models": model,
         "forecast_days": 7, "timezone": "UTC", "wind_speed_unit": "kmh"}
    p.update(extra)
    st, body = get(url + "?" + urllib.parse.urlencode(p), timeout=60)
    if st != 200:
        pb("prevision %s : HTTP %s %s" % (model, st, body[:120])); continue
    d = json.loads(body); d = d if isinstance(d, list) else [d]
    rec, nonvides, total = {}, 0, 0
    for n, loc in zip(names, d):
        h = loc.get("hourly", {})
        rec[n] = {"grid": [loc.get("latitude"), loc.get("longitude")], "hourly": h}
        for v in hourly.split(","):
            vals = h.get(v) or []
            total += len(vals); nonvides += sum(1 for x in vals if x is not None)
    prev["modeles"][model] = {"couche": couche, "data": rec}
    say("prevision %-28s %d/%d valeurs non vides" % (model, nonvides, total))
    if total == 0 or nonvides == 0:
        pb("prevision %s : aucune valeur" % model)
    time.sleep(1)
wgz(OUT / "prev" / (TODAY + ".json.gz"), json.dumps(prev, separators=(",", ":")))
report("previsions")

# --- 2. observations LMML (IEM), 2 jours -------------------------------------
d0 = dt.date.today() - dt.timedelta(days=2); d1 = dt.date.today()
iem = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=LMML"
       "&data=sknt&data=drct&data=gust&tz=Etc/UTC&format=onlycomma&latlon=yes&missing=M&trace=T"
       "&year1=%d&month1=%d&day1=%d&year2=%d&month2=%d&day2=%d"
       % (d0.year, d0.month, d0.day, d1.year, d1.month, d1.day))
st, body = get(iem, timeout=60, tries=2)
rows = [l for l in body.decode("utf-8", "replace").splitlines() if l.startswith("LMML")] if st == 200 else []
say("observation LMML : HTTP %s, %d lignes" % (st, len(rows)))
if not rows: pb("LMML vide")
else: wgz(OUT / "obs" / "lmml" / (TODAY + ".csv.gz"), body)
report("LMML")

# --- 3. CALYPSO : decouverte des jeux, courants, vagues ------------------------
ERD = "https://erddap.hfrnode.eu/erddap"
t0 = (dt.datetime.utcnow() - dt.timedelta(hours=48)).strftime("%Y-%m-%dT%H:00:00Z")
t1 = dt.datetime.utcnow().strftime("%Y-%m-%dT%H:00:00Z")
BOX = "[(35.70):1:(36.20)][(14.05):1:(14.70)]"

st, body = get(ERD + "/search/index.json?page=1&itemsPerPage=200&searchFor=CALYPSO", timeout=60, tries=2)
jeux = []
if st == 200:
    tab = json.loads(body)["table"]; ci = tab["columnNames"].index("Dataset ID")
    jeux = [r[ci] for r in tab["rows"]]
say("jeux CALYPSO sur ERDDAP : " + (", ".join(jeux) if jeux else "aucun (HTTP %s)" % st))
report("recherche CALYPSO")

def calypso(ds, variables, tag):
    # borne de fin = derniere heure publiee. Crochets et parentheses encodes : Tomcat
    # refuse [ ] bruts dans l'URL (HTTP 400, runs du 17/09 17:37 et 17:40).
    q = ",".join("%s[(%s):1:(last)][0]%s" % (v, t0, BOX) for v in variables)
    st, body = get("%s/griddap/%s.csv?%s" % (ERD, ds, urllib.parse.quote(q, safe=":,.")), timeout=120, tries=2)
    if st != 200:
        pb("CALYPSO %s : HTTP %s %s" % (tag, st, body[:160])); return
    lines = body.decode("utf-8", "replace").splitlines()[2:]
    heures = set(); ok = 0
    for l in lines:
        p = l.split(",")
        heures.add(p[0])
        if any(x not in ("NaN", "") for x in p[4:]): ok += 1
    say("observation CALYPSO %s : %d lignes, %d heures, %d lignes renseignees" % (tag, len(lines), len(heures), ok))
    if ok == 0: pb("CALYPSO %s : aucune valeur" % tag)
    else: wgz(OUT / "obs" / ("calypso-" + tag) / (TODAY + ".csv.gz"), body)

calypso("EUHFR_NRTcurrent_HFR-CALYPSO-Total_v3", ["EWCT", "NSCT"], "courant")
report("CALYPSO courant")

# Vagues : on cherche un jeu CALYPSO qui porte une hauteur significative.
vague = None
cands = [j for j in jeux if "wav" in j.lower()][:6]  # borne par prudence
say("candidats vagues CALYPSO : " + (", ".join(cands) if cands else "aucun"))
for ds in cands:
    st, das = get("%s/griddap/%s.das" % (ERD, ds), timeout=30, tries=1)
    if st != 200:
        continue
    txt = das.decode("utf-8", "replace")
    for v in ("VHM0", "WSH", "VAVH", "HM0"):
        if ("\n  %s {" % v) in txt:
            vague = (ds, v); break
    if vague: break
if vague:
    say("jeu vagues CALYPSO : %s, variable %s" % vague)
    calypso(vague[0], [vague[1]], "vagues")
else:
    pb("aucun jeu de vagues CALYPSO ouvert trouve sur ERDDAP (a chercher ailleurs)")

# --- rapport ------------------------------------------------------------------
signal.alarm(0)
report("fin")
print(open(OUT / "last-run.txt", encoding="utf-8").readline().strip())
sys.exit(1 if PROBLEMES else 0)
