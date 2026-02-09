# File: src_streamlit/io_utils/display.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_header_text(content):
    """Displays title and intro markdown."""
    st.title(content.get('title', "Quantum Impact Dashboard"))
    if 'intro_markdown' in content:
        st.markdown(content['intro_markdown'])


def show_resource_bar_charts(RESOURCES, SCENARIOS, chart_data, selected_scale, labels, units):
    """Generates the vertical stack of log-scale bar charts."""
    for resource in RESOURCES:
        label = labels.get(resource, resource)
        unit = units.get(resource, "")
        rows = []

        for scenario in SCENARIOS:
            entries = chart_data.get(scenario, [])
            # Filter by the FTQC scale selected in sidebar
            subset = [e for e in entries if e.get("scale") == selected_scale]
            val = sum(e.get(resource, 0) for e in subset)
            err = (sum(e.get(f"{resource}Err", 0) ** 2 for e in subset)) ** 0.5
            rows.append({"scenario": scenario, "value": val, "error": err})

        df = pd.DataFrame(rows)
        if not df.empty:
            st.markdown(f"**{label}**")
            fig = px.bar(
                df, x='scenario', y='value', error_y='error',
                labels={'scenario': 'Scenario', 'value': f"{label} ({unit})"},
                color_discrete_sequence=[px.colors.qualitative.Pastel[0]]
            )
            fig.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
            fig.update_yaxes(type="log", autorange=True)
            st.plotly_chart(fig, use_container_width=True)


def show_geographic_map(selected_layers, map_layers_data, style_config):
    """Renders the Mapbox visualization."""
    fig = go.Figure()
    defaults = style_config.get('defaults', {'color': 'red', 'size': 8, 'opacity': 0.7})
    layer_styles = style_config.get('layers', {})

    has_data = False
    for name in selected_layers:
        points = map_layers_data.get(name, [])
        if not points: continue

        has_data = True
        df = pd.DataFrame(points)
        style = layer_styles.get(name, {})

        fig.add_trace(go.Scattermapbox(
            lat=df['lat'], lon=df['lon'], mode='markers',
            marker=go.scattermapbox.Marker(
                size=style.get('size', defaults['size']),
                color=style.get('color', defaults['color']),
                opacity=style.get('opacity', defaults['opacity'])
            ),
            text=df.get('name', name), name=name
        ))

    if has_data:
        fig.update_layout(
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

        st.plotly_chart(fig)
    else:
        st.info("No layer data selected.")