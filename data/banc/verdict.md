# Verdict du banc de fiabilite

Genere le 2026-10-11 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **25** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 624 heures observees dont **13** au-dessus du seuil.
**En attente** : 28 jours non atteints (25/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 13 | 9.82 km/h | -9.82 | — | 9.82 | — |
| ecmwf_ifs | J+3 | 12 | 8.64 km/h | -8.64 | — | 8.64 | — |
| ecmwf_ifs | J+6 | 12 | 14.41 km/h | -14.41 | — | 14.41 | — |
| gfs_seamless | J+1 | 13 | 5.34 km/h | -3.01 | — | 5.34 | — |
| gfs_seamless | J+3 | 12 | 7.07 km/h | -3.97 | — | 7.07 | — |
| gfs_seamless | J+6 | 12 | 11.19 km/h | -11.19 | — | 11.19 | — |
| icon_eu | J+1 | 13 | 13.91 km/h | -13.91 | — | 13.91 | — |
| icon_eu | J+3 | 12 | 12.79 km/h | -12.79 | — | 12.79 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 13 | 12.92 km/h | -12.92 | — | 12.92 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
**Aucun arbitre** : aucune observation de houle dans l'archive. Aucun score n'est calcule, aucun modele n'est designe.
Voir data/banc/arbitre-houle.txt.

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 2653 heures observees dont **830** au-dessus du seuil.
**En attente** : 28 jours non atteints (25/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 752 | 0.48 m/s | -0.48 | 0.44 | 0.58 | 0.19 |
| copernicus_courant | J+3 | 684 | 0.49 m/s | -0.49 | 0.45 | 0.60 | 0.19 |
| copernicus_courant | J+6 | 575 | 0.47 m/s | -0.47 | 0.41 | 0.60 | 0.18 |
| meteofrance_currents | J+1 | 752 | 0.45 m/s | -0.45 | 0.41 | 0.54 | 0.22 |
| meteofrance_currents | J+3 | 684 | 0.45 m/s | -0.45 | 0.40 | 0.55 | 0.23 |
| meteofrance_currents | J+6 | 575 | 0.44 m/s | -0.44 | 0.38 | 0.56 | 0.23 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
