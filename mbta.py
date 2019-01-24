import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
from collections import OrderedDict

r = requests.get('https://api-v3.mbta.com/stops?filter[route_type]=1', headers={'api_key':'17635449db9d4d41a6cd765ad49ab78e'})

stops = OrderedDict()

for item in r.json()['data']:
    description = item['attributes']['description']
    name = description.split('-')[0]
    line = description.split('-')[1]
    if name not in stops.keys():
        entry = {}
        entry['line'] = line
        entry['lat'] = item['attributes']['latitude']
        entry['lon'] = item['attributes']['longitude']
        entry['geometry'] = Point(entry['lon'], entry['lat'])
        stops[name] = entry

df = pd.DataFrame.from_dict(stops, orient='index')

street_map = gpd.read_file('shapefile/bos_land.shp')
street_map = street_map.to_crs({'init': 'epsg:4326'})
fig, ax = plt.subplots(figsize=(15, 15))
street_map.plot(ax=ax, alpha=0.4, color="grey")
crs = {'init': 'epsg:4326'}

geometry = [row['geometry'] for idx, row in df.iterrows()]

geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

geo_df[geo_df['line'].str.contains('Red Line')==True].plot(ax=ax, markersize=20, color="red", marker="o", label="Red Line")
geo_df[geo_df['line'].str.contains('Blue Line')==True].plot(ax=ax, markersize=20, color="blue", marker="o", label="Blue Line")
geo_df[geo_df['line'].str.contains('Orange Line')==True].plot(ax=ax, markersize=20, color="orange", marker="o", label="Orange Line")

plt.legend(prop={'size': 15})
plt.show()
