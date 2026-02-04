# File: src_streamlit/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
from src_streamlit.quantum_data_loader import (
    get_display_text,
    get_barchart_data,
    get_map_layers_data,
    get_map_styles
)
from data_utils.GIS_format_converter import get_image_base64
st.set_page_config(layout="wide", page_title="Quantum Resource Dashboard")

# --- 1. Load Data ---
text_data = get_display_text()
chart_data = get_barchart_data()
map_layers = get_map_layers_data()
map_styles = get_map_styles()

# Unpack Config
content = text_data.get('content', {})
res_config = text_data.get('bar_chart_info', {})
resource_labels = res_config.get('labels', {})
resource_units = res_config.get('units', {})

# Constants
SCENARIOS = list(chart_data.keys()) if chart_data else ['baseline']
# Helper to get scales
sample_entries = chart_data.get(SCENARIOS[0], []) if SCENARIOS else []
SCALES = list(set(e.get('scale') for e in sample_entries if 'scale' in e))
SCALES.sort()  # Ensure consistent order
RESOURCES = list(resource_labels.keys())

# --- 2. Sidebar Controls ---
st.sidebar.header("Configuration")

# Map Layer Selection
available_layer_names = list(map_layers.keys())
selected_layer_names = st.sidebar.multiselect(
    "Map Layers:",
    available_layer_names,
    default=available_layer_names
)

selected_scale = st.sidebar.selectbox("FTQC System Configuration:", SCALES, index=0)

# --- 3. Main Content ---
st.title(content.get('title', "Quantum Resource Dashboard"))
if 'intro_markdown' in content:
    st.markdown(content['intro_markdown'])

# --- 4. Layout ---
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Resource Bar Charts")

    if not chart_data:
        st.warning("No chart data found.")
    else:
        for resource in RESOURCES:
            label = resource_labels.get(resource, resource)
            unit = resource_units.get(resource, "")

            rows = []
            for scenario in SCENARIOS:
                entries = chart_data.get(scenario, [])
                vals = [e.get(resource, 0) for e in entries if e.get("scale") == selected_scale]
                errs = [e.get(f"{resource}Err", 0) for e in entries if e.get("scale") == selected_scale]

                total = sum(vals) if vals else 0.0
                total_err = np.sqrt(sum((e or 0.0) ** 2 for e in errs)) if errs else 0.0
                rows.append({"scenario": scenario, "value": total, "error": total_err})

            df_chart = pd.DataFrame(rows)
            if not df_chart.empty:
                fig = px.bar(
                    df_chart, x='scenario', y='value', error_y='error',
                    labels={'scenario': 'Scenario', 'value': f"{label} ({unit})"},
                    color_discrete_sequence=[px.colors.qualitative.Pastel[0]]
                )
                fig.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
                fig.update_yaxes(type="log", autorange=True)
                st.markdown(f"**{label}**")
                st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Geographic Distribution")

    # Initialize Mapbox Figure
    fig_map = go.Figure()

    # Get style defaults
    defaults = map_styles.get('defaults', {'color': 'red', 'size': 8, 'opacity': 0.7})
    layer_style_config = map_styles.get('layers', {})

    has_data = False

    for name in selected_layer_names:
        points = map_layers.get(name, [])
        if not points:
            continue

        has_data = True
        df_layer = pd.DataFrame(points)

        # Determine Style
        style = layer_style_config.get(name, {})
        color = style.get('color', defaults.get('color'))
        size = style.get('size', defaults.get('size'))
        opacity = style.get('opacity', defaults.get('opacity'))

        # Add Trace
        fig_map.add_trace(go.Scattermapbox(
            lat=df_layer['lat'],
            lon=df_layer['lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=size,
                color=color,
                opacity=opacity,
            ),
            text=df_layer.get('name', name),
            name=name
        ))

    if has_data:
        fig_map.update_layout(
            mapbox={
                "style": "open-street-map",
                "bounds": {
                    "west": -135, "east": -60,
                    "south": 20, "north": 55
                },
                "zoom": 1,
                "center": {"lat": 38.0, "lon": -95.0},
            },
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=300,
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )

        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No layer data selected or available.")

    st.subheader("Description")
    if 'map_markdown' in content:
        st.markdown(content['map_markdown'])