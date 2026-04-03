# The potential energy and physical resource impacts of quantum systems at scale

## Overview
This repository provides a Streamlit dashboard that visualizes quantum impact, published as https://quantum-impact-dashbboard.streamlit.app/ 

This dashboard summarizes the supplemental analysis behind the study by showing three illustrative fault-tolerant quantum computing (FTQC) configurations based on superconducting transmon circuits: `Practical FTQC`, `Full FTQC (Small)`, and `Full FTQC (Large)`. The intent is a first-of-its-kind proof-of-concept that is simple, standardized, and easy to communicate, while acknowledging that many alternative system designs are possible.

Using these assumptions, the dashboard compares low- and high-penetration deployment scenarios and reports national-scale implications for electric power, water, liquid nitrogen, and helium demand. The supplemental spreadsheets are intended to let readers reproduce and extend the analysis with their own customized assumptions.

## Features
- Interactive barchart display 
- Map display and filtering
- Configuration via `DashboardInput.yaml`

### Map display and filtering
Map datasets are stored in MotherDuck and loaded as two GIS layers:

- **US Quantum R&D Centers:** Locations of federal quantum research centers in the United States from Center for Strategic & International Studies (CSIS): https://www.csis.org/analysis/innovation-lightbulb-us-federal-investments-quantum-technology-research-and-infrastructure
- **US Commercial Data Centers:** Locations of US commercial data centers up until mid-2025 from S&P Global Research Datacenter KnowledgeBase.

### Data access and usage
- To use map display features in your own deployment, you need to host and connect your own map data source (for example, in MotherDuck).
- Bar chart data is already provided in `DashboardInput.yaml` and can be used directly without additional data hosting.
- If you do not plan to extend this repository, use the published dashboard directly: https://quantum-impact-dashbboard.streamlit.app/

## Prerequisites
- Python 3.9+ (or compatible)
- Recommended: create a virtual environment using `uv sync`

## Running the dashboard
From the repository root:
   streamlit run app.py

The app will start at http://localhost:8501 by default. If your app uses a React component, make sure any build step for that component is run (e.g., npm run build in the component folder) before starting Streamlit.

## Citation
If you use this dashboard, please cite the following publications:

McCollum, D.L., Bhanja, S., Chehade, S. et al. Energy and physical resource impacts of quantum computing merit greater attention. Nat. Rev. Clean Technol. (2026). https://doi.org/10.1038/s44359-026-00156-3

McCollum DL, Sharma N, Pan M, Yao W, Bhanja S, Chehade S, et al. Uncertain quantum computing futures and potential energy and physical resource impacts at scale. Renewable and Sustainable Energy Transition 2026;9:100140. https://doi.org/10.1016/j.rset.2026.100140.


