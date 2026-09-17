# Etat du banc de fiabilite

Genere le 2026-09-17 par scripts/banc_hebdo.py. Chiffres lus dans data/banc/, jamais supposes.

Premier jour archive : **2026-09-17**. Jours ecoules depuis : **1**.

| source | jours | dernier | manquants depuis le debut |
|---|---|---|---|
| previsions (GFS, IFS, ICON-EU, ICON-2I, WAM, Meteo-France, GFS Wave, courants) | 1 | 2026-09-17 | aucun |
| previsions Copernicus MEDSEA (houle, courant) | 1 | 2026-09-17 | aucun |
| observations METAR Luqa (LMML) | 1 | 2026-09-17 | aucun |
| observations courants CALYPSO | 1 | 2026-09-17 | aucun |
| observations vagues CALYPSO | 0 | — | jamais archive |

## Regle d'arret
Au moins 28 jours de previsions archivees ET, par variable, au moins 30 h observees
au-dessus du seuil qui compte (vent > 25 km/h, houle > 0,5 m, courant > 0,25 m/s)
a chaque echeance J+1, J+3, J+6. Sinon on prolonge.

28 jours atteints au plus tot le **2026-10-14**.

## Dernier run
```
ECHEC 2026-09-17T18:28Z · 1 probleme(s) · derniere etape : fin
prevision gfs_seamless                 4536/4536 valeurs non vides
prevision ecmwf_ifs                    4536/4536 valeurs non vides
prevision icon_eu                      3591/4536 valeurs non vides
prevision italia_meteo_arpae_icon_2i   2295/4536 valeurs non vides
prevision ecmwf_wam025                 4536/4536 valeurs non vides
prevision meteofrance_wave             4536/4536 valeurs non vides
prevision ncep_gfswave016              4536/4536 valeurs non vides
prevision meteofrance_currents         3024/3024 valeurs non vides
-- etape previsions terminee a 15 s
observation LMML : HTTP 200, 96 lignes
-- etape LMML terminee a 17 s
jeux CALYPSO sur ERDDAP : EUHFR_NRTcurrent_HFR-CALYPSO-BARK_v3, EUHFR_NRTcurrent_HFR-CALYPSO-CENC_v3, EUHFR_NRTcurrent_HFR-CALYPSO-LAPS_v3, EUHFR_NRTcurrent_HFR-CALYPSO-LICA_v3, EUHFR_NRTcurrent_HFR-CALYPSO-MRAG_v3, EUHFR_NRTcurrent_HFR-CALYPSO-POZZ_v3, EUHFR_NRTcurrent_HFR-CALYPSO-SOPU_v3, EUHFR_NRTcurrent_HFR-CALYPSO-Total_v3
-- etape recherche CALYPSO terminee a 18 s
observation CALYPSO courant : 13824 lignes, 48 heures, 7588 lignes renseignees
-- etape CALYPSO courant terminee a 21 s
candidats vagues CALYPSO : aucun
PROBLEME aucun jeu de vagues CALYPSO ouvert trouve sur ERDDAP (a chercher ailleurs)
-- etape fin terminee a 21 s
```

## Dernier run Copernicus
```
OK 2026-09-17T18:00Z
```

## Arbitre de houle
```
Recherche d'un arbitre de houle, 2026-09-17 18:00 UTC
Contexte : aucun jeu de vagues CALYPSO ouvert sur l'ERDDAP EuroGOOS (17/09).
WAVE_GLO_PHY_SWH (altimetrie satellite, hauteur significative le long des traces) : 27 jeux
  - cci_obs-wave_glo_phy-swh_my_l3_PT1S-i
  - cmems_obs-wave_glo_phy-swh_my_multi-l4-0.5deg_P1D-i
  - cmems_obs-wave_glo_phy-swh_my_multi-l4-2deg_P1D-m
  - cmems_obs-wave_glo_phy-swh_nrt_al-l3-1km_PT0.2S-i
  - cmems_obs-wave_glo_phy-swh_nrt_al-l3_PT1S
  - cmems_obs-wave_glo_phy-swh_nrt_c2-l3-1km_PT0.2S-i
  - cmems_obs-wave_glo_phy-swh_nrt_c2-l3_PT1S
  - cmems_obs-wave_glo_phy-swh_nrt_cfo-l3-1km_PT0.2S-i
  - cmems_obs-wave_glo_phy-swh_nrt_cfo-l3_PT1S
```
