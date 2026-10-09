# Verdict du banc de fiabilite

Genere le 2026-10-09 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **23** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 576 heures observees dont **7** au-dessus du seuil.
**En attente** : 28 jours non atteints (23/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 7 | 9.48 km/h | -9.48 | — | 9.48 | — |
| ecmwf_ifs | J+3 | 6 | 7.44 km/h | -7.44 | — | 7.44 | — |
| ecmwf_ifs | J+6 | 6 | 12.29 km/h | -12.29 | — | 12.29 | — |
| gfs_seamless | J+1 | 7 | 4.66 km/h | -1.75 | — | 4.66 | — |
| gfs_seamless | J+3 | 6 | 11.04 km/h | -11.04 | — | 11.04 | — |
| gfs_seamless | J+6 | 6 | 12.70 km/h | -12.70 | — | 12.70 | — |
| icon_eu | J+1 | 7 | 11.64 km/h | -11.64 | — | 11.64 | — |
| icon_eu | J+3 | 6 | 12.55 km/h | -12.55 | — | 12.55 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 7 | 11.55 km/h | -11.55 | — | 11.55 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
**Aucun arbitre** : aucune observation de houle dans l'archive. Aucun score n'est calcule, aucun modele n'est designe.
Voir data/banc/arbitre-houle.txt.

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 2472 heures observees dont **765** au-dessus du seuil.
**En attente** : 28 jours non atteints (23/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 687 | 0.48 m/s | -0.48 | 0.44 | 0.59 | 0.19 |
| copernicus_courant | J+3 | 619 | 0.49 m/s | -0.49 | 0.45 | 0.61 | 0.18 |
| copernicus_courant | J+6 | 510 | 0.47 m/s | -0.47 | 0.41 | 0.62 | 0.18 |
| meteofrance_currents | J+1 | 687 | 0.45 m/s | -0.45 | 0.41 | 0.55 | 0.23 |
| meteofrance_currents | J+3 | 619 | 0.46 m/s | -0.46 | 0.40 | 0.57 | 0.24 |
| meteofrance_currents | J+6 | 510 | 0.45 m/s | -0.45 | 0.38 | 0.57 | 0.23 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
