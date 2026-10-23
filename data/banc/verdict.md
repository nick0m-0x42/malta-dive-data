# Verdict du banc de fiabilite

Genere le 2026-10-23 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **37** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 908 heures observees dont **89** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 89 | 6.98 km/h | -6.92 | — | 6.98 | — |
| ecmwf_ifs | J+3 | 88 | 8.44 km/h | -8.30 | — | 8.44 | — |
| ecmwf_ifs | J+6 | 88 | 14.15 km/h | -14.15 | — | 14.15 | — |
| gfs_seamless | J+1 | 89 | 4.08 km/h | -0.55 | — | 4.08 | — |
| gfs_seamless | J+3 | 88 | 6.44 km/h | -1.97 | — | 6.44 | — |
| gfs_seamless | J+6 | 88 | 8.04 km/h | -7.50 | — | 8.04 | — |
| icon_eu | J+1 | 89 | 12.33 km/h | -12.33 | — | 12.33 | — |
| icon_eu | J+3 | 88 | 14.00 km/h | -14.00 | — | 14.00 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 89 | 11.49 km/h | -11.49 | — | 11.49 | — |
| italia_meteo_arpae_icon_2i | J+3 | 1 | 14.83 km/h | -14.83 | — | 14.83 | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 6720 heures observees dont **3936** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 3805 | 0.11 m | -0.02 | 0.12 | 0.11 | 0.11 |
| copernicus_houle | J+3 | 3787 | 0.20 m | -0.11 | 0.19 | 0.19 | 0.21 |
| copernicus_houle | J+6 | 3740 | 0.36 m | -0.25 | 0.34 | 0.34 | 0.39 |
| ecmwf_wam025 | J+1 | 3805 | 0.18 m | -0.04 | 0.21 | 0.17 | 0.16 |
| ecmwf_wam025 | J+3 | 3787 | 0.21 m | -0.09 | 0.23 | 0.20 | 0.18 |
| ecmwf_wam025 | J+6 | 3740 | 0.34 m | -0.23 | 0.36 | 0.34 | 0.33 |
| meteofrance_wave | J+1 | 3805 | 0.19 m | -0.09 | 0.22 | 0.20 | 0.16 |
| meteofrance_wave | J+3 | 3787 | 0.26 m | -0.17 | 0.28 | 0.25 | 0.23 |
| meteofrance_wave | J+6 | 3740 | 0.37 m | -0.30 | 0.38 | 0.35 | 0.38 |
| ncep_gfswave016 | J+1 | 3805 | 0.21 m | -0.11 | 0.20 | 0.20 | 0.22 |
| ncep_gfswave016 | J+3 | 3787 | 0.31 m | -0.19 | 0.34 | 0.31 | 0.28 |
| ncep_gfswave016 | J+6 | 3740 | 0.42 m | -0.36 | 0.42 | 0.45 | 0.40 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
23 heure(s) observee(s) dont 23 au-dessus du seuil ; colonnes lues : VAVH. Trop peu d'heures pour juger (23 h au-dessus du seuil, 30 h exigees par echeance).

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 23 | 0.34 m | -0.29 |
| copernicus_houle | J+3 | 23 | 0.41 m | -0.23 |
| copernicus_houle | J+6 | 23 | 0.61 m | -0.34 |
| ecmwf_wam025 | J+1 | 23 | 0.30 m | -0.26 |
| ecmwf_wam025 | J+3 | 23 | 0.29 m | -0.25 |
| ecmwf_wam025 | J+6 | 23 | 0.56 m | -0.40 |
| meteofrance_wave | J+1 | 23 | 0.25 m | -0.23 |
| meteofrance_wave | J+3 | 23 | 0.35 m | -0.22 |
| meteofrance_wave | J+6 | 23 | 0.56 m | -0.31 |
| ncep_gfswave016 | J+1 | 23 | 0.35 m | -0.29 |
| ncep_gfswave016 | J+3 | 23 | 0.49 m | -0.16 |
| ncep_gfswave016 | J+6 | 23 | 0.60 m | -0.59 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 3921 heures observees dont **1247** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1169 | 0.46 m/s | -0.46 | 0.42 | 0.59 | 0.17 |
| copernicus_courant | J+3 | 1101 | 0.47 m/s | -0.47 | 0.43 | 0.60 | 0.19 |
| copernicus_courant | J+6 | 992 | 0.45 m/s | -0.45 | 0.40 | 0.59 | 0.19 |
| meteofrance_currents | J+1 | 1169 | 0.42 m/s | -0.42 | 0.39 | 0.53 | 0.18 |
| meteofrance_currents | J+3 | 1101 | 0.43 m/s | -0.43 | 0.39 | 0.54 | 0.18 |
| meteofrance_currents | J+6 | 992 | 0.43 m/s | -0.43 | 0.38 | 0.56 | 0.19 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
