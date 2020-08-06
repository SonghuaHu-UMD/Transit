# Daily_Lstaion['Day'] = (Daily_Lstaion.date.dt.month).astype(str) + '-' + (Daily_Lstaion.date.dt.day).astype(str)
# Daily
Daily_Count = Daily_Lstaion.groupby(['date']).sum()['rides']
Daily_Count.plot()

# For each station, calculate the decrease
Daily_Lstaion_2019 = Daily_Lstaion[Daily_Lstaion['Year'] == 2019]
Daily_Lstaion_2020 = Daily_Lstaion[Daily_Lstaion['Year'] == 2020]
Daily_Lstaion_2020 = Daily_Lstaion_2020.merge(Daily_Lstaion_2019, on=['station_id', 'Day'])
Daily_Lstaion_2020['Diff'] = (Daily_Lstaion_2020['rides_y'] - Daily_Lstaion_2020['rides_x']) / Daily_Lstaion_2020[
    'rides_y']

# Each station
Daily_Lstaion_2020.groupby(['station_id']).mean()['Diff'].plot()

import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pylab as plt
from scipy import stats
from pandas.tseries.holiday import USFederalHolidayCalendar

os.chdir(r'D:\Transit')


def haversine_array(lat1, lng1, lat2, lng2):
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    AVG_EARTH_RADIUS = 6371  # in km
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))
    return h


# Read the L station ridership
Daily_Lstaion = pd.read_csv(r'CTA_-_Ridership_-__L__Station_Entries_-_Daily_Totals.csv')
Daily_Lstaion['date'] = pd.to_datetime(Daily_Lstaion['date'])
Daily_Lstaion = Daily_Lstaion.sort_values(by=['station_id', 'date']).reset_index(drop=True)
Daily_Lstaion['Year'] = Daily_Lstaion.date.dt.year
# Only need after 2015
Daily_Lstaion = Daily_Lstaion[Daily_Lstaion['Year'] >= 2015].reset_index(drop=True)
Daily_Lstaion = Daily_Lstaion.drop_duplicates(subset=['station_id', 'date'])
# Some stations drop before 2020
Daily_Lstaion = Daily_Lstaion[
    Daily_Lstaion['station_id'].isin(set(Daily_Lstaion[Daily_Lstaion['Year'] == 2020]['station_id']))].reset_index(
    drop=True)
print(len(set(Daily_Lstaion['station_id'])))

# Range the date
max(Daily_Lstaion['date'])
Date_Range = pd.DataFrame(
    {'date': list(pd.date_range('2015-01-01', '2020-04-30', freq='D')) * len(set(Daily_Lstaion['station_id'])),
     'station_id': np.repeat(list(set(Daily_Lstaion['station_id'])),
                             len(list(pd.date_range('2015-01-01', '2020-04-30', freq='D'))))})
Daily_Lstaion = Daily_Lstaion.merge(Date_Range, on=['station_id', 'date'], how='right')
Daily_Lstaion = Daily_Lstaion.sort_values(by=['station_id', 'date'])

# Check NaN and outliers using Z-score
# Some Data cannot be used
Daily_Lstaion['Year'] = Daily_Lstaion.date.dt.year
Daily_Lstaion = Daily_Lstaion.drop(
    Daily_Lstaion[(Daily_Lstaion['station_id'].isin([40140, 40460, 40660, 40710, 40800, 41680, 40140, 41690])) &
                  (Daily_Lstaion['Year'] == 2015)].index).reset_index(drop=True)
Daily_Lstaion = Daily_Lstaion.drop(
    Daily_Lstaion[(Daily_Lstaion['station_id'].isin([41700])) & (Daily_Lstaion['Year'] <= 2017)].index).reset_index(
    drop=True)

zscore = lambda x: abs((x - x.mean()) / x.std())
Daily_Lstaion['zscore'] = Daily_Lstaion.groupby(['station_id'])['rides'].transform(zscore)
Daily_Lstaion['Shift7'] = Daily_Lstaion.groupby(['station_id'])['rides'].shift(7)
Daily_Lstaion['Raw_Rides'] = Daily_Lstaion['rides']
Daily_Lstaion.loc[Daily_Lstaion['zscore'] > 2.5, 'rides'] = Daily_Lstaion.loc[Daily_Lstaion['zscore'] > 2.5, 'Shift7']
Daily_Lstaion.isnull().sum()
Daily_Lstaion = Daily_Lstaion.drop(['Shift7'], axis=1)
Daily_Lstaion = Daily_Lstaion.dropna().reset_index(drop=True)

