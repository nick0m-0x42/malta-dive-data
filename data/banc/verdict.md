# Verdict du banc de fiabilite

Genere le 2026-10-31 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **45** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 1100 heures observees dont **109** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 109 | 6.50 km/h | -6.34 | — | 6.50 | — |
| ecmwf_ifs | J+3 | 108 | 8.59 km/h | -8.42 | — | 8.59 | — |
| ecmwf_ifs | J+6 | 108 | 13.42 km/h | -13.30 | — | 13.42 | — |
| gfs_seamless | J+1 | 109 | 4.40 km/h | +0.09 | — | 4.40 | — |
| gfs_seamless | J+3 | 108 | 6.06 km/h | -0.94 | — | 6.06 | — |
| gfs_seamless | J+6 | 108 | 7.51 km/h | -6.77 | — | 7.51 | — |
| icon_eu | J+1 | 109 | 12.23 km/h | -12.23 | — | 12.23 | — |
| icon_eu | J+3 | 108 | 13.61 km/h | -13.61 | — | 13.61 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 109 | 11.43 km/h | -11.43 | — | 11.43 | — |
| italia_meteo_arpae_icon_2i | J+3 | 1 | 14.83 km/h | -14.83 | — | 14.83 | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 8256 heures observees dont **5278** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 5147 | 0.10 m | -0.00 | 0.11 | 0.10 | 0.10 |
| copernicus_houle | J+3 | 5129 | 0.19 m | -0.07 | 0.19 | 0.18 | 0.21 |
| copernicus_houle | J+6 | 5082 | 0.35 m | -0.18 | 0.35 | 0.33 | 0.38 |
| ecmwf_wam025 | J+1 | 5147 | 0.19 m | -0.01 | 0.21 | 0.18 | 0.17 |
| ecmwf_wam025 | J+3 | 5129 | 0.21 m | -0.06 | 0.23 | 0.20 | 0.19 |
| ecmwf_wam025 | J+6 | 5082 | 0.39 m | -0.19 | 0.41 | 0.36 | 0.39 |
| meteofrance_wave | J+1 | 5147 | 0.19 m | -0.06 | 0.20 | 0.20 | 0.17 |
| meteofrance_wave | J+3 | 5129 | 0.25 m | -0.12 | 0.26 | 0.26 | 0.23 |
| meteofrance_wave | J+6 | 5082 | 0.38 m | -0.22 | 0.38 | 0.36 | 0.38 |
| ncep_gfswave016 | J+1 | 5147 | 0.22 m | -0.06 | 0.21 | 0.22 | 0.25 |
| ncep_gfswave016 | J+3 | 5129 | 0.31 m | -0.10 | 0.33 | 0.31 | 0.30 |
| ncep_gfswave016 | J+6 | 5082 | 0.42 m | -0.28 | 0.42 | 0.45 | 0.40 |

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
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 4765 heures observees dont **1504** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1426 | 0.45 m/s | -0.45 | 0.40 | 0.58 | 0.17 |
| copernicus_courant | J+3 | 1358 | 0.46 m/s | -0.46 | 0.41 | 0.60 | 0.19 |
| copernicus_courant | J+6 | 1249 | 0.45 m/s | -0.45 | 0.38 | 0.59 | 0.19 |
| meteofrance_currents | J+1 | 1426 | 0.42 m/s | -0.42 | 0.36 | 0.54 | 0.18 |
| meteofrance_currents | J+3 | 1358 | 0.42 m/s | -0.42 | 0.36 | 0.55 | 0.18 |
| meteofrance_currents | J+6 | 1227 | 0.42 m/s | -0.42 | 0.36 | 0.56 | 0.19 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
