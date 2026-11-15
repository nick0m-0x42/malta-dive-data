# Verdict du banc de fiabilite

Genere le 2026-11-15 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **60** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 1447 heures observees dont **147** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 147 | 6.19 km/h | -4.73 | — | 6.19 | — |
| ecmwf_ifs | J+3 | 146 | 7.61 km/h | -7.40 | — | 7.61 | — |
| ecmwf_ifs | J+6 | 146 | 13.36 km/h | -13.21 | — | 13.36 | — |
| gfs_seamless | J+1 | 147 | 5.05 km/h | +1.81 | — | 5.05 | — |
| gfs_seamless | J+3 | 146 | 5.90 km/h | +0.40 | — | 5.90 | — |
| gfs_seamless | J+6 | 146 | 10.98 km/h | -10.43 | — | 10.98 | — |
| icon_eu | J+1 | 147 | 11.45 km/h | -11.45 | — | 11.45 | — |
| icon_eu | J+3 | 146 | 13.41 km/h | -13.41 | — | 13.41 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 147 | 11.58 km/h | -11.58 | — | 11.58 | — |
| italia_meteo_arpae_icon_2i | J+3 | 1 | 14.83 km/h | -14.83 | — | 14.83 | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 11136 heures observees dont **6861** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 6730 | 0.11 m | -0.02 | 0.12 | 0.11 | 0.11 |
| copernicus_houle | J+3 | 6712 | 0.18 m | -0.07 | 0.18 | 0.17 | 0.20 |
| copernicus_houle | J+6 | 6665 | 0.40 m | -0.22 | 0.39 | 0.35 | 0.46 |
| ecmwf_wam025 | J+1 | 6730 | 0.20 m | -0.01 | 0.22 | 0.19 | 0.17 |
| ecmwf_wam025 | J+3 | 6712 | 0.23 m | -0.08 | 0.24 | 0.21 | 0.22 |
| ecmwf_wam025 | J+6 | 6665 | 0.40 m | -0.21 | 0.42 | 0.35 | 0.43 |
| meteofrance_wave | J+1 | 6730 | 0.20 m | -0.06 | 0.22 | 0.21 | 0.18 |
| meteofrance_wave | J+3 | 6712 | 0.25 m | -0.11 | 0.26 | 0.26 | 0.24 |
| meteofrance_wave | J+6 | 6665 | 0.41 m | -0.25 | 0.42 | 0.37 | 0.44 |
| ncep_gfswave016 | J+1 | 6730 | 0.22 m | -0.07 | 0.21 | 0.22 | 0.24 |
| ncep_gfswave016 | J+3 | 6712 | 0.31 m | -0.14 | 0.32 | 0.30 | 0.32 |
| ncep_gfswave016 | J+6 | 6665 | 0.47 m | -0.30 | 0.47 | 0.44 | 0.50 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
48 heure(s) observee(s) dont 44 au-dessus du seuil ; colonnes lues : VAVH. Meilleur meteofrance_wave ; concordance avec le verdict : NON.

| modele | echeance | heures | MAE | biais |
|---|---|---|---|---|
| copernicus_houle | J+1 | 44 | 0.33 m | -0.29 |
| copernicus_houle | J+3 | 44 | 0.37 m | -0.25 |
| copernicus_houle | J+6 | 44 | 0.58 m | -0.42 |
| ecmwf_wam025 | J+1 | 44 | 0.29 m | -0.26 |
| ecmwf_wam025 | J+3 | 44 | 0.32 m | -0.27 |
| ecmwf_wam025 | J+6 | 44 | 0.46 m | -0.34 |
| meteofrance_wave | J+1 | 44 | 0.28 m | -0.25 |
| meteofrance_wave | J+3 | 44 | 0.33 m | -0.26 |
| meteofrance_wave | J+6 | 44 | 0.50 m | -0.35 |
| ncep_gfswave016 | J+1 | 44 | 0.39 m | -0.34 |
| ncep_gfswave016 | J+3 | 44 | 0.44 m | -0.25 |
| ncep_gfswave016 | J+6 | 44 | 0.65 m | -0.61 |

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 5885 heures observees dont **1912** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 1834 | 0.44 m/s | -0.44 | 0.39 | 0.59 | 0.23 |
| copernicus_courant | J+3 | 1766 | 0.45 m/s | -0.45 | 0.39 | 0.60 | 0.24 |
| copernicus_courant | J+6 | 1657 | 0.44 m/s | -0.44 | 0.37 | 0.60 | 0.23 |
| meteofrance_currents | J+1 | 1834 | 0.41 m/s | -0.41 | 0.35 | 0.54 | 0.22 |
| meteofrance_currents | J+3 | 1766 | 0.42 m/s | -0.42 | 0.35 | 0.56 | 0.24 |
| meteofrance_currents | J+6 | 1635 | 0.43 m/s | -0.43 | 0.34 | 0.57 | 0.26 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
