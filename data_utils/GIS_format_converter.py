import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from pathlib import Path
import duckdb

def csv_to_geojson(filepath,outpath):
    df = pd.read_csv(filepath, encoding="ISO-8859-1")
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df.dropna(subset=['Latitude', 'Longitude'])

    df = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df['Longitude'], df['Latitude'])],
                               crs="EPSG:4326")
    df.to_file(outpath, driver="GeoJSON")


def csv_to_parquet(csv_filepath, parquet_outpath):
    """
    Converts CSV to Parquet while cleaning coordinates.
    Best for MotherDuck uploads.
    """
    # Load with your specific encoding
    df = pd.read_csv(csv_filepath, encoding="ISO-8859-1")

    # Clean data (matching your existing logic)
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Save to Parquet
    # This preserves the float type for Latitude/Longitude perfectly
    df.to_parquet(parquet_outpath, index=False)
    print(f"Created Parquet file: {parquet_outpath}")
    return parquet_outpath


def upload_parquet_to_motherduck(parquet_path, table_name):
    """
    Uploads a Parquet file to MotherDuck.
    Much faster and more reliable than CSV.
    """
    abs_path = str(Path(parquet_path).resolve())
    con = duckdb.connect("md:my_db")

    try:
        # No 'sniffing' needed for Parquet!
        con.execute(f"CREATE OR REPLACE TABLE main.{table_name} AS SELECT * FROM '{abs_path}'")
        print(f"Successfully uploaded {table_name} to MotherDuck via Parquet.")
    except Exception as e:
        print(f"Parquet Upload Error: {e}")