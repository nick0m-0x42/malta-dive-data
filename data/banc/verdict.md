# Verdict du banc de fiabilite

Genere le 2026-10-15 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **29** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 716 heures observees dont **39** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 39 | 6.59 km/h | -6.59 | — | 6.59 | — |
| ecmwf_ifs | J+3 | 38 | 9.15 km/h | -9.13 | — | 9.15 | — |
| ecmwf_ifs | J+6 | 38 | 13.50 km/h | -13.50 | — | 13.50 | — |
| gfs_seamless | J+1 | 39 | 3.82 km/h | -1.29 | — | 3.82 | — |
| gfs_seamless | J+3 | 38 | 6.99 km/h | -4.27 | — | 6.99 | — |
| gfs_seamless | J+6 | 38 | 9.78 km/h | -9.58 | — | 9.78 | — |
| icon_eu | J+1 | 39 | 12.33 km/h | -12.33 | — | 12.33 | — |
| icon_eu | J+3 | 38 | 14.00 km/h | -14.00 | — | 14.00 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 39 | 11.30 km/h | -11.30 | — | 11.30 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
**Aucun arbitre** : aucune observation de houle dans l'archive. Aucun score n'est calcule, aucun modele n'est designe.
Voir data/banc/arbitre-houle.txt.

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 3078 heures observees dont **931** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 853 | 0.47 m/s | -0.47 | 0.43 | 0.57 | 0.18 |
| copernicus_courant | J+3 | 785 | 0.48 m/s | -0.48 | 0.44 | 0.59 | 0.18 |
| copernicus_courant | J+6 | 676 | 0.45 m/s | -0.45 | 0.40 | 0.58 | 0.18 |
| meteofrance_currents | J+1 | 853 | 0.43 m/s | -0.43 | 0.39 | 0.51 | 0.20 |
| meteofrance_currents | J+3 | 785 | 0.43 m/s | -0.43 | 0.40 | 0.52 | 0.21 |
| meteofrance_currents | J+6 | 676 | 0.42 m/s | -0.42 | 0.37 | 0.53 | 0.21 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
