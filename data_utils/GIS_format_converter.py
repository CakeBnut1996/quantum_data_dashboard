import geopandas as gpd
from shapely.geometry import Point
import pandas as pd


def csv_to_geojson(filepath,outpath):
    df = pd.read_csv(filepath, encoding="ISO-8859-1")
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df.dropna(subset=['Latitude', 'Longitude'])

    df = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df['Longitude'], df['Latitude'])],
                               crs="EPSG:4326")
    df.to_file(outpath, driver="GeoJSON")
