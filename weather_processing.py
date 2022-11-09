"""
Created on Mon Feb  7 14:10:42 2022

@author: Okhrimchuk Roman
for Sierentz Global Merchants

Test task
"""

# TODO Import the necessary libraries
import pandas as pd
import numpy as np
import datetime

# TODO Import the dataset

path = r'./data/weather_dataset.data'

# TODO  Assign it to a variable called data and replace the first 3 columns by a proper datetime index
data = pd.read_csv(path, index_col=False, sep="\s+", dtype={'Yr': str, 'Mo': str, 'Dy': str})
data['full_data'] = data['Dy'] + '-' + data['Mo'] + '-' + data['Yr']
data = data.set_index(['full_data'])
data = data.drop(columns=['Yr', 'Mo', 'Dy'])

# TODO Check if everything is okay with the data. Create functions to delete/fix rows with strange cases and apply them
# replace comas whis dots for further possible convertation to float
data = data.apply(lambda x: x.str.replace(',', '.'))
# convert values from string to float (including empty records)
for column in data.columns:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# check values for outliers
# here we  can see, that, for example, in column loc9 range of values seems to be enormous
# also it doesn't seem to be a realistic wind speed
# so there are outliers in the data, that need to be removed
print('data before removing outliers \n', data.describe().loc[['min', 'max', 'mean', 'std']])

# remove rows with outliers
standard_deviations = 3


def not_outliers_mask(column_values, standard_deviations):
    return np.abs(column_values - column_values.mean()) / column_values.std() < standard_deviations


data_without_outliers = data[data.apply(lambda x: not_outliers_mask(x, standard_deviations)).all(axis=1)]

# compare with the same statistic above - difference is visible

print('data after removing outliers \n', data_without_outliers.describe().loc[['min', 'max', 'mean', 'std']])


# TODO Write a function in order to fix date (this relate only to the year info) and apply it
# TODO Set the right dates as the index. Pay attention at the data type, it should be datetime64[ns]
def fix_year(x):
    if x.year > 2000:
        year = x.year - 100
    else:
        year = x.year
    return datetime.datetime(year, x.month, x.day)


data_without_outliers.index = pd.to_datetime(data_without_outliers.index)
data_without_outliers.index = data_without_outliers.index.map(fix_year)

print('updated datetime indexes \n', data_without_outliers.index)

# TODO Compute how many values are missing for each location over the entire record
# missing values where removed while processing data and deleting outliers, so here we check "raw" data
print('number of empty values in "raw" data \n', data.isna().sum().to_frame().T)

# TODO Compute how many non-missing values there are in total
print('number of non-empty values in "raw" data : ', data.notnull().sum().sum())

# TODO Calculate the mean windspeeds of the windspeeds over all the locations and all the times
print('mean windspead over all locations and all times : ',  data_without_outliers.mean().mean())

# TODO Create a DataFrame called loc_stats and calculate the min, max and mean windspeeds and standard deviations of the windspeeds at each location over all the days
loc_stats = data_without_outliers.describe().loc[['min', 'max', 'mean', 'std']]
print('statistics via loc_stats\n', loc_stats)

# TODO Find the average windspeed in January for each location
date_mask = data_without_outliers.index.month == 1
data_upp_new_january = data_without_outliers[date_mask]
print('average windspeed in January for each location\n', data_upp_new_january.mean().to_frame().T)

# TODO Downsample the record to a yearly frequency for each location
print('downsampled record via yearly frequency for each location\n',
      data_without_outliers.resample('Y', label='right').mean())

# TODO Downsample the record to a monthly frequency for each location
print('downsampled record via monthly frequency for each location\n',
      data_without_outliers.resample('M', label='right').mean())

# TODO Downsample the record to a weekly frequency for each location
print('downsampled record via weekly frequency for each location\n',
      data_without_outliers.resample('W', label='right').mean())

# TODO Calculate the min, max and mean windspeeds and standard deviations of the windspeeds across all locations for each week (assume that the first week starts on January 2 1961) for the first 21 weeks
data_used = data_without_outliers[data_without_outliers.index > '1961-01-02']
data_used_weeks = data_used.resample('W', label='right').mean().iloc[:21, :]
print('statistic for fist 21 weeks since 2 January 1968 \n',
      data_used_weeks.describe().loc[['min', 'max', 'mean', 'std']])
