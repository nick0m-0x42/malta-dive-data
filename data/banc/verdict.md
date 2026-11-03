# Verdict du banc de fiabilite

Genere le 2026-11-03 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **48** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 1172 heures observees dont **129** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 129 | 6.48 km/h | -5.44 | — | 6.48 | — |
| ecmwf_ifs | J+3 | 128 | 8.12 km/h | -7.94 | — | 8.12 | — |
| ecmwf_ifs | J+6 | 128 | 14.61 km/h | -14.51 | — | 14.61 | — |
| gfs_seamless | J+1 | 129 | 4.57 km/h | +0.89 | — | 4.57 | — |
| gfs_seamless | J+3 | 128 | 5.87 km/h | -0.21 | — | 5.87 | — |
| gfs_seamless | J+6 | 128 | 10.05 km/h | -9.42 | — | 10.05 | — |
| icon_eu | J+1 | 129 | 11.87 km/h | -11.86 | — | 11.87 | — |
| icon_eu | J+3 | 128 | 13.53 km/h | -13.53 | — | 13.53 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 129 | 11.68 km/h | -11.68 | — | 11.68 | — |
| italia_meteo_arpae_icon_2i | J+3 | 1 | 14.83 km/h | -14.83 | — | 14.83 | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 8832 heures observees dont **5382** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 5251 | 0.10 m | -0.00 | 0.11 | 0.10 | 0.10 |
| copernicus_houle | J+3 | 5233 | 0.19 m | -0.07 | 0.19 | 0.18 | 0.21 |
| copernicus_houle | J+6 | 5186 | 0.36 m | -0.16 | 0.36 | 0.33 | 0.38 |
| ecmwf_wam025 | J+1 | 5251 | 0.19 m | -0.01 | 0.21 | 0.18 | 0.16 |
| ecmwf_wam025 | J+3 | 5233 | 0.21 m | -0.05 | 0.23 | 0.21 | 0.19 |
| ecmwf_wam025 | J+6 | 5186 | 0.39 m | -0.18 | 0.41 | 0.36 | 0.39 |
| meteofrance_wave | J+1 | 5251 | 0.19 m | -0.07 | 0.20 | 0.20 | 0.17 |
| meteofrance_wave | J+3 | 5233 | 0.25 m | -0.11 | 0.26 | 0.26 | 0.24 |
| meteofrance_wave | J+6 | 5186 | 0.38 m | -0.21 | 0.38 | 0.36 | 0.39 |
| ncep_gfswave016 | J+1 | 5251 | 0.22 m | -0.06 | 0.21 | 0.22 | 0.24 |
| ncep_gfswave016 | J+3 | 5233 | 0.31 m | -0.10 | 0.33 | 0.31 | 0.30 |
| ncep_gfswave016 | J+6 | 5186 | 0.42 m | -0.27 | 0.42 | 0.45 | 0.39 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
30 heure(s) observee(s) dont 27 au-dessus du seuil ; colonnes lues : VAVH. Trop peu d'heures pour juger (27 h au-dessus du seuil, 30 h exigees par echeance).

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 27 | 0.34 m | -0.29 |
| copernicus_houle | J+3 | 27 | 0.40 m | -0.25 |
| copernicus_houle | J+6 | 27 | 0.60 m | -0.37 |
| ecmwf_wam025 | J+1 | 27 | 0.30 m | -0.26 |
| ecmwf_wam025 | J+3 | 27 | 0.28 m | -0.21 |
| ecmwf_wam025 | J+6 | 27 | 0.53 m | -0.40 |
| meteofrance_wave | J+1 | 27 | 0.25 m | -0.23 |
| meteofrance_wave | J+3 | 27 | 0.34 m | -0.23 |
| meteofrance_wave | J+6 | 27 | 0.54 m | -0.32 |
| ncep_gfswave016 | J+1 | 27 | 0.36 m | -0.31 |
| ncep_gfswave016 | J+3 | 27 | 0.45 m | -0.18 |
| ncep_gfswave016 | J+6 | 27 | 0.60 m | -0.59 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 5004 heures observees dont **1640** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1562 | 0.45 m/s | -0.45 | 0.40 | 0.59 | 0.21 |
| copernicus_courant | J+3 | 1494 | 0.46 m/s | -0.46 | 0.41 | 0.60 | 0.22 |
| copernicus_courant | J+6 | 1385 | 0.45 m/s | -0.45 | 0.38 | 0.60 | 0.23 |
| meteofrance_currents | J+1 | 1562 | 0.41 m/s | -0.41 | 0.36 | 0.54 | 0.20 |
| meteofrance_currents | J+3 | 1494 | 0.42 m/s | -0.42 | 0.36 | 0.55 | 0.21 |
| meteofrance_currents | J+6 | 1363 | 0.43 m/s | -0.43 | 0.35 | 0.56 | 0.24 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