'''
# Plot the figure for each station
the_zscore = 2.5
Daily_Lstaion_DE = Daily_Lstaion[Daily_Lstaion['Year'] != 2020].reset_index(drop=True)
for jj in list(set(Daily_Lstaion['station_id'])):
    tem = Daily_Lstaion[Daily_Lstaion['station_id'] == jj]
    # Find
    fig, ax = plt.subplots(figsize=(10, 5), nrows=2, ncols=1)
    ax[0].plot(tem['date'], tem['rides'], color='k')
    ax[1].plot(tem['date'], tem['Raw_Rides'], color='k')
    plt.tight_layout()
    plt.savefig(str(jj) + '.png')
    plt.close()
'''

# Find NAN
NA_Count = Daily_Lstaion.groupby(['station_id', 'Year']).count().reset_index()
# plt.plot(NA_Count['stationname'], 'o')
# Find 0
Daily_Lstaion['Is_Zero'] = Daily_Lstaion['rides'] == 0
Zero_Count = Daily_Lstaion.groupby(['station_id', 'Year'])['Is_Zero'].sum().reset_index()
plt.plot(Zero_Count['Is_Zero'], 'o')

# Merge with weather and holidays
# W=Weekday, A=Saturday, U=Sunday/Holiday
Daily_Lstaion['Week'] = Daily_Lstaion['date'].dt.dayofweek
Daily_Lstaion['IsWeekend'] = (Daily_Lstaion['Week'].isin([5, 6])).astype(int)
Daily_Lstaion['Holidays'] = 0
Daily_Lstaion.loc[(Daily_Lstaion['IsWeekend'] == 0) & (Daily_Lstaion['daytype'] != 'W'), 'Holidays'] = 1

# Merge with Station Location
Stations = pd.read_csv(r'CTA_-_System_Information_-_List_of__L__Stops.csv')
Stations = Stations[['MAP_ID', 'Location']]
Stations.columns = ['station_id', 'Location']
Stations['Location'] = Stations['Location'].str.replace('(', ',')
Stations['Location'] = Stations['Location'].str.replace(')', ',')
Stations['LAT'] = [var.split(',')[1] for var in Stations['Location']]
Stations['LNG'] = [var.split(',')[2] for var in Stations['Location']]
Stations = Stations[['station_id', 'LAT', 'LNG']]
Stations['LAT'] = Stations['LAT'].astype(float)
Stations['LNG'] = Stations['LNG'].astype(float)
Stations = Stations.drop_duplicates(subset='station_id').reset_index(drop=True)

# Merge with weather
# Get the weather station info
Station_raw = pd.read_csv(r'Weather\ghcnd-stations1.csv', header=None)
Station_raw = Station_raw.loc[:, 0:2]
Station_raw.columns = ['Sid', 'LAT', 'LON']
# Select the weather station close to transit stop
Need_Weather = []
for jj in range(0, len(Stations)):
    # print(jj)
    tem = Stations.loc[jj]
    Station_raw['Ref_Lat'] = tem['LAT']
    Station_raw['Ref_Lng'] = tem['LNG']
    Station_raw['Distance'] = haversine_array(Station_raw['Ref_Lat'], Station_raw['Ref_Lng'], Station_raw['LAT'],
                                              Station_raw['LON'])
    tem_id = list(Station_raw[Station_raw['Distance'] < 50]['Sid'])
    Need_Weather.extend(tem_id)
Need_Weather = set(Need_Weather)

## ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
ALL_WEATHER = pd.DataFrame()
for eachyear in [2015, 2016, 2017, 2018, 2019, 2020]:
    print(eachyear)
    Weather_raw = pd.read_csv('Weather\\' + str(eachyear) + '.csv', header=None)
    Weather_raw = Weather_raw.loc[:, 0:3]
    Weather_raw.columns = ['Sid', 'date', 'Type', 'Number']
    Weather_raw = Weather_raw[Weather_raw['Sid'].isin(Need_Weather)]
    PV_Weather = pd.pivot_table(Weather_raw, values='Number', index=['Sid', 'date'], columns=['Type']).reset_index()
    tem = PV_Weather.isnull().sum()
    PV_Weather = PV_Weather[['Sid', 'date', 'PRCP', 'TAVG', 'TMAX', 'TMIN']]
    # Find the nearest stations for each CT_Info
    All_Weather = pd.DataFrame()
    for jj in range(0, len(Stations)):
        # print(jj)
        tem = Stations.loc[jj]
        Station_raw['Ref_Lat'] = tem['LAT']
        Station_raw['Ref_Lng'] = tem['LNG']
        Station_raw['Distance'] = haversine_array(Station_raw['Ref_Lat'], Station_raw['Ref_Lng'], Station_raw['LAT'],
                                                  Station_raw['LON'])
        # sns.distplot(Station_raw['Distance'])
        tem_id = Station_raw[Station_raw['Distance'] < 15]['Sid']
        tem_weather_PRCP = PV_Weather[PV_Weather['Sid'].isin(tem_id)].groupby('date').mean()['PRCP'].reset_index()
        tem_id = Station_raw[Station_raw['Distance'] < 30]['Sid']
        tem_weather_T = PV_Weather[PV_Weather['Sid'].isin(tem_id)].groupby('date').mean()[
            ['TMAX', 'TMIN']].reset_index()
        tem_weather_PRCP = tem_weather_PRCP.merge(tem_weather_T, on='date', how='outer')
        tem_weather_PRCP['station_id'] = tem['station_id']
        All_Weather = All_Weather.append(tem_weather_PRCP)
    ALL_WEATHER = ALL_WEATHER.append(All_Weather)

# Unit: Precipitation (tenths of mm); Maximum temperature (tenths of degrees C)
ALL_WEATHER.isnull().sum()
ALL_WEATHER['TMAX'] = ALL_WEATHER['TMAX'].fillna(method='ffill').fillna(method='bfill')
ALL_WEATHER['TMIN'] = ALL_WEATHER['TMIN'].fillna(method='ffill').fillna(method='bfill')
# ALL_WEATHER = ALL_WEATHER.groupby('station_id')[['TMAX', 'TMIN', 'PRCP']].fillna(method='ffill').fillna(method='bfill')
# Change to mm and C
ALL_WEATHER['TMAX'] = ALL_WEATHER['TMAX'] * 0.1
ALL_WEATHER['TMIN'] = ALL_WEATHER['TMIN'] * 0.1
ALL_WEATHER['PRCP'] = ALL_WEATHER['PRCP'] * 0.1
# plt.plot(ALL_WEATHER['TMIN'], 'ok', alpha=0.2)
# plt.plot(All_Weather['PRCP'], 'ok', alpha=0.2)
ALL_WEATHER.to_csv('All_Weather_2015_2020.csv')
ALL_WEATHER['date'] = pd.to_datetime(ALL_WEATHER['date'], format='%Y%m%d')
# Merge with weather
Daily_Lstaion_Final = Daily_Lstaion.merge(ALL_WEATHER, on=['station_id', 'date'], how='left')
Daily_Lstaion_Final.isnull().sum()

Daily_Lstaion_Final[['station_id', 'stationname', 'date', 'daytype', 'rides', 'Year',
                     'Raw_Rides', 'Week', 'IsWeekend', 'Holidays', 'PRCP', 'TMAX', 'TMIN']].to_csv(
    'Daily_Lstaion_Final.csv', index=False)

Count_sta = Daily_Lstaion_Final[Daily_Lstaion_Final['Year'] == 2019].groupby(['station_id']).mean()[
    ['rides']].reset_index()
Stations = Stations.merge(Count_sta, on='station_id')
Stations.to_csv('LStations_Chicago.csv')

# Calculate the casual impact
# Start from 03-02
Impact = pd.read_csv(r'C:\Users\Songhua Hu\Desktop\Transit\finalMatrix_Transit.csv', index_col=0)
Impact['time'] = pd.to_datetime(Impact['time'])
Impact = Impact.reset_index(drop=True)
Impact.rename(columns={'CTNAME': 'station_id'}, inplace=True)
Impact_0302 = Impact[Impact['time'] >= datetime.datetime(2020, 3, 2)]
# Calculate the relative impact
Impact_0302['Relative_Impact'] = (Impact_0302['point.effect'] / Impact_0302['point.pred'])
Impact_Sta = Impact_0302.groupby(['station_id']).mean()['Relative_Impact'].reset_index()
plt.plot(Impact_Sta['Relative_Impact'])
Impact_Sta = Impact_Sta.merge(Stations, on='station_id')
Impact_Sta.to_csv('Impact_Sta.csv')

