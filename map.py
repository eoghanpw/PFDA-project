import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Ireland map coordinates.
# https://data-osi.opendata.arcgis.com/datasets/osi::counties-national-statutory-boundaries-2019-generalised-20m/about
file_path = '''./data/Counties___OSi_National_Statutory_Boundaries
___Generalised_20m_-6920972630406172930.geojson'''

# Import to geopandas dataframe.
# https://datascience.quantecon.org/tools/maps.html#get-the-map
# https://geopandas.org/en/latest/docs/user_guide/fiona_to_pyogrio.html#migration-from-the-fiona-to-the-pyogrio-read-write-engine
ireland = gpd.read_file(file_path, engine='pyogrio')

# Weather station coordinates.
# https://cli.fusio.net/cli/climate_data/webdata/StationDetails.csv
station_details = './data/met_eireann_station_details.csv'

# Import to dataframe.
stations = pd.read_csv(station_details)

# Add coordinates to dataframe.
# https://datascience.quantecon.org/tools/maps.html#id1
stations['coordinates'] = list(zip(stations.longitude, stations.latitude))
stations['coordinates'] = stations['coordinates'].apply(Point)

# Create geopandas dataframe for stations.
station_df = gpd.GeoDataFrame(stations, geometry='coordinates')

# Ensure station coordinates line up with ireland map when plotting.
# https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.set_crs.html
station_df = station_df.set_crs(4326, allow_override=True)

# Plot the map.
# https://geopandas.org/en/stable/docs/user_guide/mapping.html#maps-with-layers
# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 10))
base = ireland.plot(ax=ax, edgecolor='gray', color='green', alpha=0.5)
station_df.plot(ax=base, marker='*', color='red')
ax.set_title('Met Eireann Synoptic Weather Stations')

# Remove spines and axes.
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

# Label the stations.
for x, y, label in zip(station_df['coordinates'].x,
                       station_df['coordinates'].y, station_df['name']):
    ax.annotate(label, xy=(x, y), xytext=(4, -2),
                textcoords='offset points', size='x-small', weight='bold')
plt.show()
