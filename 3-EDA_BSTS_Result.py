import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import seaborn as sns
import geopandas as gpd

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
    ax[0].plot(Temp_time.loc[Temp_time['Component'] == 'Trend', 'Value'], color='#2f4c58', alpha=0.6)
    ax[0].set_ylabel('Trend')

    ax[1].plot(Temp_time.loc[Temp_time['Component'] == 'Seasonality', 'Value'], color='#2f4c58', alpha=0.6)
    ax[1].set_ylabel('Weekly')

    ax[2].plot(Temp_time.loc[Temp_time['Component'] == 'Monthly', 'Value'], color='#2f4c58', alpha=0.6)
    ax[2].set_ylabel('Monthly')

    ax[3].plot(Temp_time.loc[Temp_time['Component'] == 'Regression', 'Value'], color='#2f4c58', alpha=0.6)
    ax[3].set_ylabel('Covariates')

    ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'], color='#2f4c58', alpha=0.6)
    ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Predict', 'Value'], '--', color='#62760c', alpha=0.6, lw=0.5)
    ax[4].fill_between(Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'].index,
                       Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'],
                       Temp_time.loc[Temp_time['Component'] == 'Predict_Upper', 'Value'], facecolor='#96bb7c',
                       alpha=0.5)
    ax[4].set_ylabel('Prediction')

    ax[5].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
        Temp_time['Component'] == 'Predict', 'Value'], color='#2f4c58', alpha=0.6)
    ax[5].fill_between(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'].index,
                       Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                           Temp_time['Component'] == 'Predict_Upper', 'Value'],
                       Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                           Temp_time['Component'] == 'Predict_Lower', 'Value'], facecolor='#96bb7c', alpha=0.5)
    ax[5].xaxis.set_major_formatter(myFmt)
    ax[5].set_ylabel('Residual')
    ax[5].set_xlabel('Date')
    plt.xlim(xmin=min(Temp_time.index), xmax=max(Temp_time.index))
    # for axx in ax:
    #     axx.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=False)
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
ax[0].plot(Temp_time.loc[Temp_time['Component'] == 'Trend', 'Value'], color='#2f4c58')
ax[1].plot(Temp_time.loc[Temp_time['Component'] == 'Seasonality', 'Value'], color='#2f4c58')
ax[2].plot(Temp_time.loc[Temp_time['Component'] == 'Monthly', 'Value'], color='#2f4c58')
ax[3].plot(Temp_time.loc[Temp_time['Component'] == 'Regression', 'Value'], color='#2f4c58')
ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'], color='#2f4c58')
ax[4].plot(Temp_time.loc[Temp_time['Component'] == 'Predict', 'Value'], '--', color='#62760c', alpha=0.8)
ax[4].fill_between(Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'].index,
                   Temp_time.loc[Temp_time['Component'] == 'Predict_Lower', 'Value'],
                   Temp_time.loc[Temp_time['Component'] == 'Predict_Upper', 'Value'], facecolor='#96bb7c',
                   alpha=0.5)
ax[5].plot(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
    Temp_time['Component'] == 'Predict', 'Value'], color='#2f4c58')
ax[5].fill_between(Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'].index,
                   Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                       Temp_time['Component'] == 'Predict_Upper', 'Value'],
                   Temp_time.loc[Temp_time['Component'] == 'Response', 'Value'] - Temp_time.loc[
                       Temp_time['Component'] == 'Predict_Lower', 'Value'], facecolor='#96bb7c', alpha=0.5)
ax[5].xaxis.set_major_formatter(myFmt)
ax[5].xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
ax[5].set_xlabel('Date')
plt.xlim(xmin=min(Temp_time.index), xmax=max(Temp_time.index))
for ax0 in ax:
    ax0.axes.yaxis.set_visible(False)
plt.tight_layout()
plt.subplots_adjust(top=0.987, bottom=0.087, left=0.022, right=0.987, hspace=0.078, wspace=0.09)
plt.savefig('FIG2-2.png', dpi=600)

