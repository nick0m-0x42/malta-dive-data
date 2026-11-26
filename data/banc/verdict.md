# Verdict du banc de fiabilite

Genere le 2026-11-26 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **71** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 1689 heures observees dont **181** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 181 | 5.84 km/h | -4.33 | — | 5.84 | — |
| ecmwf_ifs | J+3 | 180 | 7.16 km/h | -6.79 | — | 7.16 | — |
| ecmwf_ifs | J+6 | 180 | 12.71 km/h | -12.59 | — | 12.71 | — |
| gfs_seamless | J+1 | 181 | 5.30 km/h | +2.66 | — | 5.30 | — |
| gfs_seamless | J+3 | 180 | 5.83 km/h | +1.15 | — | 5.83 | — |
| gfs_seamless | J+6 | 180 | 10.19 km/h | -9.54 | — | 10.19 | — |
| icon_eu | J+1 | 181 | 11.29 km/h | -11.29 | — | 11.29 | — |
| icon_eu | J+3 | 180 | 12.90 km/h | -12.90 | — | 12.90 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 181 | 11.69 km/h | -11.69 | — | 11.69 | — |
| italia_meteo_arpae_icon_2i | J+3 | 6 | 18.23 km/h | -18.23 | — | 18.23 | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 13248 heures observees dont **8452** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 8321 | 0.11 m | +0.00 | 0.12 | 0.10 | 0.11 |
| copernicus_houle | J+3 | 8303 | 0.17 m | -0.06 | 0.18 | 0.16 | 0.18 |
| copernicus_houle | J+6 | 8256 | 0.40 m | -0.19 | 0.40 | 0.35 | 0.43 |
| ecmwf_wam025 | J+1 | 8321 | 0.19 m | -0.01 | 0.22 | 0.19 | 0.15 |
| ecmwf_wam025 | J+3 | 8303 | 0.22 m | -0.06 | 0.24 | 0.21 | 0.20 |
| ecmwf_wam025 | J+6 | 8256 | 0.39 m | -0.18 | 0.42 | 0.35 | 0.40 |
| meteofrance_wave | J+1 | 8321 | 0.20 m | -0.04 | 0.20 | 0.21 | 0.17 |
| meteofrance_wave | J+3 | 8303 | 0.24 m | -0.09 | 0.24 | 0.25 | 0.22 |
| meteofrance_wave | J+6 | 8256 | 0.41 m | -0.21 | 0.43 | 0.37 | 0.43 |
| ncep_gfswave016 | J+1 | 8321 | 0.22 m | -0.06 | 0.20 | 0.22 | 0.23 |
| ncep_gfswave016 | J+3 | 8303 | 0.29 m | -0.12 | 0.29 | 0.30 | 0.30 |
| ncep_gfswave016 | J+6 | 8256 | 0.46 m | -0.28 | 0.47 | 0.44 | 0.47 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
64 heure(s) observee(s) dont 60 au-dessus du seuil ; colonnes lues : VAVH. Meilleur ecmwf_wam025 ; concordance avec le verdict : OUI.

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 60 | 0.30 m | -0.23 |
| copernicus_houle | J+3 | 60 | 0.33 m | -0.22 |
| copernicus_houle | J+6 | 60 | 0.50 m | -0.34 |
| ecmwf_wam025 | J+1 | 60 | 0.25 m | -0.21 |
| ecmwf_wam025 | J+3 | 60 | 0.27 m | -0.22 |
| ecmwf_wam025 | J+6 | 60 | 0.44 m | -0.25 |
| meteofrance_wave | J+1 | 60 | 0.26 m | -0.20 |
| meteofrance_wave | J+3 | 60 | 0.29 m | -0.20 |
| meteofrance_wave | J+6 | 60 | 0.50 m | -0.25 |
| ncep_gfswave016 | J+1 | 60 | 0.33 m | -0.28 |
| ncep_gfswave016 | J+3 | 60 | 0.41 m | -0.25 |
| ncep_gfswave016 | J+6 | 60 | 0.57 m | -0.50 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 6257 heures observees dont **2018** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1940 | 0.45 m/s | -0.45 | 0.38 | 0.59 | 0.26 |
| copernicus_courant | J+3 | 1872 | 0.46 m/s | -0.46 | 0.38 | 0.61 | 0.27 |
| copernicus_courant | J+6 | 1763 | 0.45 m/s | -0.45 | 0.36 | 0.61 | 0.27 |
| meteofrance_currents | J+1 | 1940 | 0.41 m/s | -0.41 | 0.33 | 0.55 | 0.26 |
| meteofrance_currents | J+3 | 1872 | 0.42 m/s | -0.42 | 0.33 | 0.57 | 0.27 |
| meteofrance_currents | J+6 | 1741 | 0.43 m/s | -0.43 | 0.33 | 0.58 | 0.29 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
