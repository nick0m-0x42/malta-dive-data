# Verdict du banc de fiabilite

Genere le 2026-10-19 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **33** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 812 heures observees dont **46** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 46 | 7.50 km/h | -7.50 | — | 7.50 | — |
| ecmwf_ifs | J+3 | 45 | 9.46 km/h | -9.44 | — | 9.46 | — |
| ecmwf_ifs | J+6 | 45 | 13.69 km/h | -13.69 | — | 13.69 | — |
| gfs_seamless | J+1 | 46 | 4.40 km/h | -2.10 | — | 4.40 | — |
| gfs_seamless | J+3 | 45 | 6.84 km/h | -4.48 | — | 6.84 | — |
| gfs_seamless | J+6 | 45 | 10.14 km/h | -9.97 | — | 10.14 | — |
| icon_eu | J+1 | 46 | 12.60 km/h | -12.60 | — | 12.60 | — |
| icon_eu | J+3 | 45 | 14.04 km/h | -14.04 | — | 14.04 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 46 | 11.42 km/h | -11.42 | — | 11.42 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 5952 heures observees dont **3283** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 3152 | 0.11 m | -0.01 | 0.12 | 0.11 | 0.10 |
| copernicus_houle | J+3 | 3134 | 0.19 m | -0.09 | 0.19 | 0.19 | 0.20 |
| copernicus_houle | J+6 | 3087 | 0.34 m | -0.26 | 0.34 | 0.31 | 0.38 |
| ecmwf_wam025 | J+1 | 3152 | 0.19 m | -0.04 | 0.22 | 0.17 | 0.15 |
| ecmwf_wam025 | J+3 | 3134 | 0.21 m | -0.08 | 0.24 | 0.19 | 0.18 |
| ecmwf_wam025 | J+6 | 3087 | 0.34 m | -0.26 | 0.36 | 0.33 | 0.31 |
| meteofrance_wave | J+1 | 3152 | 0.20 m | -0.10 | 0.23 | 0.19 | 0.15 |
| meteofrance_wave | J+3 | 3134 | 0.26 m | -0.17 | 0.29 | 0.25 | 0.22 |
| meteofrance_wave | J+6 | 3087 | 0.36 m | -0.32 | 0.39 | 0.34 | 0.35 |
| ncep_gfswave016 | J+1 | 3152 | 0.21 m | -0.13 | 0.20 | 0.20 | 0.22 |
| ncep_gfswave016 | J+3 | 3134 | 0.32 m | -0.23 | 0.35 | 0.31 | 0.29 |
| ncep_gfswave016 | J+6 | 3087 | 0.44 m | -0.40 | 0.44 | 0.47 | 0.41 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
9 heure(s) observee(s) dont 9 au-dessus du seuil ; colonnes lues : VAVH. Trop peu d'heures pour juger (9 h au-dessus du seuil, 30 h exigees par echeance).

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 9 | 0.27 m | -0.19 |
| copernicus_houle | J+3 | 9 | 0.28 m | -0.18 |
| copernicus_houle | J+6 | 9 | 0.73 m | -0.73 |
| ecmwf_wam025 | J+1 | 9 | 0.15 m | -0.13 |
| ecmwf_wam025 | J+3 | 9 | 0.17 m | -0.16 |
| ecmwf_wam025 | J+6 | 9 | 0.35 m | -0.35 |
| meteofrance_wave | J+1 | 9 | 0.16 m | -0.13 |
| meteofrance_wave | J+3 | 9 | 0.21 m | -0.21 |
| meteofrance_wave | J+6 | 9 | 0.56 m | -0.56 |
| ncep_gfswave016 | J+1 | 9 | 0.29 m | -0.24 |
| ncep_gfswave016 | J+3 | 9 | 0.44 m | -0.44 |
| ncep_gfswave016 | J+6 | 9 | 0.73 m | -0.73 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 3489 heures observees dont **1057** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 979 | 0.48 m/s | -0.48 | 0.44 | 0.59 | 0.17 |
| copernicus_courant | J+3 | 911 | 0.49 m/s | -0.49 | 0.44 | 0.61 | 0.18 |
| copernicus_courant | J+6 | 802 | 0.47 m/s | -0.47 | 0.41 | 0.60 | 0.18 |
| meteofrance_currents | J+1 | 979 | 0.44 m/s | -0.44 | 0.40 | 0.53 | 0.19 |
| meteofrance_currents | J+3 | 911 | 0.44 m/s | -0.44 | 0.40 | 0.54 | 0.20 |
| meteofrance_currents | J+6 | 802 | 0.44 m/s | -0.44 | 0.39 | 0.56 | 0.21 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
