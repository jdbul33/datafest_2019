# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 22:30:59 2019

@author: jdbul
"""


"""
Import necessary packages
"""

import pandas as pd
import matplotlib.pyplot as plt

#%%

"""
Name file paths, must be in 'Data' subdirectory in Working Directory
Read in CSV data
"""

gps_file = "Data/gps.csv"
game_file = "Data/games.csv"
rpe_file = "Data/rpe.csv"
wellness_file = "Data/wellness.csv"

gps_data = pd.read_csv(gps_file)
games_data = pd.read_csv(game_file)
rpe_data = pd.read_csv(rpe_file)
wellness_data = pd.read_csv(wellness_file)

#%%
"""
Games
"""
games_data.head()
games_data.columns
games_data.info()
#games_data.describe().to_csv("games_description.csv")
assert games_data.isna().sum().sum() == 0
#no missing data, seems intact

#%%
"""
Games Exploration
"""
games_data.hist()



#%%
"""
RPE
"""
rpe_data.head()
rpe_data.columns
rpe_data.info()
#rpe_data.describe().to_csv("rpe_description.csv")
rpe_data.isna().sum()

#Significant missing data, especially in BestOutOfmySelf and Daily Load

#session_type_values = rpe_data['SessionType'].unique()
#%%
"""
RPE Exploration
"""
rpe_data.hist()


#%%
"""
Wellness
"""
wellness_data.head()
wellness_data.columns
wellness_data.info()
#wellness_data.describe().to_csv("wellness_description.csv")
wellness_data.isna().sum()

#%%
"""
Wellness Exploration
"""
wellness_data.hist()


#%%
"""
GPS
"""
gps_data.head()
gps_data.columns
gps_data.info()
#gps_data.describe().to_csv("gps_description.csv")
gps_data.isna().sum()


#%%
"""
GPS Exploration
"""
gps_data.hist()


#%%
"""
Join data frames
"""
gps_data['GameID'] = gps_data['GameID'].astype(str)
gps_data['PlayerID'] = gps_data['PlayerID'].astype(str)
gps_data['Half'] = gps_data['Half'].astype(str)


accelimpulse_grouped_mean = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['AccelImpulse'].mean().to_frame()
accelimpulse_grouped_std = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['AccelImpulse'].std().to_frame()
accelimpulse_grouped_skew = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['AccelImpulse'].skew().to_frame()
accelimpulse_grouped_median = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['AccelImpulse'].median().to_frame()
accelimpulse_merged = pd.merge(accelimpulse_grouped_mean, accelimpulse_grouped_std, how='inner', left_index=True, right_index=True, suffixes=('_mean', '_std'))
accelimpulse_merged = pd.merge(accelimpulse_merged, accelimpulse_grouped_median, how='inner', left_index=True, right_index=True, suffixes=('','_median'))
accelimpulse_merged = pd.merge(accelimpulse_merged, accelimpulse_grouped_skew, how='inner', left_index=True, right_index=True, suffixes=('','_skew'))
accelimpulse_merged.rename(index=str, columns={"AccelImpulse": "AccelImpulse_median"}, inplace=True)

#make sure it doesnt fuck up the column names



speed_grouped_mean = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['Speed'].mean().to_frame()
speed_grouped_std = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['Speed'].std().to_frame()
speed_grouped_skew = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['Speed'].skew().to_frame()
speed_grouped_median = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['Speed'].median().to_frame()
speed_grouped_sum = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['Speed'].sum().to_frame()
speed_merged = pd.merge(speed_grouped_mean, speed_grouped_std, how='inner', left_index=True, right_index=True, suffixes=('_mean', '_std'))
speed_merged = pd.merge(speed_merged, speed_grouped_median, how='inner', left_index=True, right_index=True)
speed_merged = pd.merge(speed_merged, speed_grouped_skew, how='inner', left_index=True, right_index=True, suffixes=('','_skew'))
speed_merged = pd.merge(speed_merged, speed_grouped_sum, how='inner', left_index=True, right_index=True, suffixes=('','_sum'))
speed_merged.rename(index=str, columns={"Speed": "Speed_median"}, inplace=True)

accel_speed_merged = pd.merge(accelimpulse_merged, speed_merged, how='inner', left_index=True, right_index=True)


#%%
"""
Create Eli calc column
"""

gps_data['Accel_3D'] = ((gps_data['AccelX']**2)+(gps_data['AccelY']**2)+(gps_data['AccelZ']**2))**(0.5)

#%%
"""
More Joining
"""

accel_directions_list = ['AccelX', 'AccelY', 'AccelZ', 'AccelLoad', 'Accel_3D']

for i in accel_directions_list:
    if i == 'AccelX':
        grouped_mean = gps_data.groupby(['PlayerID', 'GameID', 'Half'])[i].mean().to_frame()
        grouped_std = gps_data.groupby(['PlayerID', 'GameID', 'Half'])[i].std().to_frame()
        grouped_skew = gps_data.groupby(['PlayerID', 'GameID', 'Half'])[i].skew().to_frame()
        grouped_median = gps_data.groupby(['PlayerID', 'GameID', 'Half'])[i].median().to_frame()
        merged = pd.merge(grouped_mean, grouped_std, how='inner', left_index=True, right_index=True, suffixes=('_mean', '_std'))
        merged = pd.merge(merged, grouped_median, how='inner', left_index=True, right_index=True, suffixes=('','_median'))
        merged = pd.merge(merged, grouped_skew, how='inner', left_index=True, right_index=True, suffixes=('','_skew'))
        main = merged
    else:
        grouped_mean = gps_data.groupby(['PlayerID', 'GameID', 'Half'])[i].mean().to_frame()
        grouped_std = gps_data.groupby(['PlayerID', 'GameID', 'Half'])[i].std().to_frame()
        grouped_skew = gps_data.groupby(['PlayerID', 'GameID', 'Half'])[i].skew().to_frame()
        grouped_median = gps_data.groupby(['PlayerID', 'GameID', 'Half'])[i].median().to_frame()
        merged = pd.merge(grouped_mean, grouped_std, how='inner', left_index=True, right_index=True, suffixes=('_mean', '_std'))
        merged = pd.merge(merged, grouped_median, how='inner', left_index=True, right_index=True, suffixes=('','_median'))
        merged = pd.merge(merged, grouped_skew, how='inner', left_index=True, right_index=True, suffixes=('','_skew'))
        main = pd.merge(main, merged, how='inner', left_index=True, right_index=True)

#%%
"""
Merge this all into one
"""

# need to rename median columns since they arent working right

all_gps_data_summarized = pd.merge(accel_speed_merged, main, how='inner', left_index=True, right_index=True)
#all_gps_data_summarized.to_csv("GPS_Summary.csv")
