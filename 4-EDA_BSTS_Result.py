import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pylab as plt
import matplotlib.dates as mdates

myFmt = mdates.DateFormatter('%y-%b-%d')

os.chdir(r'D:\Transit')

# Plot the time series
Temp_time = pd.read_csv(r'finalMatrix_Transit_temp.csv', index_col=0)
Temp_time = Temp_time[Temp_time['Date'] >= '2018-01-01']
Temp_time['Date'] = pd.to_datetime(Temp_time['Date'])
Temp_time.set_index('Date', inplace=True)
Temp_time.columns
set(Temp_time['Component'])
fig, ax = plt.subplots(nrows=6, ncols=1)
ax[0].plot(Temp_time.loc[Temp_time['Component'] == 'Trend', 'Value'])
ax[0].xaxis.set_major_formatter(myFmt)
ax[1].plot(Temp_time.loc[Temp_time['Component'] == 'Seasonality', 'Value'])
ax[1].xaxis.set_major_formatter(myFmt)
ax[2].plot(Temp_time.loc[Temp_time['Component'] == 'Monthly', 'Value'])
ax[2].xaxis.set_major_formatter(myFmt)
ax[3].plot(Temp_time.loc[Temp_time['Component'] == 'Regression', 'Value'])
ax[3].xaxis.set_major_formatter(myFmt)
ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'])
ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Predict', 'Value'], '--', color='k', alpha=0.8)
ax[4].fill_between(Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'].index,
                   Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'],
                   Temp_time.loc[Temp_time['Component'] == 'Predict_Upper', 'Value'], facecolor='g', alpha=0.5)
ax[4].xaxis.set_major_formatter(myFmt)
ax[5].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
    Temp_time['Component'] == 'Predict', 'Value'])
ax[5].fill_between(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'].index,
                   Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                       Temp_time['Component'] == 'Predict_Upper', 'Value'],
                   Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                       Temp_time['Component'] == 'Predict_Lower', 'Value'], facecolor='g', alpha=0.5)
ax[5].xaxis.set_major_formatter(myFmt)

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
