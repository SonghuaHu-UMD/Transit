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
