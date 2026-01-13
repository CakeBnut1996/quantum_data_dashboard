import os
from data_utils.GIS_format_converter import csv_to_geojson

data_dir = r"C:\Users\mmh\Documents\quantum\data_map"
data_center = os.path.join(data_dir,"data center","Q2 2025 451 Research Datacenter KnowledgeBase_GLOBAL.csv")
data_center_json = os.path.join(data_dir,"data center","data_center_all.geojson")
csv_to_geojson(data_center,data_center_json)


quantum_center = os.path.join(data_dir,"quantum data center","quantum_data_center.csv")
quantum_center_json = os.path.join(data_dir,"quantum data center","quantum_data_center.geojson")
csv_to_geojson(quantum_center,quantum_center_json)
