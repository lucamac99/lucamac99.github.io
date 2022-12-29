import gpxpy
import pandas as pd
import folium
from math import radians, sin, cos, sqrt, atan2
import geopandas as gpd
import pandas as pd
import numpy as np
import movingpandas as mpd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import time
import warnings
warnings.filterwarnings('ignore')

def plot_tracks(df): 
    trial_df, trial_points = process_gpx_to_df(df.iloc[0:1])

    mymap = folium.Map( location=[ trial_df.Latitude.mean(), trial_df.Longitude.mean() ], zoom_start=6, tiles=None)
    folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(mymap)
    folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC', name='Nat Geo Map').add_to(mymap)
    folium.TileLayer('http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg', attr='terrain-bcg', name='Terrain Map').add_to(mymap)
    folium.PolyLine(trial_points, color='red', weight=4.5, opacity=.5).add_to(mymap)
    # start from the second row
    for i in range(1, len(df)):
        try:
            gpx_df, points = process_gpx_to_df(df.iloc[i:i+1])
            folium.PolyLine(points, color='red', weight=4.5, opacity=.5).add_to(mymap)
        except:
            print(i)
            continue
    
    return mymap

def process_gpx_to_df(hike):
    gpx = gpxpy.parse(hike['gpx'].values[0])
 
    #(1)make DataFrame
    track = gpx.tracks[0]
    segment = track.segments[0]
    # Load the data into a Pandas dataframe (by way of a list)
    data = []
    segment_length = segment.length_3d()
    for point_idx, point in enumerate(segment.points):
        data.append([point.longitude, point.latitude,point.elevation,
    point.time, segment.get_speed(point_idx), hike['user'].values[0]])
    columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed', 'User']
    gpx_df = pd.DataFrame(data, columns=columns)

    df_gpx = gpx_df.set_index('Time')
    
    #2(make points tuple for line)
    points = []
    for track in gpx.tracks:
        for segment in track.segments: 
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
    
    return df_gpx, points

def get_start_end_points(hike):
    gpx = gpxpy.parse(hike['gpx'])
 
    #(1)make DataFrame
    track = gpx.tracks[0]
    segment = track.segments[0]
    # Load the data into a Pandas dataframe (by way of a list)
    data = []
    for point_idx, point in enumerate(segment.points):
        data.append([point.longitude, point.latitude,point.elevation,
    point.time, segment.get_speed(point_idx)])

    start_point = data[0]
    end_point = data[-1]
    
    return start_point, end_point

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    # Calculate the distance using the Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # 6371 is the radius of the Earth in kilometers
    
    return distance

def distance3d_min_10m(lat1, lon1, alt1, lat2, lon2, alt2):
    # Calculate the 2D distance between the points using the Haversine formula
    distance2d = haversine(lat1, lon1, lat2, lon2)
    
    # Calculate the 3D distance using the Pythagorean theorem
    distance3d = sqrt(distance2d**2 + (alt2 - alt1)**2)
    
    return distance3d <= 10

def distance3d_min_10000m(lat1, lon1, alt1, lat2, lon2, alt2):
    # Calculate the 2D distance between the points using the Haversine formula
    distance2d = haversine(lat1, lon1, lat2, lon2)
    
    # Calculate the 3D distance using the Pythagorean theorem
    distance3d = sqrt(distance2d**2 + (alt2 - alt1)**2)
    
    return distance3d <= 10000

def toGdfList(activities_dfList) -> list:

    target_gdfList = []
    for i in tqdm(range(len(activities_dfList))):
        geo_df = gpd.GeoDataFrame(activities_dfList[i], crs=4326, geometry=gpd.points_from_xy(activities_dfList[i].Longitude, activities_dfList[i].Latitude, activities_dfList[i].Altitude))      
        target_gdfList.append(geo_df)

    return target_gdfList