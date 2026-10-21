# Verdict du banc de fiabilite

Genere le 2026-10-21 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **35** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 860 heures observees dont **67** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 67 | 8.17 km/h | -8.17 | — | 8.17 | — |
| ecmwf_ifs | J+3 | 66 | 9.09 km/h | -9.08 | — | 9.09 | — |
| ecmwf_ifs | J+6 | 66 | 13.32 km/h | -13.32 | — | 13.32 | — |
| gfs_seamless | J+1 | 67 | 3.93 km/h | -1.45 | — | 3.93 | — |
| gfs_seamless | J+3 | 66 | 6.01 km/h | -3.84 | — | 6.01 | — |
| gfs_seamless | J+6 | 66 | 8.48 km/h | -8.22 | — | 8.48 | — |
| icon_eu | J+1 | 67 | 12.93 km/h | -12.93 | — | 12.93 | — |
| icon_eu | J+3 | 66 | 14.31 km/h | -14.31 | — | 14.31 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 67 | 12.01 km/h | -12.01 | — | 12.01 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 6336 heures observees dont **3552** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 3421 | 0.11 m | -0.02 | 0.12 | 0.11 | 0.10 |
| copernicus_houle | J+3 | 3403 | 0.20 m | -0.11 | 0.19 | 0.20 | 0.20 |
| copernicus_houle | J+6 | 3356 | 0.34 m | -0.27 | 0.34 | 0.32 | 0.37 |
| ecmwf_wam025 | J+1 | 3421 | 0.18 m | -0.05 | 0.22 | 0.17 | 0.15 |
| ecmwf_wam025 | J+3 | 3403 | 0.21 m | -0.08 | 0.24 | 0.20 | 0.17 |
| ecmwf_wam025 | J+6 | 3356 | 0.34 m | -0.27 | 0.35 | 0.33 | 0.31 |
| meteofrance_wave | J+1 | 3421 | 0.20 m | -0.10 | 0.22 | 0.20 | 0.16 |
| meteofrance_wave | J+3 | 3403 | 0.26 m | -0.18 | 0.29 | 0.26 | 0.23 |
| meteofrance_wave | J+6 | 3356 | 0.36 m | -0.33 | 0.38 | 0.35 | 0.35 |
| ncep_gfswave016 | J+1 | 3421 | 0.21 m | -0.13 | 0.19 | 0.20 | 0.23 |
| ncep_gfswave016 | J+3 | 3403 | 0.32 m | -0.23 | 0.35 | 0.32 | 0.29 |
| ncep_gfswave016 | J+6 | 3356 | 0.44 m | -0.40 | 0.43 | 0.47 | 0.42 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
19 heure(s) observee(s) dont 19 au-dessus du seuil ; colonnes lues : VAVH. Trop peu d'heures pour juger (19 h au-dessus du seuil, 30 h exigees par echeance).

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 19 | 0.38 m | -0.34 |
| copernicus_houle | J+3 | 19 | 0.42 m | -0.36 |
| copernicus_houle | J+6 | 19 | 0.67 m | -0.49 |
| ecmwf_wam025 | J+1 | 19 | 0.34 m | -0.30 |
| ecmwf_wam025 | J+3 | 19 | 0.33 m | -0.29 |
| ecmwf_wam025 | J+6 | 19 | 0.54 m | -0.35 |
| meteofrance_wave | J+1 | 19 | 0.28 m | -0.26 |
| meteofrance_wave | J+3 | 19 | 0.35 m | -0.34 |
| meteofrance_wave | J+6 | 19 | 0.60 m | -0.45 |
| ncep_gfswave016 | J+1 | 19 | 0.39 m | -0.35 |
| ncep_gfswave016 | J+3 | 19 | 0.41 m | -0.38 |
| ncep_gfswave016 | J+6 | 19 | 0.68 m | -0.66 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 3676 heures observees dont **1142** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1064 | 0.48 m/s | -0.47 | 0.43 | 0.60 | 0.17 |
| copernicus_courant | J+3 | 996 | 0.48 m/s | -0.48 | 0.44 | 0.62 | 0.18 |
| copernicus_courant | J+6 | 887 | 0.47 m/s | -0.47 | 0.41 | 0.61 | 0.18 |
| meteofrance_currents | J+1 | 1064 | 0.44 m/s | -0.44 | 0.40 | 0.54 | 0.19 |
| meteofrance_currents | J+3 | 996 | 0.44 m/s | -0.44 | 0.40 | 0.56 | 0.19 |
| meteofrance_currents | J+6 | 887 | 0.44 m/s | -0.44 | 0.39 | 0.57 | 0.19 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
