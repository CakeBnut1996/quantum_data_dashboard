# File: src_streamlit/quantum_data_loader.py
import json, os
import yaml
from pathlib import Path
import duckdb
from dotenv import load_dotenv
import streamlit as st

# --- Constants & Helpers ---
BASE_DIR = Path(__name__).resolve().parent
YAML_PATH = BASE_DIR / 'DashboardInput.yaml'
load_dotenv()


def get_motherduck_token():
    """Retrieves token from Streamlit Secrets or Environment Variables."""
    # 1. Try Streamlit Secrets (Cloud)
    if "MOTHERDUCK_TOKEN" in st.secrets:
        return st.secrets["MOTHERDUCK_TOKEN"]

    # 2. Fallback to Environment Variables (Local)
    return os.getenv("MOTHERDUCK_TOKEN")


def _load_yaml(path):
    """Reads YAML with relative-to-file path resolution."""
    # Resolve relative to this script's directory if not absolute
    p = Path(path)
    if not p.is_absolute():
        p = Path(__file__).parent.parent / p  # Adjust '.parent' count based on folder depth

    if not p.exists():
        print(f"DEBUG: File not found: {p}")
        return {}

    try:
        return yaml.safe_load(p.read_text(encoding='utf-8')) or {}
    except Exception as e:
        print(f"DEBUG: Error loading {p}: {e}")
        return {}

def _fetch_from_motherduck(table_name):
    token = get_motherduck_token()
    if not token:
        print(f"Error: MOTHERDUCK_TOKEN not found for {table_name}")
        return None

    try:
        # Pass the token explicitly in the connection string for maximum flexibility
        con = duckdb.connect(f"md:?motherduck_token={token}")
        con.execute("INSTALL spatial; LOAD spatial;")

        query = f"SELECT *, ST_AsGeoJSON(ST_Point(Longitude, Latitude)) as geometry FROM {table_name}"
        df = con.execute(query).df()

        features = [
            {
                "type": "Feature",
                "geometry": json.loads(row["geometry"]),
                "properties": row.drop("geometry").to_dict()
            }
            for _, row in df.iterrows()
        ]
        return {"type": "FeatureCollection", "features": features}
    except Exception as e:
        st.error(f"MotherDuck Error ({table_name}): {e}")
        return None


def _load_geojson_file(resource_identifier):
    """Unified loader: Detects MotherDuck URI or Local Path."""
    if resource_identifier.startswith("motherduck://"):
        return _fetch_from_motherduck(resource_identifier.replace("motherduck://", ""))

    p = Path(resource_identifier)
    # Ensure local files are found relative to the project root
    if not p.is_absolute():
        p = Path(__file__).parent.parent / p

    if p.exists():
        return json.loads(p.read_text(encoding='utf-8'))

    st.warning(f"Resource not found: {resource_identifier}")
    return None


def _extract_points(gj):
    """Convert GeoJSON to flat list of points for Streamlit map."""
    if not gj:
        return []
    features = gj.get('features', []) or []
    results = []
    for f in features:
        geom = f.get('geometry', {}) or {}
        props = f.get('properties', {}) or {}
        coords = geom.get('coordinates') or []
        # GeoJSON is [lon, lat]
        lon, lat = (coords[0], coords[1]) if len(coords) >= 2 else (None, None)
        if lat is not None and lon is not None:
            entry = {'lat': lat, 'lon': lon}
            entry.update(props)
            results.append(entry)
    return results


# --- 1. Display Text Functions ---
def get_display_text():
    """
    Returns the dashboard textual content (titles, markdown descriptions)
    and resource configuration (labels, units).
    """
    data = _load_yaml(YAML_PATH)
    return {
        "content": data.get("dashboard_content", {}),
        "bar_chart_info": data.get("bar_chart_info", {})
    }


# --- 2. Display Barcharts Data ---
def get_barchart_data():
    """
    Returns the raw data needed for the resource bar charts.
    """
    data = _load_yaml(YAML_PATH)
    return data.get("bar_chart_data", {})


# --- 3. Display Maps Data ---
def get_map_layers_data():
    """Returns { LayerName: [Points] } by iterating through YAML config."""
    layer_config = _load_yaml(YAML_PATH).get("gis_layers", {})
    loaded_layers = {}

    for name, uri in layer_config.items():
        if name.lower() == 'style': continue

        geojson = _load_geojson_file(uri)
        if geojson:
            points = _extract_points(geojson)
            if points:
                loaded_layers[name] = points
                print(f"Loaded {name}: {len(points)} points")

    return loaded_layers


# --- 4. (New) Map Styles ---
def get_map_styles():
    """Returns the styling configuration from map_style.yaml."""
    # 1. Load the MAIN config
    data = _load_yaml(YAML_PATH)
    layer_config = data.get("gis_layers", {})

    # 2. Get the filename of the style file (e.g., "map_style.yaml")
    style_filename = layer_config.get('style')

    if style_filename:
        # --- CRITICAL FIX ---
        # Combine the BASE_DIR (defined earlier) with the filename
        # This ensures Python looks in the correct project folder
        full_style_path = BASE_DIR / style_filename

        loaded_styles = _load_yaml(full_style_path)

        # Only return if we actually found data, otherwise keep going to fallback
        if loaded_styles:
            return loaded_styles

    # Fallback if no style file is defined OR if loading failed
    print("WARNING: Using default styles. Could not load style file.")
    return {
        'defaults': {'color': 'red', 'size': 10, 'opacity': 0.7},
        'layers': {}
    }