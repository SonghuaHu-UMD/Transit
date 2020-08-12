import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import seaborn as sns

os.chdir(r'D:\Transit')

# Plot the time series
Results_All = pd.read_csv(r'finalMatrix_Transit_0810.csv', index_col=0)
Results_All['Date'] = pd.to_datetime(Results_All['Date'])
# plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 24, 'font.family': "Times New Roman"})

for jj in set(Results_All['CTNAME']):
    print(jj)
    # jj = 40930
    myFmt = mdates.DateFormatter('%Y')
    Temp_time = Results_All[Results_All['CTNAME'] == jj]
    # Temp_time = Temp_time[Temp_time['Date'] >= '2019-01-01']
    Temp_time.set_index('Date', inplace=True)

    fig, ax = plt.subplots(nrows=6, ncols=1, figsize=(11, 9.5), sharex=True)  # 12,9.5
    # ax[0].set_title('Station_ID: ' + str(jj))
    ax[0].plot(Temp_time.loc[Temp_time['Component'] == 'Trend', 'Value'], color='#2f4c58')
    ax[0].set_ylabel('Trend')

    ax[1].plot(Temp_time.loc[Temp_time['Component'] == 'Seasonality', 'Value'], color='#2f4c58')
    ax[1].set_ylabel('Seasonality')

    ax[2].plot(Temp_time.loc[Temp_time['Component'] == 'Monthly', 'Value'], color='#2f4c58')
    ax[2].set_ylabel('Monthly')

    ax[3].plot(Temp_time.loc[Temp_time['Component'] == 'Regression', 'Value'], color='#2f4c58')
    ax[3].set_ylabel('Regressor')

    ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'], color='#2f4c58')
    ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Predict', 'Value'], '--', color='#62760c', alpha=0.8, lw=0.5)
    ax[4].fill_between(Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'].index,
                       Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'],
                       Temp_time.loc[Temp_time['Component'] == 'Predict_Upper', 'Value'], facecolor='#96bb7c',
                       alpha=0.5)
    ax[4].set_ylabel('Prediction')

    ax[5].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
        Temp_time['Component'] == 'Predict', 'Value'], color='#2f4c58')
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
    plt.subplots_adjust(top=0.987, bottom=0.087, left=0.127, right=0.982, hspace=0.078, wspace=0.09)
    # plt.savefig('FIG2-1.png', dpi=600)
    plt.savefig(r'D:\Transit\Full_Time_Figure\Full_Time_Range_' + str(jj) + 'png', dpi=500)
    plt.close()

# Plot the zoom in figure
jj = 40930
myFmt = mdates.DateFormatter('%b-%d')
Temp_time = Results_All[Results_All['CTNAME'] == jj]
Temp_time = Temp_time[Temp_time['Date'] >= '2020-01-01']
Temp_time.set_index('Date', inplace=True)
fig, ax = plt.subplots(nrows=6, ncols=1, figsize=(6, 9.5), sharex=True)  # 12,9.5
# ax[0].set_title('Station_ID: ' + str(jj))
ax[0].plot(Temp_time.loc[Temp_time['Component'] == 'Trend', 'Value'], color='#2f4c58')
# ax[0].set_ylabel('Trend')

ax[1].plot(Temp_time.loc[Temp_time['Component'] == 'Seasonality', 'Value'], color='#2f4c58')
# ax[1].set_ylabel('Seasonality')

ax[2].plot(Temp_time.loc[Temp_time['Component'] == 'Monthly', 'Value'], color='#2f4c58')
# ax[2].set_ylabel('Monthly')

ax[3].plot(Temp_time.loc[Temp_time['Component'] == 'Regression', 'Value'], color='#2f4c58')
# ax[3].set_ylabel('Regressor')

ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'], color='#2f4c58')
ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Predict', 'Value'], '--', color='#62760c', alpha=0.8)
ax[4].fill_between(Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'].index,
                   Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'],
                   Temp_time.loc[Temp_time['Component'] == 'Predict_Upper', 'Value'], facecolor='#96bb7c',
                   alpha=0.5)
# ax[4].set_ylabel('Prediction')

ax[5].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
    Temp_time['Component'] == 'Predict', 'Value'], color='#2f4c58')
ax[5].fill_between(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'].index,
                   Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                       Temp_time['Component'] == 'Predict_Upper', 'Value'],
                   Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                       Temp_time['Component'] == 'Predict_Lower', 'Value'], facecolor='#96bb7c', alpha=0.5)
