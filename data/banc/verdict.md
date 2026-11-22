# Verdict du banc de fiabilite

Genere le 2026-11-22 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **67** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 1593 heures observees dont **158** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 158 | 6.23 km/h | -4.88 | — | 6.23 | — |
| ecmwf_ifs | J+3 | 157 | 7.74 km/h | -7.54 | — | 7.74 | — |
| ecmwf_ifs | J+6 | 157 | 13.18 km/h | -13.05 | — | 13.18 | — |
| gfs_seamless | J+1 | 158 | 5.02 km/h | +2.00 | — | 5.02 | — |
| gfs_seamless | J+3 | 157 | 5.73 km/h | +0.55 | — | 5.73 | — |
| gfs_seamless | J+6 | 157 | 11.00 km/h | -10.29 | — | 11.00 | — |
| icon_eu | J+1 | 158 | 11.41 km/h | -11.40 | — | 11.41 | — |
| icon_eu | J+3 | 157 | 13.38 km/h | -13.38 | — | 13.38 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 158 | 11.68 km/h | -11.68 | — | 11.68 | — |
| italia_meteo_arpae_icon_2i | J+3 | 6 | 18.23 km/h | -18.23 | — | 18.23 | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 12480 heures observees dont **7767** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 7636 | 0.11 m | -0.00 | 0.12 | 0.11 | 0.11 |
| copernicus_houle | J+3 | 7618 | 0.17 m | -0.06 | 0.18 | 0.16 | 0.18 |
| copernicus_houle | J+6 | 7571 | 0.39 m | -0.17 | 0.38 | 0.34 | 0.42 |
| ecmwf_wam025 | J+1 | 7636 | 0.19 m | -0.01 | 0.22 | 0.19 | 0.16 |
| ecmwf_wam025 | J+3 | 7618 | 0.22 m | -0.07 | 0.24 | 0.21 | 0.20 |
| ecmwf_wam025 | J+6 | 7571 | 0.39 m | -0.17 | 0.41 | 0.35 | 0.40 |
| meteofrance_wave | J+1 | 7636 | 0.20 m | -0.05 | 0.21 | 0.21 | 0.17 |
| meteofrance_wave | J+3 | 7618 | 0.24 m | -0.10 | 0.25 | 0.25 | 0.22 |
| meteofrance_wave | J+6 | 7571 | 0.40 m | -0.19 | 0.41 | 0.37 | 0.43 |
| ncep_gfswave016 | J+1 | 7636 | 0.22 m | -0.06 | 0.21 | 0.22 | 0.23 |
| ncep_gfswave016 | J+3 | 7618 | 0.30 m | -0.13 | 0.30 | 0.29 | 0.30 |
| ncep_gfswave016 | J+6 | 7571 | 0.45 m | -0.28 | 0.46 | 0.43 | 0.47 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
61 heure(s) observee(s) dont 57 au-dessus du seuil ; colonnes lues : VAVH. Meilleur ecmwf_wam025 ; concordance avec le verdict : OUI.

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 57 | 0.30 m | -0.24 |
| copernicus_houle | J+3 | 57 | 0.34 m | -0.23 |
| copernicus_houle | J+6 | 57 | 0.50 m | -0.33 |
| ecmwf_wam025 | J+1 | 57 | 0.26 m | -0.23 |
| ecmwf_wam025 | J+3 | 57 | 0.27 m | -0.24 |
| ecmwf_wam025 | J+6 | 57 | 0.44 m | -0.24 |
| meteofrance_wave | J+1 | 57 | 0.25 m | -0.21 |
| meteofrance_wave | J+3 | 57 | 0.28 m | -0.22 |
| meteofrance_wave | J+6 | 57 | 0.50 m | -0.24 |
| ncep_gfswave016 | J+1 | 57 | 0.34 m | -0.28 |
| ncep_gfswave016 | J+3 | 57 | 0.42 m | -0.26 |
| ncep_gfswave016 | J+6 | 57 | 0.56 m | -0.49 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 6091 heures observees dont **1967** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1889 | 0.45 m/s | -0.45 | 0.38 | 0.59 | 0.25 |
| copernicus_courant | J+3 | 1821 | 0.46 m/s | -0.46 | 0.39 | 0.61 | 0.26 |
| copernicus_courant | J+6 | 1712 | 0.45 m/s | -0.45 | 0.37 | 0.61 | 0.25 |
| meteofrance_currents | J+1 | 1889 | 0.41 m/s | -0.41 | 0.34 | 0.55 | 0.24 |
| meteofrance_currents | J+3 | 1821 | 0.42 m/s | -0.42 | 0.34 | 0.56 | 0.26 |
| meteofrance_currents | J+6 | 1690 | 0.43 m/s | -0.43 | 0.34 | 0.58 | 0.28 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
