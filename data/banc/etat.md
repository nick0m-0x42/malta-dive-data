# Etat du banc de fiabilite

Genere le 2026-09-19 par scripts/banc_hebdo.py. Chiffres lus dans data/banc/, jamais supposes.

Premier jour archive : **2026-09-17**. Jours ecoules depuis : **3**.

| source | jours | dernier | manquants depuis le debut |
|---|---|---|---|
| previsions (GFS, IFS, ICON-EU, ICON-2I, WAM, Meteo-France, GFS Wave, courants) | 3 | 2026-09-19 | aucun |
| previsions Copernicus MEDSEA (houle, courant) | 3 | 2026-09-19 | aucun |
| observations METAR Luqa (LMML) | 3 | 2026-09-19 | aucun |
| observations courants CALYPSO | 3 | 2026-09-19 | aucun |
| observations vagues CALYPSO | 0 | — | jamais archive |

## Regle d'arret
Au moins 28 jours de previsions archivees ET, par variable, au moins 30 h observees
au-dessus du seuil qui compte (vent > 25 km/h, houle > 0,5 m, courant > 0,25 m/s)
a chaque echeance J+1, J+3, J+6. Sinon on prolonge.

28 jours atteints au plus tot le **2026-10-14**.

## Dernier run
```
OK 2026-09-19T05:47Z · 0 probleme(s) · 1 manque(s) amont · derniere etape : fin
prevision gfs_seamless                 4536/4536 valeurs non vides
prevision ecmwf_ifs                    4536/4536 valeurs non vides
prevision icon_eu                      3267/4536 valeurs non vides
prevision italia_meteo_arpae_icon_2i   1971/4536 valeurs non vides
prevision ecmwf_wam025                 4536/4536 valeurs non vides
prevision meteofrance_wave             4536/4536 valeurs non vides
prevision ncep_gfswave016              4536/4536 valeurs non vides
prevision meteofrance_currents         3024/3024 valeurs non vides
-- etape previsions terminee a 15 s
observation LMML : HTTP 200, 96 lignes
-- etape LMML terminee a 16 s
jeux CALYPSO sur ERDDAP : EUHFR_NRTcurrent_HFR-CALYPSO-BARK_v3, EUHFR_NRTcurrent_HFR-CALYPSO-CENC_v3, EUHFR_NRTcurrent_HFR-CALYPSO-LAPS_v3, EUHFR_NRTcurrent_HFR-CALYPSO-LICA_v3, EUHFR_NRTcurrent_HFR-CALYPSO-MRAG_v3, EUHFR_NRTcurrent_HFR-CALYPSO-POZZ_v3, EUHFR_NRTcurrent_HFR-CALYPSO-SOPU_v3, EUHFR_NRTcurrent_HFR-CALYPSO-Total_v3
-- etape recherche CALYPSO terminee a 18 s
observation CALYPSO courant : 13824 lignes, 48 heures, 7165 lignes renseignees
-- etape CALYPSO courant terminee a 21 s
candidats vagues CALYPSO : aucun
MANQUE aucun jeu de vagues CALYPSO ouvert sur ERDDAP : arbitre de houle cherche chez Copernicus (banc_cmems.py)
-- etape fin terminee a 21 s
```

## Dernier run Copernicus
```
OK 2026-09-19T05:00Z
```

## Arbitre de houle
```
Recherche d'un arbitre de houle, 2026-09-19 05:00 UTC
Contexte : aucun jeu de vagues CALYPSO ouvert sur l'ERDDAP EuroGOOS (17/09).
inventaire du catalogue saute : rapport vieux de 0.0 jour(s), refait a 7 jours
altimetrie cmems_obs-wave_glo_phy-swh_nrt_al-l3_PT1S : 0 lignes sur la zone en 1 jours, colonnes de houle : aucune
  -> rien a archiver (aucune ligne ou aucune colonne de houle)
```
