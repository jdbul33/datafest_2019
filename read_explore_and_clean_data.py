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
import numpy as np

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
#games_data.hist()



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
#rpe_data.hist()


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
#wellness_data.hist()


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
#gps_data.hist()


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
Create Eli calc columns
"""

gps_data['Accel_3D'] = ((gps_data['AccelX']**2)+(gps_data['AccelY']**2)+(gps_data['AccelZ']**2))**(0.5)
stddev_of_accel_load = 1.5*(gps_data['AccelLoad'].std())

temp_list = []

for i in range(len(gps_data['AccelLoad'])):
    if gps_data['AccelLoad'].iloc[i] >= stddev_of_accel_load or gps_data['AccelLoad'].iloc[i] >= stddev_of_accel_load:
        temp_list.append(1)
    else:
        temp_list.append(0)
        
gps_data['Count_Accel_Load_GE_1.5_SD'] = temp_list

accelload_grouped_sum = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['Count_Accel_Load_GE_1.5_SD'].sum().to_frame()

accel_speed_merged = pd.merge(accel_speed_merged, accelload_grouped_sum, how='inner', left_index=True, right_index=True)

#####

stddev_of_speed = 1.5*(gps_data['Speed'].std())

temp_list = []

for i in range(len(gps_data['Speed'])):
    if gps_data['Speed'].iloc[i] >= stddev_of_speed or gps_data['Speed'].iloc[i] >= stddev_of_speed:
        temp_list.append(1)
    else:
        temp_list.append(0)
        
gps_data['Count_Speed_GE_1.5_SD'] = temp_list

speedstd_grouped_sum = gps_data.groupby(['PlayerID', 'GameID', 'Half'])['Count_Speed_GE_1.5_SD'].sum().to_frame()

accel_speed_merged = pd.merge(accel_speed_merged, speedstd_grouped_sum, how='inner', left_index=True, right_index=True)


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

#%%
"""
Split by halves
"""

splitting_up = pd.DataFrame(all_gps_data_summarized.to_records())

first_half = splitting_up[splitting_up['Half'] == "1"]
second_half = splitting_up[splitting_up['Half'] == "2"]
halves_merged = pd.merge(first_half, second_half, how='inner', on=['PlayerID', 'GameID'], suffixes=('_1','_2'))
halves_merged.isna().sum().sum()

#%%
"""
Speed Difference
"""

halves_merged['Speed_Diff_by_Half'] = halves_merged.Speed_mean_1 - halves_merged.Speed_mean_2
halves_merged['Accel_Load_Diff_by_Half'] = halves_merged.AccelLoad_mean_1 - halves_merged.AccelLoad_mean_2
halves_merged['Accel_Impulse_Diff_by_Half'] = halves_merged.AccelImpulse_mean_1 - halves_merged.AccelImpulse_mean_2
halves_merged['Accel_3D_Diff_by_Half'] = halves_merged.Accel_3D_mean_1 - halves_merged.Accel_3D_mean_2

#%%
"""
RPE Grouping and Clean
"""

rpe_games_data = rpe_data[rpe_data['SessionType'] == 'Game']
rpe_games_data_cleaner = rpe_games_data.drop(columns=['Training', 'SessionType', 'SessionLoad', 'ObjectiveRating', 'FocusRating', 'BestOutOfMyself', 'DailyLoad'])

vars_to_include = ['Duration', 'RPE', 'AcuteLoad', 'ChronicLoad', 'AcuteChronicRatio']
list_of_frames = []

for i in vars_to_include:
    if i == 'Duration':
        list_of_frames.append(rpe_games_data_cleaner.groupby(['PlayerID', 'Date'])[i].sum().to_frame())
    else:
        list_of_frames.append(rpe_games_data_cleaner.groupby(['PlayerID', 'Date'])[i].mean().to_frame())
    
for i in range(len(list_of_frames)-1):
    if i == 0:
        j = i + 1
        merge_start = pd.merge(list_of_frames[i], list_of_frames[j], right_index=True, left_index=True, suffixes=('_sum', '_mean'))
    elif i == 1:
        j = i + 1
        merging = pd.merge(merge_start, list_of_frames[j], right_index=True, left_index=True, suffixes=('', '_mean'))
    else:
        j = i + 1
        merging = pd.merge(merging, list_of_frames[j], right_index=True, left_index=True, suffixes=('', '_mean'))
    
#%%
"""
Join with Games
"""

rpe_data_for_games = pd.DataFrame(merging.to_records())
rpe_data_for_games['PlayerID'] = rpe_data_for_games['PlayerID'].astype(str)
games_clean_data = games_data.drop(columns=['TournamentGame', 'Tournament', 'Team', 'Opponent', 'Outcome'])
games_clean_data['GameID'] = games_clean_data['GameID'].astype(str)
games_w_rpe_data = pd.merge(games_clean_data, rpe_data_for_games, left_on='Date', right_on='Date')

#%%
"""
Merge with the GPS data and such
"""
halves_merged.set_index(['GameID', 'PlayerID'], inplace=True)
games_w_rpe_data.set_index(['GameID', 'PlayerID'], inplace=True)
all_data = pd.merge(halves_merged, games_w_rpe_data, left_index=True, right_index=True)

#all_data.to_csv('all_except_wellness_data.csv')

#%%
"""
Merge Mark's wellness normed to the table
"""
file_path_wellness_norm = 'wellness_normalized.csv'
wellness_normalized = pd.read_csv(file_path_wellness_norm)


wellness_normalized['PlayerID'] = wellness_normalized['PlayerID'].astype(str)
wellness_normalized.drop(columns=['Unnamed: 0', 'BedTime', 'WakeTime', 'USGMeasurement',
                                  'USG', 'NutritionAdjustment', 'Nutrition'], inplace=True)
    
wellness_normalized['TrainingReadiness'] = wellness_normalized['TrainingReadiness'].str.strip('%').astype(int)

wellness_normalized.isna().sum()

wellness_normalized['Menstruation'].value_counts()

wellness_normalized['Menstruation'] = wellness_normalized['Menstruation'].fillna('No')

assert wellness_normalized.isna().sum().sum() == 0

#%%
"""
Make Dummies
"""
wellness_normalized.set_index(['PlayerID', 'Date'], inplace=True)
wellness_w_dummies = pd.get_dummies(wellness_normalized)

#%%
"""
Join to rest of data
"""

all_data_apart = pd.DataFrame(all_data.to_records())
all_data_apart.set_index(['PlayerID', 'Date'], inplace=True)

even_more_all_data = pd.merge(all_data_apart, wellness_w_dummies, how='left',
                              left_index=True, right_index=True)
even_more_all_data.drop(columns=['Half_1', 'Half_2'], inplace=True)
even_more_all_data_games_dummies = pd.get_dummies(even_more_all_data)

#even_more_all_data_games_dummies.to_csv('all_data_games_dummies.csv')

#%%
"""
Create more fucking variables for my failing model team
"""
"""
accel_eval_list = ['AccelX', 'AccelY', 'AccelZ', 'AccelLoad', 'Accel_3D', 'Speed']

for i in accel_eval_list:
    list_of_holding = []
    for j in range(len(even_more_all_data_games_dummies)):
        if even_more_all_data_games_dummies[i].iloc[j] >= even_more_all_data_games_dummies[i]

"""







