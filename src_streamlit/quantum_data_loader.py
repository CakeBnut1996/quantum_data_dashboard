# File: src_streamlit/quantum_data_loader.py
import json, os
import yaml
from pathlib import Path

# --- Constants & Helpers ---
BASE_DIR = Path(__name__).resolve().parent
YAML_PATH = BASE_DIR / 'DashboardInput.yaml'


def _load_yaml(path):
    """Helper to read the single source of truth YAML file."""
    # Ensure it's a Path object (in case a string was passed)
    path = Path(path)

    # FIX: Use 'path', NOT 'YAML_PATH'
    if not path.exists():
        print(f"DEBUG: File not found: {path}")  # Helpful debug
        return {}

    try:
        # FIX: Use 'path' here too
        return yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    except Exception as e:
        print(f"DEBUG: Error loading {path}: {e}")
        return {}

def _load_geojson_file(filename):
    """
    Helper to parse a GeoJSON file.
    Supports ONLY:
    1) Absolute paths.
    2) Paths relative to the project root (Current Working Directory).
    """
    path = Path(filename)

    # 1. Check if it is an absolute path
    if path.is_absolute():
        if path.exists():
            try:
                return json.loads(path.read_text(encoding='utf-8'))
            except Exception:
                pass
        return None
    # 2. Check relative to Project Root (Current Working Directory)
    # This captures "data_map/quantumhub.geojson" inside your project folder
    project_path = Path.cwd() / filename
    if project_path.exists():
        try:
            return json.loads(project_path.read_text(encoding='utf-8'))
        except Exception:
            pass

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
    """Returns dictionary of { LayerName: [Points] } from gis_layers."""
    data = _load_yaml(YAML_PATH)
    layer_config = data.get("gis_layers", {})

    loaded_layers = {}
    for name, filename in layer_config.items():
        if name.lower() == 'style':
            continue
        geojson = _load_geojson_file(filename)
        if geojson:
            points = _extract_points(geojson)
            if points:
                loaded_layers[name] = points
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