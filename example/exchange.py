#%% md

TODO: chapter numbers

# Data Analysis

1. 2019 vs 2020 differences
2. Prediction of Severity with traffic data [day, time, state??]

---
## 1 Imports
### 1.1 Libraries

#%%

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sns

#%% md

### 1.2 Data

#%%

file_path = './US_Accidents_Dec20_updated.csv'

# If file exists
if os.path.isfile(file_path):
    data_ori = pd.read_csv(file_path)
else:
    # TODO: insert code to download file
    pass
"""
PATH_HOME = os.getcwd()
PATH_DATA = os.path.join(PATH_HOME, "data")
PATH_OUTPUT = os.path.join(PATH_HOME, "output")
filename = os.path.join(PATH_DATA, "amazon_electronics.json")
if not os.path.exists(filename):
    display("Reading from URL..")
    df_amz = pd.read_json("https://www.dropbox.com/s/o9jxaeax4mascd3/Electronics_5.json?dl=1", lines = True)
    if not os.path.exists(PATH_DATA):
        os.mkdir(PATH_DATA)
    df_amz.to_pickle(filename)

else:
    display("Reading from hard drive..")
    df_amz = pd.read_pickle(filename)

df_amz.head()
"""

#%% md

---
## 2 Definitions

#%%
#all parameters in original data

column_list = [
    'ID',
    'Severity',
    'Start_Time',
    'End_Time',
    'Start_Lat',
    'Start_Lng',
    'End_Lat',
    'End_Lng',
    'Distance(mi)',
    'Description',
    'Number',
    'Street',
    'Side',
    'City',
    'County',
    'State',
    'Zipcode',
    'Country',
    'Timezone',
    'Airport_Code',
    'Weather_Timestamp',
    'Temperature(F)',
    'Wind_Chill(F)',
    'Humidity(%)',
    'Pressure(in)',
    'Visibility(mi)',
    'Wind_Direction',
    'Wind_Speed(mph)',
    'Precipitation(in)',
    'Weather_Condition',
    'Amenity',
    'Bump',
    'Crossing',
    'Give_Way',
    'Junction',
    'No_Exit',
    'Railway',
    'Roundabout',
    'Station',
    'Stop',
    'Traffic_Calming',
    'Traffic_Signal',
    'Turning_Loop',
    'Sunrise_Sunset',
    'Civil_Twilight',
    'Nautical_Twilight',
    'Astronomical_Twilight'
]

# defining all columns in original data with numeric values
numeric_columns = [
    'Severity',
    'Start_Lat',
    'Start_Lng',
    'End_Lat',
    'End_Lng',
    'Distance(mi)',
    'Number',
    'State',
    'Zipcode',
    'Temperature(F)',
    'Wind_Chill(F)',
    'Humidity(%)',
    'Pressure(in)',
    'Visibility(mi)',
    'Wind_Speed(mph)',
    'Precipitation(in)'
]

# defining wind values for value transformation (section 5.4.4)
wind_values = {
    'North': 'N',
    'South': 'S',
    'West': 'W',
    'East': 'E',
    'Calm': 'CALM',
    'Variable': 'VAR',
}

#%% md

---
## 3 Data Overview

#%%

# Shape of data
data_ori.shape

#%%

# Types
data_ori.dtypes


#%%

# Features
list(data_ori)  # What potential lies in the "Description"? (?@luke)

#%%

# Head
data_ori.head()

#%%

# Descriptions
data_ori.describe()

#%% md

---
## 5 Data Cleaning

Number, Temperature(F)	Wind_Chill(F)	Humidity(%)	Pressure(in)	Visibility(mi)	Wind_Speed(mph)	Precipitation(in)

#%%

# display all value counts -> length: counts unique values
for column in column_list:  # list of columns
    print(data_ori[column].value_counts().sort_index(), "\n")



#%% md

### 5.1 Drop columns
Dropping irrelevant columns.

