# Etat du banc de fiabilite

Genere le 2026-09-23 par scripts/banc_hebdo.py. Chiffres lus dans data/banc/, jamais supposes.

Premier jour archive : **2026-09-17**. Jours ecoules depuis : **7**.

| source | jours | dernier | manquants depuis le debut |
|---|---|---|---|
| previsions (GFS, IFS, ICON-EU, ICON-2I, WAM, Meteo-France, GFS Wave, courants) | 7 | 2026-09-23 | aucun |
| previsions Copernicus MEDSEA (houle, courant) | 7 | 2026-09-23 | aucun |
| observations METAR Luqa (LMML) | 7 | 2026-09-23 | aucun |
| observations courants CALYPSO | 7 | 2026-09-23 | aucun |
| observations vagues CALYPSO | 0 | — | jamais archive |

## Regle d'arret
Au moins 28 jours de previsions archivees ET, par variable, au moins 30 h observees
au-dessus du seuil qui compte (vent > 25 km/h, houle > 0,5 m, courant > 0,25 m/s)
a chaque echeance J+1, J+3, J+6. Sinon on prolonge.

28 jours atteints au plus tot le **2026-10-14**.

## Dernier run
```
OK 2026-09-23T05:49Z · 0 probleme(s) · 1 manque(s) amont · derniere etape : fin
prevision gfs_seamless                 4536/4536 valeurs non vides
prevision ecmwf_ifs                    4536/4536 valeurs non vides
prevision icon_eu                      3267/4536 valeurs non vides
prevision italia_meteo_arpae_icon_2i   1971/4536 valeurs non vides
prevision ecmwf_wam025                 4536/4536 valeurs non vides
prevision meteofrance_wave             4536/4536 valeurs non vides
prevision ncep_gfswave016              4536/4536 valeurs non vides
prevision meteofrance_currents         3024/3024 valeurs non vides
-- etape previsions terminee a 11 s
observation LMML : HTTP 200, 94 lignes
-- etape LMML terminee a 13 s
jeux CALYPSO sur ERDDAP : EUHFR_NRTcurrent_HFR-CALYPSO-BARK_v3, EUHFR_NRTcurrent_HFR-CALYPSO-CENC_v3, EUHFR_NRTcurrent_HFR-CALYPSO-LAPS_v3, EUHFR_NRTcurrent_HFR-CALYPSO-LICA_v3, EUHFR_NRTcurrent_HFR-CALYPSO-MRAG_v3, EUHFR_NRTcurrent_HFR-CALYPSO-POZZ_v3, EUHFR_NRTcurrent_HFR-CALYPSO-SOPU_v3, EUHFR_NRTcurrent_HFR-CALYPSO-Total_v3
-- etape recherche CALYPSO terminee a 14 s
observation CALYPSO courant : 13824 lignes, 48 heures, 7789 lignes renseignees
-- etape CALYPSO courant terminee a 16 s
candidats vagues CALYPSO : aucun
MANQUE aucun jeu de vagues CALYPSO ouvert sur ERDDAP : arbitre de houle cherche chez Copernicus (banc_cmems.py)
-- etape fin terminee a 16 s
```

## Dernier run Copernicus
```
OK 2026-09-23T05:00Z
```

## Arbitre de houle
```
Recherche d'un arbitre de houle, 2026-09-23 05:00 UTC
Contexte : aucun jeu de vagues CALYPSO ouvert sur l'ERDDAP EuroGOOS (17/09).
inventaire du catalogue saute : rapport vieux de 0.0 jour(s), refait a 7 jours
altimetrie cmems_obs-wave_glo_phy-swh_nrt_al-l3_PT1S : 0 lignes sur la zone en 1 jours, colonnes de houle : aucune
  -> rien a archiver (aucune ligne ou aucune colonne de houle)
plateformes : get --index-parts code 0, 4 fichier(s) : index_history.txt, index_latest.txt, index_monthly.txt, index_platform.txt
  index_platform : 5079 plateforme(s) dans le produit, colonnes : platform_code, creation_date, update_date, wmo_platform_code, data_source, institution, institution_edmo_code, parameters, last_latitude_observation, last_longitude_observation, last_date_observation
  plateformes a moins de 100 km de Malte : 44
     6.8 km  61853            61853                  VHM0=non  derniere obs 2013-02-21T06:30:10Z  params= DEPH EWCT NSCT TEMP
     7.3 km  IDSL-Malta                              VHM0=non  derniere obs 2020-05-31T05:10:00Z  params= DEPH SLEV
     7.4 km  6204609          6204609                VHM0=non  derniere obs 2024-04-23T15:00:00Z  params= ATMS DEPH TEMP
     8.2 km  EXEC181A                                VHM0=non  derniere obs 1998-05-15T00:00:00Z  params= AMON CPHL DEPH DOXY NTRA NTRZ PHOS PHPH PSAL TEMP
```
