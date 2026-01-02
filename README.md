# Data Science for Residential Energy Systems

An open-source collection of models, simulations, and interactive tools for understanding and optimizing residential energy systems.

## Live Applications

| Module | Description | Demo |
|--------|-------------|------|
| **Heating Curve** | Simulate and analyze heating curves (Heizkennlinie) | [Try it](https://datascience-residentialenergysystems-heating-curve.streamlit.app) |

## Project Goals

This project provides:

- **Educational resources** for understanding heating system behavior
- **Reference implementations** of common algorithms and control strategies
- **Interactive tools** for energy engineers, building managers, and researchers
- **Reproducible research** with documented methodologies

## Modules

### Heating Curve (Heizkennlinie)

Located in `models/heating-curve/`

The heating curve module simulates and analyzes the relationship between outdoor temperature and flow temperature (Vorlauftemperatur) in residential heating systems.

**Features:**
- Simulate heating curve data with real weather from German cities
- Building type presets (Heat Pump, Radiators, Historic buildings)
- Noise models for testing algorithm robustness
- Parameter extraction using OLS and RANSAC regression
- All values referenced to German standards (DIN, VDI, GEG)

**Technical basis:**
```
T_vorlauf = T_base + K × (T_room - T_outdoor)
```

| Building Type | Slope (K) | Max Vorlauf | Reference |
|---------------|-----------|-------------|-----------|
| Heat Pump + Floor Heating | 0.3 | 55°C | DIN EN 1264 |
| Radiators + Good Insulation | 1.0 | 65°C | EnEV/GEG |
| Radiators + Poor Insulation | 1.4 | 75°C | Factory default |
| Historic Building | 1.6 | 80°C | DIN 4701 |

[View Heating Curve Documentation](models/heating-curve/app/README.md)

## Planned Modules

| Module | Description | Priority |
|--------|-------------|----------|
| Heat Pump | COP modeling, performance curves | High |
| District Heating | Fernwärme optimization, return temperature | High |
| Solar Thermal | Collector efficiency, storage | Medium |
| Building Thermal Mass | Thermal inertia, response times | Medium |
| Hybrid Systems | Combined heat sources optimization | Low |
| Sector Coupling | PV + Heat Pump + Storage | Low |

## Standards & References

Parameter values throughout this project are based on German norms:

| Standard | Description |
|----------|-------------|
| DIN EN 12831 | Heat load calculation, indoor design temperature (20°C) |
| DIN EN 1264 | Floor heating systems (max 35°C Vorlauf) |
| DIN 4703 | Radiator design temperatures |
| VDI 2067 | Night setback recommendations (4K) |
| VDI 6030 | Heating curve slopes per building type |
| GEG | Gebäudeenergiegesetz (Building Energy Act) |

## Project Structure

```
DataScience_ResidentialEnergySystems/
├── models/
│   └── heating-curve/           # Heating curve module
│       ├── app/                 # Streamlit application
│       │   ├── streamlit_app.py # Main application
│       │   ├── simulation.py    # Simulation functions
│       │   ├── analysis.py      # Analysis algorithms
│       │   └── config.py        # Configuration & presets
│       ├── model.ipynb          # Sprint 1: Simulation notebook
│       ├── analysis.ipynb       # Sprint 2: Analysis notebook
│       └── plan/                # Project planning documents
├── project-knowledge/           # Domain knowledge & references
└── README.md                    # This file
```

## Getting Started

### Run Locally

```bash
# Clone the repository
git clone https://github.com/albertodiazdurana/DataScience_ResidentialEnergySystems.git
cd DataScience_ResidentialEnergySystems

# Navigate to a module
cd models/heating-curve

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# or
source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r app/requirements.txt

# Run the Streamlit app
streamlit run app/streamlit_app.py
```

### Use the Live Demo

Visit the [Heating Curve App](https://datascience-residentialenergysystems-heating-curve.streamlit.app) directly in your browser.

## Technology Stack

- **Python 3.11+**
- **Streamlit** - Interactive web applications
- **Plotly** - Interactive visualizations
- **Pandas / NumPy** - Data manipulation
- **Scikit-learn** - Machine learning algorithms
- **Open-Meteo API** - Historical weather data

## Contributing

Contributions are welcome! Areas of interest:

- Additional building types and regional presets
- New analysis algorithms
- Integration with real sensor data
- Additional energy system modules

## Author

**Alberto Diaz Durana**

[GitHub](https://github.com/albertodiazdurana) | [LinkedIn](https://www.linkedin.com/in/albertodiazdurana/)

## License

This project is open source and available for educational and research purposes.
