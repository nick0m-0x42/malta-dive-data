# Verdict du banc de fiabilite

Genere le 2026-10-12 par scripts/banc_verdict.py. Chiffres lus dans data/banc/, jamais supposes.

Archive depuis le **2026-09-17** : **26** jour(s) d'emissions. 28 jours le **2026-10-14**, borne des 45 jours le **2026-10-31**.
Seuils « ca compte » : vent > 25 km/h, houle > 0.5 m (et 0.8 m publie a cote), courant > 0.25 m/s.
Echeances : J+1, J+3, J+6. Il faut 30 h qualifiantes par echeance.

## Vent
Arbitre : LMML (METAR), 648 heures observees dont **22** au-dessus du seuil.
**En attente** : 28 jours non atteints (26/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| ecmwf_ifs | J+1 | 22 | 8.41 km/h | -8.41 | — | 8.41 | — |
| ecmwf_ifs | J+3 | 21 | 8.17 km/h | -8.17 | — | 8.17 | — |
| ecmwf_ifs | J+6 | 21 | 16.73 km/h | -16.73 | — | 16.73 | — |
| gfs_seamless | J+1 | 22 | 4.16 km/h | -1.35 | — | 4.16 | — |
| gfs_seamless | J+3 | 21 | 5.54 km/h | -0.80 | — | 5.54 | — |
| gfs_seamless | J+6 | 21 | 7.69 km/h | -7.69 | — | 7.69 | — |
| icon_eu | J+1 | 22 | 13.14 km/h | -13.14 | — | 13.14 | — |
| icon_eu | J+3 | 21 | 12.20 km/h | -12.20 | — | 12.20 | — |
| icon_eu | J+6 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+1 | 22 | 11.81 km/h | -11.81 | — | 11.81 | — |
| italia_meteo_arpae_icon_2i | J+3 | 0 | — | — | — | — | — |
| italia_meteo_arpae_icon_2i | J+6 | 0 | — | — | — | — | — |

## Houle
**Aucun arbitre** : aucune observation de houle dans l'archive. Aucun score n'est calcule, aucun modele n'est designe.
Voir data/banc/arbitre-houle.txt.

## Courant
Arbitre : CALYPSO radar HF, mailles a E-Delimara 0.8 km, N-Comino 1.2 km, N-Gozo 1.2 km, N-Qawra 1.4 km, N-Valletta 0.9 km, S-Gozo 1.1 km, S-Lapsi 1.9 km, S-Zurrieq 1.2 km, 2753 heures observees dont **851** au-dessus du seuil.
**En attente** : 28 jours non atteints (26/28).

| modele | echeance | heures | MAE | biais | nord | est | sud |
|---|---|---|---|---|---|---|---|
| copernicus_courant | J+1 | 773 | 0.48 m/s | -0.48 | 0.44 | 0.58 | 0.18 |
| copernicus_courant | J+3 | 705 | 0.49 m/s | -0.49 | 0.45 | 0.59 | 0.19 |
| copernicus_courant | J+6 | 596 | 0.46 m/s | -0.46 | 0.41 | 0.59 | 0.18 |
| meteofrance_currents | J+1 | 773 | 0.44 m/s | -0.44 | 0.41 | 0.53 | 0.22 |
| meteofrance_currents | J+3 | 705 | 0.45 m/s | -0.45 | 0.40 | 0.54 | 0.23 |
| meteofrance_currents | J+6 | 596 | 0.44 m/s | -0.44 | 0.38 | 0.54 | 0.23 |

## Lecture
Le verdict designe un modele par variable pour tout l'archipel ; les colonnes nord, est, sud
donnent le MAE par facade, pour information. Un score ne dit rien sans son nombre d'heures.
Ce fichier est reecrit chaque jour ; METHODE.md de l'atlas reprend le verdict une fois par mois.
