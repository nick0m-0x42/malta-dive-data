# Verdict du banc de fiabilite

Genere le 2026-10-22 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **36** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 884 heures observees dont **79** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 79 | 7.42 km/h | -7.41 | — | 7.42 | — |
| ecmwf_ifs | J+3 | 78 | 9.17 km/h | -9.16 | — | 9.17 | — |
| ecmwf_ifs | J+6 | 78 | 14.02 km/h | -14.02 | — | 14.02 | — |
| gfs_seamless | J+1 | 79 | 4.07 km/h | -1.10 | — | 4.07 | — |
| gfs_seamless | J+3 | 78 | 6.26 km/h | -3.22 | — | 6.26 | — |
| gfs_seamless | J+6 | 78 | 8.46 km/h | -7.96 | — | 8.46 | — |
| icon_eu | J+1 | 79 | 12.60 km/h | -12.60 | — | 12.60 | — |
| icon_eu | J+3 | 78 | 14.68 km/h | -14.68 | — | 14.68 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 79 | 11.73 km/h | -11.73 | — | 11.73 | — |
| italia_meteo_arpae_icon_2i | J+3 | 1 | 14.83 km/h | -14.83 | — | 14.83 | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 6528 heures observees dont **3744** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 3613 | 0.11 m | -0.02 | 0.12 | 0.11 | 0.10 |
| copernicus_houle | J+3 | 3595 | 0.19 m | -0.10 | 0.19 | 0.19 | 0.20 |
| copernicus_houle | J+6 | 3548 | 0.35 m | -0.23 | 0.34 | 0.33 | 0.38 |
| ecmwf_wam025 | J+1 | 3613 | 0.18 m | -0.05 | 0.21 | 0.17 | 0.15 |
| ecmwf_wam025 | J+3 | 3595 | 0.20 m | -0.07 | 0.23 | 0.19 | 0.17 |
| ecmwf_wam025 | J+6 | 3548 | 0.34 m | -0.23 | 0.35 | 0.34 | 0.33 |
| meteofrance_wave | J+1 | 3613 | 0.19 m | -0.10 | 0.22 | 0.20 | 0.16 |
| meteofrance_wave | J+3 | 3595 | 0.25 m | -0.17 | 0.28 | 0.25 | 0.22 |
| meteofrance_wave | J+6 | 3548 | 0.36 m | -0.29 | 0.38 | 0.35 | 0.36 |
| ncep_gfswave016 | J+1 | 3613 | 0.20 m | -0.12 | 0.19 | 0.20 | 0.23 |
| ncep_gfswave016 | J+3 | 3595 | 0.31 m | -0.21 | 0.34 | 0.31 | 0.29 |
| ncep_gfswave016 | J+6 | 3548 | 0.43 m | -0.39 | 0.42 | 0.45 | 0.41 |

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
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 3797 heures observees dont **1209** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1131 | 0.47 m/s | -0.47 | 0.43 | 0.60 | 0.17 |
| copernicus_courant | J+3 | 1063 | 0.48 m/s | -0.48 | 0.44 | 0.62 | 0.19 |
| copernicus_courant | J+6 | 954 | 0.46 m/s | -0.46 | 0.41 | 0.61 | 0.19 |
| meteofrance_currents | J+1 | 1131 | 0.43 m/s | -0.43 | 0.39 | 0.54 | 0.18 |
| meteofrance_currents | J+3 | 1063 | 0.44 m/s | -0.43 | 0.39 | 0.56 | 0.18 |
| meteofrance_currents | J+6 | 954 | 0.44 m/s | -0.44 | 0.39 | 0.57 | 0.19 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
