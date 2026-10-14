# malta-dive-data
Donnees thermocline quotidiennes (05h00 Malte) pour Malta Dive Atlas.
Setup: creer les secrets Actions COPERNICUS_USER et COPERNICUS_PASSWORD (compte marine.copernicus.eu),
puis Actions > Thermocline daily > Run workflow pour le premier run.
Le site lit data/latest.json via raw.githubusercontent.com.

## Surveillance (depuis le 14/10/2026)
`watchdog.yml` + `scripts/watchdog.py` surveillent toutes les sources publiees (instantane,
thermocline, temoins, banc) et ce que lit le site en production : fraicheur selon la periode
prevue, contenu non vide, bornes physiques, donnees figees, modeles du score. Retard : relance
automatique de la collecte. Panne : issue `watchdog` dans ce depot et job en echec ; fermeture
automatique au retour. Etat et rapport : branche `watchdog-state`, `rapport.md`.
Tests : `python -m unittest discover -s tests -v`.
