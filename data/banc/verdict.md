# Verdict du banc de fiabilite

Genere le 2026-09-23 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **7** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 192 heures observees dont **1** au-dessus du seuil.
**En attente** : 28 jours non atteints (7/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 1 | 23.23 km/h | -23.23 | — | 23.23 | — |
| ecmwf_ifs | J+3 | 0 | — | — | — | — | — |
| ecmwf_ifs | J+6 | 0 | — | — | — | — | — |
| gfs_seamless | J+1 | 1 | 16.13 km/h | -16.13 | — | 16.13 | — |
| gfs_seamless | J+3 | 0 | — | — | — | — | — |
| gfs_seamless | J+6 | 0 | — | — | — | — | — |
| icon_eu | J+1 | 1 | 24.83 km/h | -24.83 | — | 24.83 | — |
| icon_eu | J+3 | 0 | — | — | — | — | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 1 | 23.83 km/h | -23.83 | — | 23.83 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
**Aucun arbitre** : aucune observation de houle dans l'archive. Aucun score n'est calcule, aucun modele n'est designe.
Voir data/banc/arbitre-houle.txt.

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 820 heures observees dont **280** au-dessus du seuil.
**En attente** : 28 jours non atteints (7/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 202 | 0.46 m/s | -0.46 | 0.48 | 0.49 | 0.19 |
| copernicus_courant | J+3 | 134 | 0.48 m/s | -0.48 | 0.50 | 0.50 | 0.23 |
| copernicus_courant | J+6 | 25 | 0.37 m/s | -0.37 | 0.38 | 0.40 | 0.24 |
| meteofrance_currents | J+1 | 202 | 0.45 m/s | -0.45 | 0.46 | 0.47 | 0.22 |
| meteofrance_currents | J+3 | 134 | 0.44 m/s | -0.44 | 0.46 | 0.46 | 0.22 |
| meteofrance_currents | J+6 | 25 | 0.33 m/s | -0.33 | 0.33 | 0.36 | 0.26 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
