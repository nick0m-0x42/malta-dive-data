# Verdict du banc de fiabilite

Genere le 2026-10-20 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **34** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 836 heures observees dont **66** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 66 | 8.12 km/h | -8.12 | — | 8.12 | — |
| ecmwf_ifs | J+3 | 65 | 9.08 km/h | -9.07 | — | 9.08 | — |
| ecmwf_ifs | J+6 | 65 | 13.32 km/h | -13.32 | — | 13.32 | — |
| gfs_seamless | J+1 | 66 | 3.92 km/h | -1.54 | — | 3.92 | — |
| gfs_seamless | J+3 | 65 | 6.02 km/h | -3.98 | — | 6.02 | — |
| gfs_seamless | J+6 | 65 | 8.44 km/h | -8.18 | — | 8.44 | — |
| icon_eu | J+1 | 66 | 12.88 km/h | -12.88 | — | 12.88 | — |
| icon_eu | J+3 | 65 | 14.25 km/h | -14.25 | — | 14.25 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 66 | 12.02 km/h | -12.02 | — | 12.02 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 6144 heures observees dont **3360** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 3229 | 0.11 m | -0.01 | 0.12 | 0.11 | 0.10 |
| copernicus_houle | J+3 | 3211 | 0.19 m | -0.10 | 0.19 | 0.18 | 0.20 |
| copernicus_houle | J+6 | 3164 | 0.34 m | -0.26 | 0.34 | 0.31 | 0.38 |
| ecmwf_wam025 | J+1 | 3229 | 0.19 m | -0.04 | 0.22 | 0.17 | 0.15 |
| ecmwf_wam025 | J+3 | 3211 | 0.21 m | -0.08 | 0.24 | 0.19 | 0.18 |
| ecmwf_wam025 | J+6 | 3164 | 0.33 m | -0.26 | 0.36 | 0.32 | 0.31 |
| meteofrance_wave | J+1 | 3229 | 0.19 m | -0.10 | 0.23 | 0.19 | 0.15 |
| meteofrance_wave | J+3 | 3211 | 0.26 m | -0.17 | 0.29 | 0.24 | 0.22 |
| meteofrance_wave | J+6 | 3164 | 0.36 m | -0.32 | 0.39 | 0.33 | 0.35 |
| ncep_gfswave016 | J+1 | 3229 | 0.20 m | -0.13 | 0.20 | 0.20 | 0.22 |
| ncep_gfswave016 | J+3 | 3211 | 0.32 m | -0.23 | 0.35 | 0.31 | 0.29 |
| ncep_gfswave016 | J+6 | 3164 | 0.44 m | -0.40 | 0.44 | 0.46 | 0.41 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
12 heure(s) observee(s) dont 12 au-dessus du seuil ; colonnes lues : VAVH. Trop peu d'heures pour juger (12 h au-dessus du seuil, 30 h exigees par echeance).

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 12 | 0.44 m | -0.39 |
| copernicus_houle | J+3 | 12 | 0.47 m | -0.39 |
| copernicus_houle | J+6 | 12 | 0.81 m | -0.81 |
| ecmwf_wam025 | J+1 | 12 | 0.37 m | -0.35 |
| ecmwf_wam025 | J+3 | 12 | 0.36 m | -0.35 |
| ecmwf_wam025 | J+6 | 12 | 0.55 m | -0.55 |
| meteofrance_wave | J+1 | 12 | 0.31 m | -0.29 |
| meteofrance_wave | J+3 | 12 | 0.37 m | -0.37 |
| meteofrance_wave | J+6 | 12 | 0.67 m | -0.67 |
| ncep_gfswave016 | J+1 | 12 | 0.42 m | -0.39 |
| ncep_gfswave016 | J+3 | 12 | 0.55 m | -0.55 |
| ncep_gfswave016 | J+6 | 12 | 0.83 m | -0.83 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 3586 heures observees dont **1099** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1021 | 0.47 m/s | -0.47 | 0.43 | 0.59 | 0.17 |
| copernicus_courant | J+3 | 953 | 0.48 m/s | -0.48 | 0.44 | 0.61 | 0.18 |
| copernicus_courant | J+6 | 844 | 0.47 m/s | -0.47 | 0.41 | 0.61 | 0.18 |
| meteofrance_currents | J+1 | 1021 | 0.44 m/s | -0.44 | 0.40 | 0.54 | 0.18 |
| meteofrance_currents | J+3 | 953 | 0.44 m/s | -0.44 | 0.40 | 0.55 | 0.19 |
| meteofrance_currents | J+6 | 844 | 0.44 m/s | -0.44 | 0.38 | 0.56 | 0.20 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