# Calculate the casual impact
# For build the PLS model
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
# plt.plot(Impact_Sta['Relative_Impact'])
# sns.distplot(Impact_Sta['Relative_Impact'])
Stations = pd.read_csv('LStations_Chicago.csv', index_col=0)
Impact_Sta = Impact_Sta.merge(Stations, on='station_id')
Impact_Sta.to_csv('Impact_Sta_.csv')

# For paper, set date at 03-13

Impact_Sta_0312 = Impact[Impact['time'] >= datetime.datetime(2020, 3, 14)]
Impact_Sta_0312['Relative_Impact'] = (Impact_Sta_0312['point.effect'] / Impact_Sta_0312['point.pred'])
Impact_Sta_0312['Relative_Impact_lower'] = (Impact_Sta_0312['point.effect.lower'] / Impact_Sta_0312['point.pred.lower'])
Impact_Sta_0312['Relative_Impact_upper'] = (Impact_Sta_0312['point.effect.upper'] / Impact_Sta_0312['point.pred.upper'])
Station_Impact = Impact_Sta_0312.groupby(['station_id']).mean()['Relative_Impact'].reset_index()
Stations = pd.read_csv('LStations_Chicago.csv', index_col=0)
Station_Impact = Station_Impact.merge(Stations, on='station_id')
Station_Impact.to_csv('Impact_Sta_ARCGIS.csv')

# Spatial plot
gdf_impact = gpd.GeoDataFrame(Station_Impact, geometry=gpd.points_from_xy(Station_Impact.LNG, Station_Impact.LAT))
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 8))
gdf_impact.plot(column='Relative_Impact', ax=ax[0], legend=True, scheme='fisher_jenks',
                markersize=abs(gdf_impact['Relative_Impact'] * 100),
                legend_kwds=dict(frameon=False, ncol=1), linewidth=0.1, edgecolor='white', cmap='YlGnBu')

# Plot the impact for each station
Impact_0101 = Impact[Impact['time'] >= datetime.datetime(2020, 2, 1)]
Impact_0101['Relative_Impact'] = (Impact_0101['point.effect'] / Impact_0101['point.pred'])
Impact_0101['Relative_Impact_lower'] = (Impact_0101['point.effect.lower'] / Impact_0101['point.pred.lower'])
Impact_0101['Relative_Impact_upper'] = (Impact_0101['point.effect.upper'] / Impact_0101['point.pred.upper'])
Impact_Sta_plot = Impact_0101.groupby(['time']).mean().reset_index()
sns.set_palette(sns.color_palette("GnBu_d"))
plt.rcParams.update({'font.size': 18, 'font.family': "Times New Roman"})
fig, ax = plt.subplots(figsize=(12, 8), nrows=4, ncols=1, sharex=True)
ax[0].ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
ax[1].ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
ax[2].ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)

sns.lineplot(data=Impact_0101, x='time', hue='station_id', y='point.pred', ax=ax[0], legend=False,
             palette=sns.color_palette("GnBu_d", Impact_0101.station_id.unique().shape[0]), alpha=0.4)
ax[0].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.pred'], color='#2f4c58', lw=2)
# ax[0].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.pred.lower'], '--', color='#2f4c58')
# ax[0].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.pred.upper'], '--', color='#2f4c58')
ax[0].set_ylabel('Prediction')

sns.lineplot(data=Impact_0101, x='time', hue='station_id', y='response', ax=ax[1], legend=False,
             palette=sns.color_palette("GnBu_d", Impact_0101.station_id.unique().shape[0]), alpha=0.4)
ax[1].plot(Impact_Sta_plot['time'], Impact_Sta_plot['response'], color='#2f4c58', lw=2)
ax[1].set_ylabel('Response')

