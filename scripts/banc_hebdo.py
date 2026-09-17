#!/usr/bin/env python3
"""banc_hebdo.py : etat du banc de fiabilite, lu dans l'archive elle-meme.

POURQUOI (Nicolas, 17/09) : suivre l'avancement du banc sans ouvrir les fichiers.
Ce script ne fait aucune hypothese : il liste les jours reellement presents dans
data/banc/, compte les trous depuis le premier jour archive, et rappelle la
regle d'arret (28 jours au moins, et 30 h au-dessus des seuils par variable et
par echeance) avec la date au plus tot. Ecrit data/banc/etat.md, relu par la
session de Malta Dive Atlas et par Nicolas.
Il tourne apres l'archive quotidienne : l'etat est donc toujours du jour.
"""
import datetime as dt, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / "data" / "banc"
AUJ = dt.date.today()

def jours(d, motif=r"(\d{4}-\d{2}-\d{2})"):
    if not d.exists(): return []
    out = []
    for f in d.iterdir():
        m = re.match(motif, f.name)
        if m:
            try: out.append(dt.date.fromisoformat(m.group(1)))
            except ValueError: pass
    return sorted(set(out))

sources = {
    "previsions (GFS, IFS, ICON-EU, ICON-2I, WAM, Meteo-France, GFS Wave, courants)": jours(B / "prev"),
    "previsions Copernicus MEDSEA (houle, courant)": jours(B / "prev-cmems"),
    "observations METAR Luqa (LMML)": jours(B / "obs" / "lmml"),
    "observations courants CALYPSO": jours(B / "obs" / "calypso-courant"),
    "observations vagues CALYPSO": jours(B / "obs" / "calypso-vagues"),
}
tous = sorted({j for v in sources.values() for j in v})
debut = tous[0] if tous else None

L = ["# Etat du banc de fiabilite", "",
     "Genere le %s par scripts/banc_hebdo.py. Chiffres lus dans data/banc/, jamais supposes." % AUJ.isoformat(), ""]
if not debut:
    L += ["**Aucun jour archive.** Voir data/banc/last-run.txt."]
else:
    attendus = (AUJ - debut).days + 1
    L += ["Premier jour archive : **%s**. Jours ecoules depuis : **%d**." % (debut.isoformat(), attendus), "",
          "| source | jours | dernier | manquants depuis le debut |", "|---|---|---|---|"]
    for nom, js in sources.items():
        if not js:
            L.append("| %s | 0 | — | jamais archive |" % nom); continue
        manque = [ (debut + dt.timedelta(days=i)).isoformat()
                   for i in range(attendus) if (debut + dt.timedelta(days=i)) not in js ]
        trous = "aucun" if not manque else "%d : %s" % (len(manque), ", ".join(manque[:6]) + (" …" if len(manque) > 6 else ""))
        L.append("| %s | %d | %s | %s |" % (nom, len(js), js[-1].isoformat(), trous))
    fin = debut + dt.timedelta(days=27)
    L += ["", "## Regle d'arret",
          "Au moins 28 jours de previsions archivees ET, par variable, au moins 30 h observees",
          "au-dessus du seuil qui compte (vent > 25 km/h, houle > 0,5 m, courant > 0,25 m/s)",
          "a chaque echeance J+1, J+3, J+6. Sinon on prolonge.", "",
          "28 jours atteints au plus tot le **%s**%s." % (fin.isoformat(), " (atteint)" if AUJ >= fin else ""),
          "", "## Dernier run", "```"]
    lr = B / "last-run.txt"
    L += [lr.read_text(encoding="utf-8").strip() if lr.exists() else "aucun rapport", "```"]
    cm = B / "cmems-run.txt"
    if cm.exists():
        L += ["", "## Dernier run Copernicus", "```", cm.read_text(encoding="utf-8").splitlines()[0], "```"]
    ah = B / "arbitre-houle.txt"
    if ah.exists():
        L += ["", "## Arbitre de houle", "```"] + ah.read_text(encoding="utf-8").splitlines()[:12] + ["```"]

(B).mkdir(parents=True, exist_ok=True)
(B / "etat.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L[:14]))
sys.exit(0)
