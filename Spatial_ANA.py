import geopandas as gpd
import pandas as pd
import os
import matplotlib.pyplot as plt
import pyproj
import numpy as np
import datetime
import math

pyproj.__version__  # (2.6.0)
gpd.__version__


# Get the UTM code
def convert_wgs_to_utm(lon, lat):
    utm_band = str((math.floor((lon + 180) / 6) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0' + utm_band
    if lat >= 0:
        epsg_code = '326' + utm_band  # lat>0: N;
    else:
        epsg_code = '327' + utm_band
    return epsg_code


os.chdir(r'C:\Users\Songhua Hu\Desktop\Transit\GIS')

# Read station
Station = gpd.read_file('StationRidership.shp')
# Get the utm code
utm_code = convert_wgs_to_utm(Station.geometry.bounds['minx'][0], Station.geometry.bounds['miny'][0])
# Project DTA 84 to utm
Station = Station.to_crs('EPSG:' + str(utm_code))

# Buffer the station
Buffer_S = Station.buffer(1000, cap_style=1).reset_index(drop=True).reset_index()
Buffer_S.columns = ['B_ID', 'geometry']
Buffer_S = gpd.GeoDataFrame(Buffer_S, geometry='geometry', crs='EPSG:4326')
Buffer_S = Buffer_S.to_crs('EPSG:' + str(utm_code))
Buffer_S['station_id'] = Station['station_id']
# Buffer_S.to_file('TransitBuffer.shp')

# Read BlockGroup
BlockGroup = gpd.read_file(r'BlockGroup.shp')
BlockGroup = BlockGroup.to_crs('EPSG:' + str(utm_code))
# SJOIN with BlockGroup
SInBG = gpd.sjoin(Station, BlockGroup, how='inner', op='within').reset_index(drop=True)
# DF_SInBG = pd.DataFrame(SInBG)

# Read ZIPCODE
ZIPCODE = gpd.read_file(r'ZIPCODEUS.shp')
ZIPCODE = ZIPCODE.to_crs('EPSG:' + str(utm_code))
# SJOIN with BlockGroup
SInZIP = gpd.sjoin(Station, ZIPCODE, how='inner', op='within').reset_index(drop=True)

# Read Landuse
Landuse = gpd.read_file(r'Landuse2013_CMAP.shp')
Landuse = Landuse.to_crs('EPSG:' + str(utm_code))
# INTERSECT with LANDUSE
SInLand = gpd.overlay(Landuse, Buffer_S, how='intersection')
SInLand['Area'] = SInLand['geometry'].area
SInLand_Area = SInLand.groupby(['station_id', 'LANDUSE']).sum()['Area'].reset_index()
SInLand_Area['Land_Use_F2'] = [var[0:2] for var in SInLand_Area['LANDUSE']]
SInLand_Area['Land_Use_F1'] = [var[0:1] for var in SInLand_Area['LANDUSE']]
# SInLand.to_file('SInLand.shp')
# set(SInLand_Area['LANDUSE'])
SInLand_Area['Land_Use_Des'] = np.nan
SInLand_Area.loc[SInLand_Area['Land_Use_F2'] == '11', 'Land_Use_Des'] = 'RESIDENTIAL'
SInLand_Area.loc[SInLand_Area['Land_Use_F2'] == '12', 'Land_Use_Des'] = 'COMMERCIAL'
SInLand_Area.loc[SInLand_Area['Land_Use_F2'] == '13', 'Land_Use_Des'] = 'INSTITUTIONAL'
SInLand_Area.loc[SInLand_Area['Land_Use_F2'] == '14', 'Land_Use_Des'] = 'INDUSTRIAL'
SInLand_Area.loc[SInLand_Area['Land_Use_F2'] == '15', 'Land_Use_Des'] = 'TCUW'
SInLand_Area.loc[SInLand_Area['Land_Use_F1'] == '3', 'Land_Use_Des'] = 'OPENSPACE'
SInLand_Area.loc[SInLand_Area['Land_Use_F1'].isin(['2', '4', '5', '6', '9']), 'Land_Use_Des'] = 'OTHERS'
SInLand_Area_New = SInLand_Area.groupby(['station_id', 'Land_Use_Des']).sum()['Area'].reset_index()

# Calculate the LUM
TAZ_LAND_USE_ALL = SInLand_Area.groupby(['station_id']).sum()['Area'].reset_index()
TAZ_LAND_USE_ALL.columns = ['station_id', 'ALL_AREA']
LandUse_Area1 = SInLand_Area_New.merge(TAZ_LAND_USE_ALL, on='station_id')
LandUse_Area1['Percen'] = LandUse_Area1['Area'] / LandUse_Area1['ALL_AREA']
LandUse_Area1['LogPercen'] = np.log(LandUse_Area1['Percen'])
LandUse_Area1['LogP*P'] = LandUse_Area1['Percen'] * LandUse_Area1['LogPercen']
LandUse_Area2 = LandUse_Area1.groupby(['station_id']).sum()['LogP*P'].reset_index()
LandUse_Area3 = SInLand_Area_New.groupby(['station_id']).count()['Land_Use_Des'].reset_index()
LandUse_Area3.columns = ['station_id', 'Count']
LandUse_Area2 = LandUse_Area2.merge(LandUse_Area3, on='station_id')
LandUse_Area2['LUM'] = LandUse_Area2['LogP*P'] * ((-1) / (np.log(LandUse_Area2['Count'])))
LUM = LandUse_Area2[['station_id', 'LUM']].fillna(0)
LandUse_Area_PCT = LandUse_Area1[['station_id', 'Land_Use_Des', 'Area', 'Percen']]
# plt.hist(LUM['LUM'])

# Read roads
Roads = gpd.read_file(r'ROAD.shp')
Roads = Roads.to_crs('EPSG:' + str(utm_code))
# INTERSECT with LANDUSE
SInRoad = gpd.clip(Roads, Buffer_S)
SInRoad1 = gpd.overlay(Roads, Buffer_S, how='intersection')
SInRoad1['Length'] = SInRoad1['geometry'].length
SInRoad_Length = SInRoad1.groupby(['station_id', 'fclass']).sum()['Length'].reset_index()
set(SInRoad_Length['fclass'])
Road_Length_With_Type = SInRoad_Length.pivot('station_id', 'fclass', 'Length').fillna(0).reset_index()
SInRoad_Length.groupby(['fclass']).sum()['Length'].plot.bar()

# SInRoad1.to_file('SInRoad_overlay.shp')
Road_Length_With_Type['Primary'] = Road_Length_With_Type['primary'] + Road_Length_With_Type['primary_link'] + \
                                   Road_Length_With_Type['tertiary'] + Road_Length_With_Type['tertiary_link']
Road_Length_With_Type['Secondary'] = Road_Length_With_Type['secondary'] + Road_Length_With_Type['secondary_link'] + \
                                     Road_Length_With_Type['residential']
Road_Length_With_Type['Minor'] = Road_Length_With_Type['service'] + Road_Length_With_Type['steps'] + \
                                 Road_Length_With_Type['track'] + Road_Length_With_Type['track_grade3']
Road_Length_With_Type['All_Road_Length'] = Road_Length_With_Type.iloc[:, 1:-3].sum(axis=1)
Road_Length_With_Type = Road_Length_With_Type[['TAZ', 'Primary', 'Secondary', 'Minor', 'All_Road_Length']]
