# Etat du banc de fiabilite

Genere le 2026-10-21 par scripts/banc_hebdo.py. Chiffres lus dans data/banc/, jamais supposes.

Premier jour archive : **2026-09-17**. Jours ecoules depuis : **35**.

| source | jours | dernier | manquants depuis le debut |
|---|---|---|---|
| previsions (GFS, IFS, ICON-EU, ICON-2I, WAM, Meteo-France, GFS Wave, courants) | 35 | 2026-10-21 | aucun |
| previsions Copernicus MEDSEA (houle, courant) | 35 | 2026-10-21 | aucun |
| observations METAR Luqa (LMML) | 35 | 2026-10-21 | aucun |
| observations courants CALYPSO | 35 | 2026-10-21 | aucun |
| observations vagues CALYPSO | 0 | — | jamais archive |

## Regle d'arret
Au moins 28 jours de previsions archivees ET, par variable, au moins 30 h observees
au-dessus du seuil qui compte (vent > 25 km/h, houle > 0,5 m, courant > 0,25 m/s)
a chaque echeance J+1, J+3, J+6. Sinon on prolonge.

28 jours atteints au plus tot le **2026-10-14** (atteint).

## Dernier run
```
OK 2026-10-21T10:34Z · 0 probleme(s) · 1 manque(s) amont · derniere etape : fin
prevision gfs_seamless                 4536/4536 valeurs non vides
prevision ecmwf_ifs                    4536/4536 valeurs non vides
prevision icon_eu                      3429/4536 valeurs non vides
prevision italia_meteo_arpae_icon_2i   1971/4536 valeurs non vides
prevision ecmwf_wam025                 4536/4536 valeurs non vides
prevision meteofrance_wave             4536/4536 valeurs non vides
prevision ncep_gfswave016              4536/4536 valeurs non vides
prevision meteofrance_currents         3024/3024 valeurs non vides
-- etape previsions terminee a 15 s
observation LMML : HTTP 200, 96 lignes
-- etape LMML terminee a 16 s
jeux CALYPSO sur ERDDAP : EUHFR_NRTcurrent_HFR-CALYPSO-BARK_v3, EUHFR_NRTcurrent_HFR-CALYPSO-CENC_v3, EUHFR_NRTcurrent_HFR-CALYPSO-LAPS_v3, EUHFR_NRTcurrent_HFR-CALYPSO-LICA_v3, EUHFR_NRTcurrent_HFR-CALYPSO-MRAG_v3, EUHFR_NRTcurrent_HFR-CALYPSO-POZZ_v3, EUHFR_NRTcurrent_HFR-CALYPSO-SOPU_v3, EUHFR_NRTcurrent_HFR-CALYPSO-Total_v3
-- etape recherche CALYPSO terminee a 17 s
observation CALYPSO courant : 13824 lignes, 48 heures, 8164 lignes renseignees
-- etape CALYPSO courant terminee a 19 s
candidats vagues CALYPSO : aucun
MANQUE aucun jeu de vagues CALYPSO ouvert sur ERDDAP : arbitre de houle cherche chez Copernicus (banc_cmems.py)
-- etape fin terminee a 19 s
```

## Dernier run Copernicus
```
OK 2026-10-21T10:00Z
```

## Arbitre de houle
```
Recherche d'un arbitre de houle, 2026-10-21 10:00 UTC
Contexte : aucun jeu de vagues CALYPSO ouvert sur l'ERDDAP EuroGOOS (17/09).
inventaire du catalogue saute : rapport vieux de 0.0 jour(s), refait a 7 jours
  al   cmems_obs-wave_glo_phy-swh_nrt_al-l3_PT1S : 0 ligne(s)
  c2   cmems_obs-wave_glo_phy-swh_nrt_c2-l3_PT1S : 66 ligne(s)
  cfo  cmems_obs-wave_glo_phy-swh_nrt_cfo-l3_PT1S : 66 ligne(s)
  h2b  cmems_obs-wave_glo_phy-swh_nrt_h2b-l3_PT1S : 63 ligne(s)
  h2c  cmems_obs-wave_glo_phy-swh_nrt_h2c-l3_PT1S : ECHEC CoordinatesOutOfDatasetBounds('Some of your subset selection [2026-10-14 10:00:00+00:00, 2026-10-21 10:00:00+00:00] for 
  j3   cmems_obs-wave_glo_phy-swh_nrt_j3-l3_PT1S : 159 ligne(s)
  s3a  cmems_obs-wave_glo_phy-swh_nrt_s3a-l3_PT1S : 48 ligne(s)
  s3b  cmems_obs-wave_glo_phy-swh_nrt_s3b-l3_PT1S : 0 ligne(s)
  s6a  cmems_obs-wave_glo_phy-swh_nrt_s6a-l3_PT1S : 48 ligne(s)
```
