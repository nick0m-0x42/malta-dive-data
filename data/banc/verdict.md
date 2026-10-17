# Verdict du banc de fiabilite

Genere le 2026-10-17 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **31** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 764 heures observees dont **43** au-dessus du seuil.
**Verdict : gfs_seamless** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 43 | 6.50 km/h | -6.50 | — | 6.50 | — |
| ecmwf_ifs | J+3 | 42 | 8.73 km/h | -8.70 | — | 8.73 | — |
| ecmwf_ifs | J+6 | 42 | 13.50 km/h | -13.50 | — | 13.50 | — |
| gfs_seamless | J+1 | 43 | 3.71 km/h | -1.25 | — | 3.71 | — |
| gfs_seamless | J+3 | 42 | 6.41 km/h | -3.88 | — | 6.41 | — |
| gfs_seamless | J+6 | 42 | 10.13 km/h | -9.95 | — | 10.13 | — |
| icon_eu | J+1 | 43 | 12.25 km/h | -12.25 | — | 12.25 | — |
| icon_eu | J+3 | 42 | 13.65 km/h | -13.65 | — | 13.65 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 43 | 11.35 km/h | -11.35 | — | 11.35 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
Arbitre : analyse Copernicus MEDSEA cmems_mod_med_wav_anfc_4.2km_PT1H-i, jours passes, aux 8 points (assimile l'altimetrie, vents ECMWF : independance partielle ; copernicus_houle score pour information, non designable), 5568 heures observees dont **2966** au-dessus du seuil.
**Verdict : ecmwf_wam025** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_houle | J+1 | 2835 | 0.11 m | -0.01 | 0.12 | 0.11 | 0.10 |
| copernicus_houle | J+3 | 2817 | 0.19 m | -0.10 | 0.19 | 0.19 | 0.20 |
| copernicus_houle | J+6 | 2770 | 0.35 m | -0.26 | 0.35 | 0.32 | 0.38 |
| ecmwf_wam025 | J+1 | 2835 | 0.19 m | -0.04 | 0.23 | 0.18 | 0.16 |
| ecmwf_wam025 | J+3 | 2817 | 0.22 m | -0.08 | 0.26 | 0.19 | 0.18 |
| ecmwf_wam025 | J+6 | 2770 | 0.35 m | -0.27 | 0.38 | 0.34 | 0.32 |
| meteofrance_wave | J+1 | 2835 | 0.20 m | -0.10 | 0.23 | 0.19 | 0.16 |
| meteofrance_wave | J+3 | 2817 | 0.26 m | -0.17 | 0.30 | 0.25 | 0.23 |
| meteofrance_wave | J+6 | 2770 | 0.36 m | -0.32 | 0.39 | 0.34 | 0.35 |
| ncep_gfswave016 | J+1 | 2835 | 0.21 m | -0.13 | 0.20 | 0.20 | 0.23 |
| ncep_gfswave016 | J+3 | 2817 | 0.33 m | -0.24 | 0.37 | 0.32 | 0.30 |
| ncep_gfswave016 | J+6 | 2770 | 0.45 m | -0.41 | 0.46 | 0.48 | 0.42 |

Au seuil 0.8 m (publie, ne pese pas) : meilleur ecmwf_wam025.

### Controle independant : altimetrie satellite (< 25 km d'un point)
0 heure(s) observee(s) dont 0 au-dessus du seuil ; colonnes lues : aucune. Aucune observation d'altimetrie a moins de 25 km des points.

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 3342 heures observees dont **1007** au-dessus du seuil.
**Verdict : meteofrance_currents** (28 jours et 30 h atteints).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 929 | 0.47 m/s | -0.47 | 0.43 | 0.59 | 0.18 |
| copernicus_courant | J+3 | 861 | 0.48 m/s | -0.48 | 0.44 | 0.61 | 0.19 |
| copernicus_courant | J+6 | 752 | 0.46 m/s | -0.46 | 0.40 | 0.60 | 0.18 |
| meteofrance_currents | J+1 | 929 | 0.44 m/s | -0.43 | 0.40 | 0.53 | 0.20 |
| meteofrance_currents | J+3 | 861 | 0.44 m/s | -0.44 | 0.40 | 0.54 | 0.20 |
| meteofrance_currents | J+6 | 752 | 0.44 m/s | -0.44 | 0.38 | 0.55 | 0.21 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
