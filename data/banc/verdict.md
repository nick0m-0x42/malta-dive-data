# Verdict du banc de fiabilite

Genere le 2026-09-25 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **9** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 240 heures observees dont **6** au-dessus du seuil.
**En attente** : 28 jours non atteints (9/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 6 | 10.26 km/h | -10.26 | — | 10.26 | — |
| ecmwf_ifs | J+3 | 5 | 7.50 km/h | -7.50 | — | 7.50 | — |
| ecmwf_ifs | J+6 | 5 | 12.28 km/h | -12.28 | — | 12.28 | — |
| gfs_seamless | J+1 | 6 | 4.45 km/h | -1.06 | — | 4.45 | — |
| gfs_seamless | J+3 | 5 | 11.84 km/h | -11.84 | — | 11.84 | — |
| gfs_seamless | J+6 | 5 | 14.12 km/h | -14.12 | — | 14.12 | — |
| icon_eu | J+1 | 6 | 12.13 km/h | -12.13 | — | 12.13 | — |
| icon_eu | J+3 | 5 | 13.04 km/h | -13.04 | — | 13.04 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 6 | 12.31 km/h | -12.31 | — | 12.31 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
**Aucun arbitre** : aucune observation de houle dans l'archive. Aucun score n'est calcule, aucun modele n'est designe.
Voir data/banc/arbitre-houle.txt.

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 1009 heures observees dont **368** au-dessus du seuil.
**En attente** : 28 jours non atteints (9/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 290 | 0.44 m/s | -0.44 | 0.46 | 0.50 | 0.19 |
| copernicus_courant | J+3 | 222 | 0.43 m/s | -0.43 | 0.47 | 0.51 | 0.19 |
| copernicus_courant | J+6 | 113 | 0.39 m/s | -0.39 | 0.39 | 0.51 | 0.20 |
| meteofrance_currents | J+1 | 290 | 0.43 m/s | -0.43 | 0.44 | 0.49 | 0.22 |
| meteofrance_currents | J+3 | 222 | 0.42 m/s | -0.42 | 0.44 | 0.49 | 0.23 |
| meteofrance_currents | J+6 | 113 | 0.37 m/s | -0.37 | 0.36 | 0.49 | 0.23 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
