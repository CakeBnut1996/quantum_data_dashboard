import geopandas as gpd
import pyproj
import pandas as pd
from shapely.geometry import Point
import base64
import os
import matplotlib.pyplot as plt

transformer = pyproj.Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)

def csv_to_geojson(filepath,outpath):
    df = pd.read_csv(filepath, encoding="ISO-8859-1")
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df.dropna(subset=['Latitude', 'Longitude'])

    df = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df['Longitude'], df['Latitude'])],
                               crs="EPSG:4326")
    df.to_file(outpath, driver="GeoJSON")


def csv_to_transparent_png(filepath, out_png_path):
    df = pd.read_csv(filepath, encoding="ISO-8859-1").dropna(subset=['Latitude', 'Longitude'])

    # 2. Filter for Mainland US (Standard Lat/Lon)
    df = df[(df['Longitude'] > -130) & (df['Longitude'] < -65) & (df['Latitude'] > 24) & (df['Latitude'] < 50)]

    # 3. Project coordinates to Web Mercator
    # This transforms degrees into meters used by the basemap
    df['x'], df['y'] = transformer.transform(df['Longitude'].values, df['Latitude'].values)

    # 4. Get the new Mercator bounds
    west, east = df['x'].min(), df['x'].max()
    south, north = df['y'].min(), df['y'].max()

    # 5. Create figure matching the new projected aspect ratio
    geo_aspect = (north - south) / (east - west)
    fig = plt.figure(figsize=(5, 5 * geo_aspect), frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # 6. Plot the projected coordinates
    ax.scatter(df['x'], df['y'], c='red', s=5, alpha=0.8, edgecolors='none')
    ax.set_xlim(west, east)
    ax.set_ylim(south, north)

    plt.savefig(out_png_path, transparent=True, dpi=200, pad_inches=0)
    plt.close()

    # IMPORTANT: Your metadata MUST still use the ORIGINAL lat/lon for Plotly to place it
    return {
        "west": west, # df['Longitude'].min(),
        "east": east, #df['Longitude'].max(),
        "south": south, # df['Latitude'].min(),
        "north": north # df['Latitude'].max()
    }

def get_image_base64(relative_path):
    if os.path.exists(relative_path):
        with open(relative_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    return None