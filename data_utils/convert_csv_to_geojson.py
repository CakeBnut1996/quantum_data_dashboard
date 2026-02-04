import os, json, importlib
import pandas as pd
import data_utils.GIS_format_converter
importlib.reload(data_utils.GIS_format_converter )
from data_utils.GIS_format_converter import csv_to_geojson, csv_to_transparent_png

data_dir = r"C:\Users\mmh\Documents\quantum\data_map"
data_center = os.path.join(data_dir,"data center","Q2 2025 451 Research Datacenter KnowledgeBase_GLOBAL.csv")
data_center_df = pd.read_csv(data_center)
data_center_df = data_center_df[data_center_df["Country "]=="USA"] # space!!
data_center_df.to_csv(os.path.join(data_dir,"data center","Q2 2025 451 Research Datacenter KnowledgeBase_USA.csv"),index=False)

data_center = os.path.join(data_dir,"data center","Q2 2025 451 Research Datacenter KnowledgeBase_USA.csv")
df = pd.read_csv(data_center)
data_center_json = os.path.join(data_dir,"data center","data_center_all.geojson")
csv_to_geojson(data_center,data_center_json)
data_center_png = os.path.join(data_dir,"data center","data_center_all.png")
metadata = csv_to_transparent_png(data_center,data_center_png)
# with open(os.path.join(data_dir,"data center","bounds.json"), "w") as f:
#     json.dump(metadata, f)

quantum_center = os.path.join(data_dir,"quantum data center","quantum_data_center.csv")
df = pd.read_csv(quantum_center)
quantum_center_json = os.path.join(data_dir,"quantum data center","quantum_data_center.geojson")
csv_to_geojson(quantum_center,quantum_center_json)
