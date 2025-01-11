# Let's plot the weather stations on the map.
# References:
# https://datascience.quantecon.org/tools/maps.html#get-the-map
# https://data-osi.opendata.arcgis.com/datasets/osi::counties-national-statutory-boundaries-2019-generalised-20m/about

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Ireland map coordinates.
file_path = "./data/Counties___OSi_National_Statutory_Boundaries___Generalised_20m_-6920972630406172930.geojson"

# Import to geopandas dataframe.
# https://geopandas.org/en/latest/docs/user_guide/fiona_to_pyogrio.html#migration-from-the-fiona-to-the-pyogrio-read-write-engine
ireland = gpd.read_file(file_path, engine="pyogrio")

# Weather station coordinates.
station_details = "./data/met_eireann_station_details.csv"

# Import to dataframe.
stations = pd.read_csv(station_details)

# Add coordinates to dataframe.
# https://datascience.quantecon.org/tools/maps.html#id1
stations["coordinates"] = list(zip(stations.longitude, stations.latitude))

stations["coordinates"] = stations["coordinates"].apply(Point)

# Create geopandas dataframe for stations.
station_df = gpd.GeoDataFrame(stations, geometry="coordinates")

# Ensure station coordinates line up with ireland map when plotting.
# https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.set_crs.html
station_df = station_df.set_crs(4326, allow_override=True)

# Plot the map.
# https://geopandas.org/en/stable/docs/user_guide/mapping.html#maps-with-layers
fig, gax = plt.subplots(figsize=(10, 10))

base = ireland.plot(ax=gax, edgecolor='gray', color='green', alpha=0.5)

station_df.plot(ax=base, marker='*', color='red')

gax.set_title('Met Eireann Synoptic Weather Stations')

# Remove spines and axes.
gax.spines['top'].set_visible(False)
gax.spines['bottom'].set_visible(False)
gax.spines['right'].set_visible(False)
gax.spines['left'].set_visible(False)

plt.gca().set_xticks([])
plt.gca().set_yticks([])

# Label the stations.
for x, y, label in zip(station_df['coordinates'].x, station_df['coordinates'].y, station_df['name']):
    gax.annotate(label, xy=(x, y), xytext=(4, -2), textcoords='offset points', size='x-small', weight='bold')

plt.show()
