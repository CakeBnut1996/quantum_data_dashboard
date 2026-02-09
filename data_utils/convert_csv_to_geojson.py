import os, json, importlib
import pandas as pd
import data_utils.GIS_format_converter
importlib.reload(data_utils.GIS_format_converter )
from data_utils.GIS_format_converter import csv_to_geojson, csv_to_parquet, upload_parquet_to_motherduck
data_dir = r"C:\Users\mmh\Documents\quantum\data_map"

data_center = os.path.join(data_dir,"data center","Q2 2025 451 Research Datacenter KnowledgeBase_GLOBAL.csv")
data_center_df = pd.read_csv(data_center)
data_center_df = data_center_df[data_center_df["Country "]=="USA"] # space!!
data_center_df.to_csv(os.path.join(data_dir,"data center","Q2 2025 451 Research Datacenter KnowledgeBase_USA.csv"),index=False)

data_center = os.path.join(data_dir,"data center","data_center_all.csv")
df = pd.read_csv(data_center)
# data_center_json = os.path.join(data_dir,"data center","data_center_all.geojson")
# csv_to_geojson(data_center,data_center_json)
data_center_parquet = os.path.join(data_dir, "data center", "data_center_all.parquet")
csv_to_parquet(data_center, data_center_parquet)
upload_parquet_to_motherduck(data_center_parquet, "data_center_all")

quantum_center = os.path.join(data_dir,"quantum data center","quantum_data_center.csv")
df = pd.read_csv(quantum_center)
# quantum_center_json = os.path.join(data_dir,"quantum data center","quantum_data_center.geojson")
# csv_to_geojson(quantum_center,quantum_center_json)
quantum_center_parquet = os.path.join(data_dir, "quantum data center", "quantum_data_center.parquet")
csv_to_parquet(quantum_center, quantum_center_parquet)
upload_parquet_to_motherduck(quantum_center_parquet, "quantum_data_center")