ax[5].xaxis.set_major_formatter(myFmt)
ax[5].xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
# ax[5].set_ylabel('Residual')
ax[5].set_xlabel('Date')
plt.xlim(xmin=min(Temp_time.index), xmax=max(Temp_time.index))
# fig.autofmt_xdate()
for ax0 in ax:
    ax0.axes.yaxis.set_visible(False)
plt.tight_layout()
plt.subplots_adjust(top=0.987, bottom=0.087, left=0.022, right=0.987, hspace=0.078, wspace=0.09)
# plt.subplots_adjust(top=0.987, bottom=0.087, left=0.127, right=0.982, hspace=0.078, wspace=0.09)
plt.savefig('FIG2-2.png', dpi=600)

# Calculate the casual impact
# Start from 03-02
Impact = pd.read_csv(r'D:\Transit\finalMatrix_Transit.csv', index_col=0)
Impact['time'] = pd.to_datetime(Impact['time'])
Impact = Impact.reset_index(drop=True)
Impact.rename(columns={'CTNAME': 'station_id'}, inplace=True)
Impact_0302 = Impact[Impact['time'] >= datetime.datetime(2020, 3, 2)]
# Calculate the relative impact
Impact_0302['Relative_Impact'] = (Impact_0302['point.effect'] / Impact_0302['point.pred'])
Impact_0302['Relative_Impact_lower'] = (Impact_0302['point.effect.lower'] / Impact_0302['point.pred.lower'])
Impact_0302['Relative_Impact_upper'] = (Impact_0302['point.effect.upper'] / Impact_0302['point.pred.upper'])

Impact_Sta = Impact_0302.groupby(['station_id']).mean()['Relative_Impact'].reset_index()
plt.plot(Impact_Sta['Relative_Impact'])
Stations = pd.read_csv('LStations_Chicago.csv', index_col=0)
Impact_Sta = Impact_Sta.merge(Stations, on='station_id')
Impact_Sta.to_csv('Impact_Sta_.csv')

Impact_Sta_plot = Impact_0302.groupby(['time']).mean().reset_index()

sns.set_palette("deep")
# sns.color_palette(flatui, Impact_0302.station_id.unique().shape[0])
# flatui = ["#2f4c58"]
fig, ax = plt.subplots(figsize=(8, 8), nrows=4, ncols=1, sharex=True)
ax[0].ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
ax[1].ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
ax[2].ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)

sns.lineplot(data=Impact_0302, x='time', hue='station_id', y='point.pred', ax=ax[0], legend=False,
             palette=sns.color_palette("Set2", Impact_0302.station_id.unique().shape[0]), alpha=0.3)
ax[0].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.pred'], color='#2f4c58')
# ax[0].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.pred.lower'], '--', color='#2f4c58')
# ax[0].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.pred.upper'], '--', color='#2f4c58')
ax[0].set_ylabel('Prediction')

sns.lineplot(data=Impact_0302, x='time', hue='station_id', y='response', ax=ax[1], legend=False,
             palette=sns.color_palette("Set2", Impact_0302.station_id.unique().shape[0]), alpha=0.3)
ax[1].plot(Impact_Sta_plot['time'], Impact_Sta_plot['response'], color='#2f4c58')
ax[1].set_ylabel('Response')

sns.lineplot(data=Impact_0302, x='time', hue='station_id', y='point.effect', ax=ax[2], legend=False,
             palette=sns.color_palette("Set2", Impact_0302.station_id.unique().shape[0]), alpha=0.3)
ax[2].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.effect'], color='#2f4c58')
# ax[2].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.effect.lower'], '--', color='#2f4c58')
# ax[2].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.effect.upper'], '--', color='#2f4c58')
ax[2].set_ylabel('Absolute impact')

sns.lineplot(data=Impact_0302, x='time', hue='station_id', y='Relative_Impact', ax=ax[3], legend=False,
             palette=sns.color_palette("Set2", Impact_0302.station_id.unique().shape[0]), alpha=0.3)
ax[3].plot(Impact_Sta_plot['time'], Impact_Sta_plot['Relative_Impact'], color='#2f4c58')
# ax[3].plot(Impact_Sta_plot['time'], Impact_Sta_plot['Relative_Impact_lower'], '--', color='#2f4c58')
# ax[3].plot(Impact_Sta_plot['time'], Impact_Sta_plot['Relative_Impact_upper'], '--', color='#2f4c58')
ax[3].xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
ax[3].xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax[3].set_xlabel('Date')
ax[3].set_ylabel('Relative impact')
# plt.tight_layout()
plt.subplots_adjust(top=0.954, bottom=0.078, left=0.088, right=0.97, hspace=0.233, wspace=0.2)
plt.savefig(r'Fig-3.png', dpi=600)
