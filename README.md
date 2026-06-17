# 🪐 Kepler Exoplanet Explorer

An interactive data analysis dashboard built with real NASA Kepler mission data.

## What it does
- Cleans and analyzes 4,600+ exoplanet records from NASA
- Interactive 3D planet explorer (drag, zoom, rotate)
- Filters by planet type and orbital period
- Identifies 359 habitable zone candidates
- Animated landing page with orbital simulation

## Tech Stack
Python · Pandas · Plotly Dash · NumPy

## How to run it
```bash
pip install pandas plotly dash numpy
python src/clean.py
python src/dashboard.py
```
Then open http://127.0.0.1:8050

## Key Findings
- Sub-Neptunes are the most common planet type Kepler found
- 359 planets fall within habitable zone temperatures (200–320K)
- Most planets cluster at orbital periods under 100 days