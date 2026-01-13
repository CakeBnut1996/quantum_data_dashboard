from data_utils.data_from_web_converter import find_flourish_id, dump_raw_flourish_text,decode_and_export_flourish

url = "https://www.csis.org/analysis/innovation-lightbulb-us-federal-investments-quantum-technology-research-and-infrastructure"
v_id = find_flourish_id(url)
raw_filepath = "data_map/quantum data center/quantum_raw.txt"
dump_raw_flourish_text(v_id, raw_filepath)
out_filepath = "data_map/quantum data center/quantum_data_center.csv"
# Assuming you saved the previous dump to a file:
decode_and_export_flourish(raw_filepath,out_filepath)