sns.lineplot(data=Impact_0101, x='time', hue='station_id', y='point.effect', ax=ax[2], legend=False,
             palette=sns.color_palette("GnBu_d", Impact_0101.station_id.unique().shape[0]), alpha=0.4)
ax[2].plot([datetime.datetime(2020, 2, 1), datetime.datetime(2020, 4, 30)], [0, 0], '--', color='r')
ax[2].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.effect'], color='#2f4c58', lw=2)
ax[2].plot([datetime.datetime(2020, 3, 11), datetime.datetime(2020, 3, 11)], [-2 * 10e3, 0.2 * 10e3], '--',
           color='#2f4c58', lw=2)
plt.text(0.35, 0.1, 'Pre-Intervention', horizontalalignment='center', verticalalignment='center',
         transform=ax[2].transAxes)
plt.text(0.53, 0.1, 'Intervention', horizontalalignment='center', verticalalignment='center',
         transform=ax[2].transAxes)
# ax[2].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.effect.lower'], '--', color='#2f4c58')
# ax[2].plot(Impact_Sta_plot['time'], Impact_Sta_plot['point.effect.upper'], '--', color='#2f4c58')
ax[2].set_ylabel('Piecewise impact')

sns.lineplot(data=Impact_0101, x='time', hue='station_id', y='Relative_Impact', ax=ax[3], legend=False,
             palette=sns.color_palette("GnBu_d", Impact_0101.station_id.unique().shape[0]), alpha=0.4)
ax[3].plot(Impact_Sta_plot['time'], Impact_Sta_plot['Relative_Impact'], color='#2f4c58', lw=2)
ax[3].plot([datetime.datetime(2020, 2, 1), datetime.datetime(2020, 4, 30)], [0, 0], '--', color='r')
ax[3].plot([datetime.datetime(2020, 3, 11), datetime.datetime(2020, 3, 11)], [-1, 1], '--', color='#2f4c58', lw=2)
# ax[3].plot(Impact_Sta_plot['time'], Impact_Sta_plot['Relative_Impact_lower'], '--', color='#2f4c58')
# ax[3].plot(Impact_Sta_plot['time'], Impact_Sta_plot['Relative_Impact_upper'], '--', color='#2f4c58')
ax[3].xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
ax[3].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
ax[3].set_xlabel('Date')
ax[3].set_ylabel('Relative impact')
plt.text(0.35, 0.1, 'Pre-Intervention', horizontalalignment='center', verticalalignment='center',
         transform=ax[3].transAxes)
plt.text(0.53, 0.1, 'Intervention', horizontalalignment='center', verticalalignment='center',
         transform=ax[3].transAxes)
# plt.tight_layout()
plt.subplots_adjust(top=0.954, bottom=0.078, left=0.068, right=0.985, hspace=0.233, wspace=0.2)
plt.savefig(r'Fig-3.png', dpi=600)
plt.savefig(r'Fig-3.svg')

# Residual
Results_All_Res = Results_All[Results_All['Date'] < datetime.datetime(2020, 3, 2)]
Results_All_Res = pd.pivot_table(Results_All_Res, values='Value', index=['Date', 'CTNAME'],
                                 columns=['Component']).reset_index()
Results_All_Res.columns
Results_All_Res['Residual'] = Results_All_Res['Response'] - Results_All_Res['Predict']
Results_All_Res['MAE'] = abs(Results_All_Res['Response'] - Results_All_Res['Predict'])
Results_All_Res['MAPE'] = abs(
    (Results_All_Res['Response'] - Results_All_Res['Predict']) / (Results_All_Res['Response']))
Results_All_Res = Results_All_Res.replace([np.inf, -np.inf], np.nan)
Results_All_Res.isnull().sum()
Results_All_Res = Results_All_Res.fillna(0)
Results_All_Res.describe()
Results_All_Res.groupby(['CTNAME']).median()['MAPE'].min()
Results_All_Res.groupby(['CTNAME']).median()['MAPE'].max()