Reasons:
    Description - contains unstructured text data (with typos) which contains information such as address/ zipcode which
    are already present in the data set. Other information in this column such as exact names, details of those involved
    etc are unimportant for our current project.

    Number, Precipitation - too many NaN values, others mostly 0. Weather data already included in another column.

    Turning_Loop - all values are 'False'. Will not make any change to model.

    Timezone - our analysis will be based on local time. Timezone does not have any effect on accidents.

    Airport_Code - Location of accident already included in data set. Airport code unimportant.

    Weather_Timestamp - shows us exact time of weather measurement which all match day of accident. Unimportant for now.

    Wind_Chill(F) - We already have weather data. Wind chill is calculated using temperature and wind speed which we
                    already have in dataset. Affect of wind on skin is unimportant for accident rates.


#%%

columns_to_drop = [
    'Description',
    'Number',
    'Precipitation(in)',
    'Turning_Loop',
    'Timezone',
    'Airport_Code',
    'Weather_Timestamp',
    'Wind_Chill(F)'
]

data_ori.drop(columns=columns_to_drop, inplace=True)  # inplace -> no need to store result in new variable

#%% md

### 5.2 Drop missing values

#%%

#TODO: Check for non and then drop



#%% md

### 5.3 Drop incorrect values

#%%

# TODO: explain why dropping these values (extreme temp/wind)

# Extreme Temperature -> 5 values
data_ori.drop(data_ori[(data_ori['Temperature(F)'] >= 168.8) | (data_ori['Temperature(F)'] <= -77.8)].index,
              inplace=True)

# Extreme Wind_Speed -> 6 values
data_ori.drop(data_ori[data_ori['Wind_Speed(mph)'] >= 471.8].index, inplace=True)

#%% md

### 5.4 Value Transformation

#### 5.4.1 Zip Code

#%%

# TODO: explanation
data_ori['Zipcode'] = data_ori['Zipcode'].str[:5]  # take first 5 digits of zip code -> save it in column again


#%% md

#### 5.4.2 Unit conversion to SI units

TODO: (Luke) fil End_lat and End_Lng by Start_Lat and Start_Lng (check prior what is the average difference between the two)


#%%

# Distance miles -> kilometres
data_ori['Distance(km)'] = data_ori['Distance(mi)'] * 1.609

# Temperature F -> C
data_ori['Temperature(C)'] = (data_ori['Temperature(F)'] - 32) / 1.8

# Wind_Speed mi/h -> km/h
data_ori['Wind_Speed(kmh)'] = data_ori['Wind_Speed(mph)'] * 1.609

# Visibility mi -> km
data_ori['Visibility(km)'] = data_ori['Visibility(mi)'] * 1.609

# Pressure Pa -> in
data_ori['Pressure(Pa)'] = data_ori['Pressure(in)'] / 29.92

columns_to_drop = [
    'Distance(mi)',
    'Temperature(F)',
    'Wind_Speed(mph)',
    'Visibility(mi)',
    'Pressure(in)'
]

data_ori.drop(columns=columns_to_drop, inplace=True)

#%% md

#### 5.4.3 Timestamp transformation
TODO: explain

#%%

data_ori['Start_Time'] = pd.to_datetime(data_ori['Start_Time'])

data_ori['Weekday'] = data_ori['Start_Time'].dt.dayofweek  # Monday = 0
data_ori['Month'] = data_ori['Start_Time'].dt.month  # Monday = 0
data_ori['Hour'] = data_ori['Start_Time'].dt.hour  # Monday = 0

#%% md

#### 5.4.4 Wind direction transformation
TODO: explain

#%%

data_ori["Wind_Direction"].replace(wind_values, inplace=True)

#%% md

### 5.5 Set Data Types

#%%

data_prep = data_ori

#%% md

---
## 6 Exploratory Data Analysis
### 6.1 Univariate Non-Graphical

describe data again

