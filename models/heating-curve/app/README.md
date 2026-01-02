# Heating Curve Streamlit Application

Interactive web application for simulating and analyzing heating curves (Heizkennlinie) in residential buildings.

## Quick Start

```bash
# Navigate to heating-curve directory
cd models/heating-curve

# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate    # Linux/Mac

# Install dependencies (if not already installed)
pip install streamlit plotly

# Run the application
streamlit run app/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`.

## Features

### Simulation Tab

Generate synthetic heating curve data with:
- **Building Presets**: Heat Pump, Good Insulation, Poor Insulation, Historic
- **Configurable Parameters**: Slope, room targets, temperature limits
- **Noise Models**: Clean (Model 1), Moderate (Model 2), Noisy (Model 3)
- **Interactive Plots**: Plotly scatter plots with day/night coloring
- **Data Export**: Download simulated data as CSV

### Analysis Tab

Extract heating curve parameters from data:
- **Data Sources**: Use simulated data or upload your own CSV
- **Algorithms**: OLS (baseline) and RANSAC (outlier robust)
- **Detected Features**: Temperature limits, day/night modes
- **Ground Truth Comparison**: See extraction errors vs known parameters

## Module Structure

```
app/
├── streamlit_app.py    # Main Streamlit application
├── simulation.py       # Heating curve simulation functions
├── analysis.py         # Parameter extraction algorithms
├── config.py           # Presets and default configurations
├── __init__.py         # Package initialization
└── README.md           # This file
```

## Heating Curve Formula

The heating curve (Heizkennlinie) defines the relationship between outdoor temperature and flow temperature:

```
T_vorlauf = T_base + K × (T_room - T_outdoor)
```

Where:
- **T_vorlauf**: Flow temperature (°C)
- **T_base**: Base temperature, typically 20°C
- **K**: Slope (Neigung), typically 0.3-1.6
- **T_room**: Target room temperature (°C)
- **T_outdoor**: Outdoor temperature (°C)

## Building Type Reference

| Building Type | Slope | Max Vorlauf | Typical |
|---------------|-------|-------------|---------|
| Heat Pump + Floor Heating | 0.3 | 55°C | Modern |
| Radiators + Good Insulation | 1.0 | 65°C | Renovated |
| Radiators + Poor Insulation | 1.4 | 75°C | Older buildings |
| Historic Building | 1.6 | 80°C | Altbau |

## Data Format for Upload

When uploading your own data, the CSV must contain:
- `t_outdoor`: Outdoor temperature (°C)
- `t_vorlauf`: Flow temperature (°C)
- `is_night` (optional): Boolean indicating night mode

Example:
```csv
datetime,t_outdoor,t_vorlauf,is_night
2024-01-01 00:00,2.5,45.3,True
2024-01-01 00:15,2.4,45.5,True
...
```

## Dependencies

- streamlit >= 1.30
- plotly >= 5.18
- pandas
- numpy
- scikit-learn
- requests

## Related Files

- [model.ipynb](../model.ipynb) - Sprint 1: Simulation development
- [analysis.ipynb](../analysis.ipynb) - Sprint 2: Algorithm development
- [Sprint3 Plan](../plan/HeatingCurve_ProjectPlan_Sprint3.md) - Project plan
