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