idea: What learnings can be drawn for your own driving behaviour? When is the most dangerous time? What is the most
what is the most dangerous weather? Which is the most dangerous state? How strong is the correlation between accidents
and the population density? What are the safest types of crossings? Where is the most dangerous place in the US?
difference weekday/weekend
differentiate between corona and pre-corona times; include apple mobility data https://covid19.apple.com/mobility

#%%

# display all value counts
for column in data_prep:  # list of columns
    print(data_prep[column].value_counts().sort_index(), "\n")

#%%

# display data types
data_prep.dtypes

#%%

# describe numerical columns
data_prep.describe()

#%%



#%%



#%%



#%%



#%%



#%% md

### 6.2 Univariate Graphical

#%%

# ideas: qq plots, histograms, barplots,

for column in:  # list of columns
    fig, ax = plt.subplots(1, 1, figsize=(15, 6))
    sns.countplot(y=data_prep[column][1:], data=data_prep.iloc[1:], order=data_prep[column][1:].value_counts().index,
                  palette='Blues_r')
    fig.text(0.1, 0.95, column, fontsize=16, fontweight='bold', fontfamily='serif')
    plt.xlabel('', fontsize=20)
    plt.ylabel('')
    plt.yticks(fontsize=13)
    plt.box(False)

#%%

# histogram of accidents of the biggest cities
data_prep.City.value_counts()[:20].plot(kind='bar')

#%%

# histogram of accidents according to the weather condition (how to standardize?)
data_prep.Weather_Condition.value_counts().plot(kind='bar')

#%%

# histogram of accidents according to time of day

#%%

# histogram of accidents filtered by state
data_prep.State.value_counts().plot(kind='bar')

#%%

# pie diagram on severity
data_prep.Severity.value_counts().plot.pie()
# pie diagram on severity if the weather is poor (wind > threashold, rain > threshold)

#%%

# average duration (densityfunction)

#%%

# barplot of the connection between severity and distance

#%%



#%%



#%%



#%% md

### 6.3 Multivariate Non-Graphical

#%%

# correlation matrices and PCA??
data_prep.corr(method='spearman')

#%% md

### 6.4 Multivariate Graphical

#%%

# to be adjusted:
fig = plt.gcf()
fig.set_size_inches(20, 20)
fig = sns.heatmap(data_prep.corr(), annot=True, linewidths=1, linecolor='k', square=True, mask=False, vmin=-1, vmax=1,
                  cbar_kws={"orientation": "vertical"}, cbar=True)
sns.set(style='ticks')
sns.pairplot(data_prep)

# US map simple: scatterplot based on latitude and longitude data, with correct alpha, to show densitiy
sns.jointplot(x=data_prep.Start_Lng.values, y=data_prep.Start_Lat.values, height=8)
plt.ylabel('Start_Lat', fontsize=12)
plt.xlabel('Start_Lng', fontsize=12)
plt.show()
# ideas: A MAP of the US, showing the accident intensity for each place by colour
# https://runestone.academy/runestone/books/published/httlads/WorldFacts/cs1_graphing_infant_mortality.html


#%% md

---
## 7 Feature Engineering
### 7.1 Type Conversion

duration
TMC: NA is an important information

#%%



#%% md

### 7.2 Transformation

#%%



#%% md

---
## 8 Model
### 8.1 Partitioning the Data

#%%



#%% md

### 8.2 Sampling

#%%



#%% md

### 8.3 ""Model""

#%%

# How much does the inclusion of apples mobility value increase the accurancy of our prediction model?
# LSTM-GBRT https://downloads.hindawi.com/journals/jcse/2020/4206919.pdf
# hybrid K-means and random forest https://link.springer.com/content/pdf/10.1007/s42452-020-3125-1.pdf
# OCT https://towardsdatascience.com/using-machine-learning-to-predict-car-accidents-44664c79c942
# Regression-kriging https://carto.com/blog/predicting-traffic-accident-hotspots-with-spatial-data-science/


#%% md

### 8.4 Testing

#%% md

### 8.5 Prediction driving factors

# SHAP diagram



