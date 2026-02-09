# Quantum Impact Dashboard

## Overview
This repository provides a Streamlit dashboard that visualizes quantum impact.

## Features
- Interactive barchart display 
- Map display and filtering
- Configuration via `DashboardInput.yaml`

## Prerequisites
- Python 3.9+ (or compatible)
- Recommended: create a virtual environment using `uv sync`

## Running the dashboard
From the repository root:
   streamlit run app.py

The app will start at http://localhost:8501 by default. If your app uses a React component, make sure any build step for that component is run (e.g., npm run build in the component folder) before starting Streamlit.

## Citation