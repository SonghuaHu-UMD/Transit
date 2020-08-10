import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import seaborn as sns

myFmt = mdates.DateFormatter('%y-%b-%d')

os.chdir(r'D:\Transit')

# Plot the time series
Results_All = pd.read_csv(r'finalMatrix_Transit_0810.csv', index_col=0)
Results_All['Date'] = pd.to_datetime(Results_All['Date'])
# plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 16, 'font.family': "Times New Roman"})

for jj in set(Results_All['CTNAME']):
    print(jj)
    Temp_time = Results_All[Results_All['CTNAME'] == jj]
    # Temp_time = Temp_time[Temp_time['Date'] >= '2018-01-01']
    Temp_time.set_index('Date', inplace=True)

    fig, ax = plt.subplots(nrows=6, ncols=1, figsize=(19, 9.5), sharex=True)  # 12,9.5
    ax[0].set_title('Station_ID: ' + str(jj))
    ax[0].plot(Temp_time.loc[Temp_time['Component'] == 'Trend', 'Value'], color='#10375c')
    ax[0].set_ylabel('Trend')

    ax[1].plot(Temp_time.loc[Temp_time['Component'] == 'Seasonality', 'Value'], color='#10375c')
    ax[1].set_ylabel('Seasonality')

    ax[2].plot(Temp_time.loc[Temp_time['Component'] == 'Monthly', 'Value'], color='#10375c')
    ax[2].set_ylabel('Monthly')

    ax[3].plot(Temp_time.loc[Temp_time['Component'] == 'Regression', 'Value'], color='#10375c')
    ax[3].set_ylabel('Regressor')

    ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'], color='#10375c')
    ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Predict', 'Value'], '--', color='#62760c', alpha=0.8)
    ax[4].fill_between(Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'].index,
                       Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'],
                       Temp_time.loc[Temp_time['Component'] == 'Predict_Upper', 'Value'], facecolor='#96bb7c',
                       alpha=0.5)
    ax[4].set_ylabel('Prediction')

    ax[5].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
        Temp_time['Component'] == 'Predict', 'Value'], color='#10375c')
    ax[5].fill_between(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'].index,
                       Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                           Temp_time['Component'] == 'Predict_Upper', 'Value'],
                       Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                           Temp_time['Component'] == 'Predict_Lower', 'Value'], facecolor='#96bb7c', alpha=0.5)
    ax[5].xaxis.set_major_formatter(myFmt)
    ax[5].set_ylabel('Residual')
    ax[5].set_xlabel('Date')
    plt.xlim(xmin=min(Temp_time.index), xmax=max(Temp_time.index))
    # fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig(r'D:\Transit\Full_Time_Figure\Full_Time_Range_' + str(jj) + 'png', dpi=500)
    plt.close()

# Calculate the casual impact
# Start from 03-02
Impact = pd.read_csv(r'D:\Transit\finalMatrix_Transit_0810.csv', index_col=0)
Impact = pd.pivot_table(Impact, values='Value', index=['Date', 'CTNAME'], columns=['Component']).reset_index()
Impact['Date'] = pd.to_datetime(Impact['Date'])
Impact.rename(columns={'CTNAME': 'station_id'}, inplace=True)
Impact_0302 = Impact[Impact['Date'] >= datetime.datetime(2020, 3, 2)]
Impact_0302 = Impact_0302.sort_values(by=['station_id', 'Date']).reset_index(drop=True)
# Calculate the relative impact
Impact_0302['Relative_Impact'] = (Impact_0302['Predict'] - Impact_0302['Response']) / Impact_0302['Predict']
Impact_Sta = Impact_0302.groupby(['station_id']).mean()['Relative_Impact'].reset_index()
plt.plot(Impact_Sta['Relative_Impact'])
Stations = pd.read_csv('LStations_Chicago.csv', index_col=0)
Impact_Sta = Impact_Sta.merge(Stations, on='station_id')
Impact_Sta.to_csv('Impact_Sta_0810.csv')

fig, ax = plt.subplots(figsize=(8, 6), nrows=3, ncols=1)
sns.lineplot(data=Impact_0302, x='time', hue='station_id', y='point.pred', ax=ax[0])
sns.lineplot(data=Impact_0302, x='time', hue='station_id', y='response', ax=ax[1])
sns.lineplot(data=Impact_0302, x='time', hue='station_id', y='point.effect', ax=ax[2])
