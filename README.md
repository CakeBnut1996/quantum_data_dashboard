# Quantum Center Streamlit Dashboard

## Overview
This repository provides a Streamlit dashboard that visualizes Quantum Center locations and associated metadata. The raw data was obtained from a public resource and integrated for offline use. The dashboard uses ingestion and preprocessing code in `data_utils/` and a React map component at `MapView.jsx` for the frontend map view.

## Features
- Interactive barchart display 
- Map display and filtering
- Raw dataset generation from a public website
- Simple configuration via `DashboardInputExample.yaml`

## Prerequisites
- Python 3.9+ (or compatible)
- Recommended: create a virtual environment using `uv sync`


## Project layout
- data_map/                      # Raw and processed data files (committed for offline use)
- data_utils/
  - get_quan_data.py             # Script to fetch/update raw quantum center data from web
  - data_from_web_converter.py   # Converter/normalizer for web data -> repo format
- src_streamlit/
  - quantum_data_loader.py       # Loader and preprocessing functions used by the app
- app.py                         # Streamlit entrypoint
- DashboardInputExample.yaml     # Example configuration for running the dashboard

## Data update workflow
1. Run `data_utils/get_quan_data.py` to fetch the latest data from the public source
2. Convert it to geojson format for the map display with `data_utils/data_from_web_converter.py`
3. Update `DashboardInputExample.yaml` if your input file path or filters change.

## Running the dashboard
From the repository root:
   streamlit run app.py

The app will start at http://localhost:8501 by default. If your app uses a React component, make sure any build step for that component is run (e.g., npm run build in the component folder) before starting Streamlit.

## Configuration
- `DashboardInputExample.yaml` — describes input file location and optional display filters. Edit this file to point the app at a different data file or change default filters.

## Development notes
- Keep data ingestion scripts idempotent: avoid overwriting corrected data without review.
- The core data-loading function is in `src_streamlit/quantum_data_loader.py`.
- The data fetching function is `data_utils/get_quan_data.py`.