fig, ax = plt.subplots(figsize=(14, 6))
sns.boxplot(x="CTNAME", y="MAPE", data=Results_All_Res, palette=sns.color_palette("GnBu_d"), showfliers=False, ax=ax,
            linewidth=1)
ax.tick_params(labelbottom=False)
ax.set_xlabel('Transit Station')
# ax.set_ylim([0, 0.15])
plt.tight_layout()
plt.savefig('Fig-MAPE.png', dpi=600)
plt.savefig('Fig-MAPE.svg')
# Tem_DA = pd.DataFrame({'Response': Results_All_Res.loc[Results_All_Res['Component'] == 'Response', 'Value'].values,
#                        'Predict': Results_All_Res.loc[Results_All_Res['Component'] == 'Predict', 'Value'].values})

# Coeeff
Coeffic = pd.read_csv(r'finalCoeff_Transit_0810.csv', index_col=0)
Coeffic.columns
Coeffic.describe().T
fig, ax = plt.subplots(figsize=(14, 6), nrows=2, ncols=2)
sns.boxplot(x="CTNAME", y="PRCP", data=Coeffic, palette=sns.color_palette("GnBu_d"), showfliers=False, ax=ax[0][0],
            linewidth=1)
sns.boxplot(x="CTNAME", y="TMAX", data=Coeffic, palette=sns.color_palette("GnBu_d"), showfliers=False, ax=ax[0][1],
            linewidth=1)
sns.boxplot(x="CTNAME", y="Holidays", data=Coeffic, palette=sns.color_palette("GnBu_d"), showfliers=False, ax=ax[1][0],
            linewidth=1)
sns.boxplot(x="CTNAME", y="IsWeekend", data=Coeffic, palette=sns.color_palette("GnBu_d"), showfliers=False, ax=ax[1][1],
            linewidth=1)

ax[0][0].tick_params(labelbottom=False)
ax[0][1].tick_params(labelbottom=False)
ax[1][0].tick_params(labelbottom=False)
ax[1][1].tick_params(labelbottom=False)

plt.rcParams.update({'font.size': 20, 'font.family': "Times New Roman"})
fig, ax = plt.subplots(figsize=(14, 4), nrows=1, ncols=3)
ax[0].set_ylabel('Frequency')
sns.distplot(Coeffic['PRCP'], ax=ax[0], rug_kws={"color": "g"}, axlabel='Coeff. of Precipitation',
             hist_kws={"histtype": "step", "linewidth": 2, "alpha": 0.8, "color": "g"},
             kde=False)
sns.distplot(Coeffic['TMAX'], ax=ax[1], rug_kws={"color": "g"}, axlabel='Coeff. of Temperature',
             hist_kws={"histtype": "step", "linewidth": 2, "alpha": 0.8, "color": "g"},
             kde=False)
sns.distplot(Coeffic['Holidays'], ax=ax[2], rug_kws={"color": "g"}, axlabel='Coeff. of Is Holiday',
             hist_kws={"histtype": "step", "linewidth": 2, "alpha": 0.8, "color": "g"},
             kde=False)
plt.text(0.3, 0.9, 'Mean = -0.6207', horizontalalignment='center', verticalalignment='center',
         transform=ax[0].transAxes)
plt.text(0.3, 0.9, 'Mean = 1.2913', horizontalalignment='center', verticalalignment='center',
         transform=ax[1].transAxes)
plt.text(0.3, 0.9, 'Mean = -1564.2068', horizontalalignment='center', verticalalignment='center',
         transform=ax[2].transAxes)
for axx in ax:
    axx.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
plt.subplots_adjust(top=0.885, bottom=0.213, left=0.049, right=0.984, hspace=0.2, wspace=0.198)
plt.savefig('Hist.png', dpi=600)
plt.savefig('Hist.svg')