#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 19:20:16 2022

@author: rachelspady
"""
import numpy as np
import pandas as pd
import os, re, struct

# Data Visualization
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
from pylab import *
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'
wvideos=pd.read_csv('watchedVideo.csv')
videos=pd.read_csv('videos.csv')
users=pd.read_csv('users.csv')
feeds=pd.read_csv('feeds.csv')

#mapping coords
lat = []
lon = []

# For each row in a varible,
for row in users['coordinates']:
    # Try to,
    try:
        # Split the row by comma and append
        # everything before the comma to lat
        lat.append(row.split(',')[0])
        # Split the row by comma and append
        # everything after the comma to lon
        lon.append(row.split(',')[1])
    # But if you get an error
    except:
        # append a missing value to lat
        lat.append(np.NaN)
        # append a missing value to lon
        lon.append(np.NaN)

# Create two new columns from lat and lon
users['latitude'] = lat
users['latitude'] = users['latitude'].str[2:]
users['latitude'] = users['latitude'].str[:-1]
users['longitude'] = lon
users['longitude'] =users['longitude'].str[2:]
users['longitude'] =users['longitude'].str[:-2]
users['longitude'] = pd.to_numeric(users['longitude'])
users['latitude'] = pd.to_numeric(users['latitude'])


fig = px.scatter_mapbox(users[users['class'] == 'Creator'], lat='latitude', lon='longitude', hover_name='class', hover_data=['created_at'], color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig2 = px.scatter_mapbox(users[users['class'] == 'Super Creator'], lat='latitude', lon='longitude', hover_name='class', hover_data=['created_at'], color_discrete_sequence=["blue"], zoom=3, height=300)
fig3 = px.scatter_mapbox(users[users['class'] == 'Super Gamer'], lat='latitude', lon='longitude', hover_name='class', hover_data=['created_at'], color_discrete_sequence=["green"], zoom=3, height=300)
fig4 = px.scatter_mapbox(users[users['class'] == 'Gamer'], lat='latitude', lon='longitude', hover_name='class', hover_data=['created_at'], color_discrete_sequence=["red"], zoom=3, height=300)
fig5 = px.scatter_mapbox(users[users['class'] == 'Viewer'], lat='latitude', lon='longitude', hover_name='class', hover_data=['created_at'], color_discrete_sequence=["yellow"], zoom=3, height=300)
fig.add_trace(fig2.data[0])
fig.add_trace(fig3.data[0])
fig.add_trace(fig4.data[0])
fig.add_trace(fig5.data[0])
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()
#this may not work if you have certain javascript blocked or some firewalls.
fig.write_html("mapofusers")
#is there correlation between video duration and shares
plt.scatter(videos['duration'], videos['num_shares'])
# Giving the title for the plot
plt.title("Duration vs Number of Shares")
# Namimg the x and y axis
plt.xlabel('Duration')
plt.ylabel('Number of Shares')
# Saving the plot as a 'png'
plt.savefig('DurationNumberShares.png')
# Displaying the bar plot
plt.show()

rforallvideos = np.corrcoef(videos['duration'], videos['num_shares'])
#there is not r = .0320
#is there correlation between video duration and shares when using AR
plt.figure() 
plt.scatter(videos['duration'][videos['is_ar']==True], videos['num_shares'][videos['is_ar']==True])
rforARvideos = np.corrcoef(videos['duration'][videos['is_ar']==True], videos['num_shares'][videos['is_ar']==True])
numberARvids = videos[videos['is_ar']==True].count()
#there is not r = .0421, number is 2528, 50.56%
#AR videos
#is there correlation between video duration and shares when not using AR
plt.figure() 
plt.scatter(videos['duration'][videos['is_ar']==False], videos['num_shares'][videos['is_ar']==False])
rfornotARvideos = np.corrcoef(videos['duration'][videos['is_ar']==False], videos['num_shares'][videos['is_ar']==False])
#there is not r = .0215
unique = videos.nunique()
df = pd.DataFrame()
df = videos.groupby('creator')['id'].nunique()
df =df.to_frame()
df.reset_index(inplace=True)
df.columns = ['id', 'vidcount']

df = df.merge(users)
df.rename(columns = {'id':'userId'}, inplace = True)
wvideos['dateTime']= pd.to_datetime(wvideos['dateTime'])
wvideos['day'] = wvideos['dateTime'].dt.day_name()
df = df.merge(wvideos,on = 'userId')
wvideos['OSindicator'] = np.where(wvideos['os'] == 'Android',0,1)
rforioswatches = np.corrcoef(wvideos['duration'],wvideos['OSindicator'])
#no correlation between OS and watch duration
#figure out usership pattern across days:


plt.figure() 
figure(figsize=(12, 6), dpi=120)
plt.hist(df['dateTime'],bins = 20)
# Giving the title for the plot
plt.title("Number of Videos Watched By Day of Year")
# Namimg the x and y axis
plt.xlabel('Day of Year')
plt.ylabel('Number of Videos Watched')
# Saving the plot as a 'png'
plt.savefig('WatchedDayOfYear.png')
# Displaying the bar plot
plt.show()

wvideos.reset_index(inplace=True)
df1 = wvideos.groupby('day')['index'].nunique()
df1 =df1.to_frame()
df1.reset_index(inplace=True)
df1.columns = ['day', 'Number of plays']
plt.figure() 

plt.bar(df1['day'],df1['Number of plays'])
# Giving the title for the plot
plt.title("Number of Videos Watched By Day of Week")
# Namimg the x and y axis
plt.xlabel('Day of Week')
plt.ylabel('Number of Videos Watched')
# Saving the plot as a 'png'
plt.savefig('WatchedDayOfWeek.png')
# Displaying the bar plot
plt.show()
