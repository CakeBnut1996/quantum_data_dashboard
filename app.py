# File: src_streamlit/app.py
import streamlit as st
from src_streamlit.quantum_data_loader import (
    get_display_text, get_barchart_data, get_map_layers_data, get_map_styles
)
from io_utils.display import (
    show_header_text, show_resource_bar_charts, show_geographic_map
)

st.set_page_config(layout="wide", page_title="Quantum Impact Dashboard")

# --- 1. Load Data ---
text_data = get_display_text()
chart_data = get_barchart_data()
map_layers = get_map_layers_data()
map_styles = get_map_styles()

content = text_data.get('content', {})
res_config = text_data.get('bar_chart_info', {})

# --- 2. Sidebar ---
st.sidebar.header("Configuration")
selected_layers = st.sidebar.multiselect("Map Layers:", list(map_layers.keys()), default=list(map_layers.keys()))

# Determine available scales from data
SCENARIOS = list(chart_data.keys()) if chart_data else []
sample_entries = chart_data.get(SCENARIOS[0], []) if SCENARIOS else []
SCALES = sorted(list(set(e.get('scale') for e in sample_entries if 'scale' in e)))
selected_scale = st.sidebar.selectbox("FTQC System Configuration:", SCALES, index=0)

# --- 3. Main Content ---
show_header_text(content)

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Energy and Resource Consumption")
    if 'scenarios_markdown' in content: st.markdown(content['scenarios_markdown'])

    show_resource_bar_charts(
        RESOURCES=list(res_config.get('labels', {}).keys()),
        SCENARIOS=SCENARIOS,
        chart_data=chart_data,
        selected_scale=selected_scale,
        labels=res_config.get('labels', {}),
        units=res_config.get('units', {})
    )

with right_col:
    st.subheader("Geographic Distribution")
    if 'map_markdown' in content: st.markdown(content['map_markdown'])

    show_geographic_map(selected_layers, map_layers, map_styles)

    st.subheader("Authors")
    if 'team_markdown' in content: st.markdown(content['team_markdown'])