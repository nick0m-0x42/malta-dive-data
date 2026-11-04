# Verdict du banc de fiabilite

Genere le 2026-11-04 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **49** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 1196 heures observees dont **143** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 143 | 6.28 km/h | -4.79 | — | 6.28 | — |
| ecmwf_ifs | J+3 | 142 | 7.64 km/h | -7.43 | — | 7.64 | — |
| ecmwf_ifs | J+6 | 142 | 13.41 km/h | -13.26 | — | 13.41 | — |
| gfs_seamless | J+1 | 143 | 5.04 km/h | +1.71 | — | 5.04 | — |
| gfs_seamless | J+3 | 142 | 5.98 km/h | +0.48 | — | 5.98 | — |
| gfs_seamless | J+6 | 142 | 11.07 km/h | -10.50 | — | 11.07 | — |
| icon_eu | J+1 | 143 | 11.54 km/h | -11.54 | — | 11.54 | — |
| icon_eu | J+3 | 142 | 13.51 km/h | -13.51 | — | 13.51 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 143 | 11.72 km/h | -11.72 | — | 11.72 | — |
| italia_meteo_arpae_icon_2i | J+3 | 1 | 14.83 km/h | -14.83 | — | 14.83 | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 9024 heures observees dont **5569** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 5438 | 0.11 m | -0.02 | 0.12 | 0.11 | 0.11 |
| copernicus_houle | J+3 | 5420 | 0.20 m | -0.07 | 0.19 | 0.18 | 0.21 |
| copernicus_houle | J+6 | 5373 | 0.40 m | -0.21 | 0.40 | 0.35 | 0.46 |
| ecmwf_wam025 | J+1 | 5438 | 0.20 m | -0.02 | 0.22 | 0.20 | 0.18 |
| ecmwf_wam025 | J+3 | 5420 | 0.23 m | -0.07 | 0.25 | 0.22 | 0.22 |
| ecmwf_wam025 | J+6 | 5373 | 0.43 m | -0.23 | 0.45 | 0.38 | 0.46 |
| meteofrance_wave | J+1 | 5438 | 0.21 m | -0.08 | 0.21 | 0.22 | 0.18 |
| meteofrance_wave | J+3 | 5420 | 0.26 m | -0.12 | 0.27 | 0.27 | 0.24 |
| meteofrance_wave | J+6 | 5373 | 0.43 m | -0.26 | 0.43 | 0.38 | 0.46 |
| ncep_gfswave016 | J+1 | 5438 | 0.24 m | -0.07 | 0.22 | 0.23 | 0.25 |
| ncep_gfswave016 | J+3 | 5420 | 0.33 m | -0.12 | 0.34 | 0.32 | 0.32 |
| ncep_gfswave016 | J+6 | 5373 | 0.47 m | -0.32 | 0.47 | 0.47 | 0.48 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
37 heure(s) observee(s) dont 34 au-dessus du seuil ; colonnes lues : VAVH. Meilleur meteofrance_wave ; concordance avec le verdict : NON.

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 34 | 0.35 m | -0.31 |
| copernicus_houle | J+3 | 34 | 0.40 m | -0.26 |
| copernicus_houle | J+6 | 34 | 0.64 m | -0.44 |
| ecmwf_wam025 | J+1 | 34 | 0.30 m | -0.26 |
| ecmwf_wam025 | J+3 | 34 | 0.30 m | -0.25 |
| ecmwf_wam025 | J+6 | 34 | 0.52 m | -0.38 |
| meteofrance_wave | J+1 | 34 | 0.28 m | -0.24 |
| meteofrance_wave | J+3 | 34 | 0.33 m | -0.24 |
| meteofrance_wave | J+6 | 34 | 0.56 m | -0.39 |
| ncep_gfswave016 | J+1 | 34 | 0.40 m | -0.35 |
| ncep_gfswave016 | J+3 | 34 | 0.47 m | -0.24 |
| ncep_gfswave016 | J+6 | 34 | 0.75 m | -0.74 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 5073 heures observees dont **1672** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1594 | 0.45 m/s | -0.45 | 0.40 | 0.59 | 0.21 |
| copernicus_courant | J+3 | 1526 | 0.46 m/s | -0.46 | 0.41 | 0.60 | 0.22 |
| copernicus_courant | J+6 | 1417 | 0.45 m/s | -0.45 | 0.38 | 0.60 | 0.23 |
| meteofrance_currents | J+1 | 1594 | 0.41 m/s | -0.41 | 0.36 | 0.54 | 0.20 |
| meteofrance_currents | J+3 | 1526 | 0.42 m/s | -0.42 | 0.36 | 0.55 | 0.22 |
| meteofrance_currents | J+6 | 1395 | 0.43 m/s | -0.43 | 0.35 | 0.57 | 0.24 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
