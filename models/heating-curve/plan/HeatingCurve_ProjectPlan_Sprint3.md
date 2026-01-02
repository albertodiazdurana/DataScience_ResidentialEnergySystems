# Heating Curve - Project Plan Sprint 3

**Project:** Heating Curve Model for Residential Energy Systems
**Phase:** Sprint 3 - Streamlit Interactive Application
**Duration:** 1 week

**Prepared by:** Alberto Diaz Durana
**Previous Phase:** Sprint 2 - Algorithm Development (Complete)
**Reference:** DEC-001, BACKLOG_Improvements.md

---

## 1. Purpose

### Objective

Develop an interactive Streamlit application that allows users to:
1. **Simulate** heating curve data with configurable parameters
2. **Analyze** uploaded or simulated data using Sprint 2 algorithms
3. **Visualize** results interactively
4. **Export** datasets and extracted parameters

### Deliverable

A fully functional Streamlit application (`app/streamlit_app.py`) with modular code structure ready for future enhancements.

### Long-Term Vision

This application is part of a larger initiative to create an **open-source collection of models and simulations for residential energy systems**. The goal is to provide:

- **Educational resources** for understanding heating system behavior
- **Reference implementations** of common algorithms and control strategies
- **Interactive tools** for energy engineers, building managers, and the general public
- **Reproducible research** with documented methodologies

### Target Audience

| Audience | Use Case |
|----------|----------|
| Energy engineers | Validate system configurations, explore optimization |
| Building managers | Understand heating behavior, identify issues |
| Students & researchers | Learn heating curve concepts, test algorithms |
| Data scientists | Reference implementations, algorithm comparison |
| General public | Educational exploration of heating systems |

### Value Proposition

- **Educational**: Interactive learning tool for heating system fundamentals
- **Practical**: Analyze real building data without specialized software
- **Open**: Transparent methodology, reproducible results
- **Extensible**: Modular design for adding new components (heat pumps, solar thermal, etc.)

---

## 2. Inputs and Dependencies

### Dependencies on Prior Sprints

| Sprint | Dependency | Status |
|--------|------------|--------|
| Sprint 1 | Simulation functions (`calculate_vorlauf`, `apply_noise`) | Ready |
| Sprint 1 | CONFIG dictionary structure | Ready |
| Sprint 2 | Pattern detection (clustering, limit detection) | Ready |
| Sprint 2 | Regression algorithms (OLS, RANSAC) | Ready |
| Sprint 2 | Parameter extraction functions | Ready |

### Technical Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| streamlit | ≥1.30 | Core framework |
| plotly | ≥5.18 | Interactive visualizations |
| pandas | 2.3.3 | Data manipulation |
| numpy | 2.4.0 | Numerical operations |
| scikit-learn | 1.8.0 | Regression algorithms |
| requests | - | Open-Meteo API |

---

## 3. Application Architecture

### File Structure

```
models/heating-curve/
├── app/
│   ├── streamlit_app.py      # Main application entry point
│   ├── config.py             # Default configurations and presets
│   ├── simulation.py         # Heating curve simulation functions
│   ├── analysis.py           # Parameter extraction algorithms
│   └── visualization.py      # Plotting functions (Plotly)
├── model.ipynb               # Sprint 1
├── analysis.ipynb            # Sprint 2
├── outputs/
│   ├── figures/
│   └── data/
└── plan/
```

### Application Pages/Tabs

| Tab | Purpose | Key Features |
|-----|---------|--------------|
| **Simulation** | Generate heating curve data | Parameter sliders, presets, scatter plot |
| **Analysis** | Extract parameters from data | Upload CSV or use simulated, algorithm comparison |
| **Documentation** | App usage and domain info | Sidebar or dedicated tab |

---

## 4. Functional Specification

### Tab 1: Simulation

#### Weather Data Selection

| Control | Type | Range | Default |
|---------|------|-------|---------|
| Location | Dropdown/Input | City or coordinates | Berlin |
| Start Date | Date picker | 1940-present | 2023-11-01 |
| End Date | Date picker | Start to present | 2024-03-31 |
| Winter Presets | Dropdown | Cold (2010-11), Mild (2023-24) | None |

#### Heating Curve Parameters

| Control | Type | Range | Default | Unit |
|---------|------|-------|---------|------|
| Building Preset | Dropdown | 4 options | Radiators + Poor | - |
| Slope (K) | Slider | 0.2 - 2.0 | 1.4 | - |
| Room Target (Day) | Slider | 18 - 24 | 20 | °C |
| Room Target (Night) | Slider | 14 - 20 | 16 | °C |
| T_vorlauf_max | Slider | 45 - 80 | 75 | °C |
| T_vorlauf_min | Slider | 20 - 35 | 25 | °C |
| Summer Cutoff | Slider | 12 - 20 | 15 | °C |
| Night Start | Slider | 20 - 24 | 22 | hour |
| Night End | Slider | 4 - 8 | 6 | hour |
| Noise Model | Radio | 1, 2, 3 | 1 | - |

#### Building Type Presets

| Preset | Slope | T_max | Description |
|--------|-------|-------|-------------|
| Heat Pump + Floor Heating | 0.3 | 55 | Modern, well-insulated |
| Radiators + Good Insulation | 1.0 | 65 | Renovated building |
| Radiators + Poor Insulation | 1.4 | 75 | Older building (default) |
| Historic Building | 1.6 | 80 | Unrenovated, high heat loss |

#### Outputs

- **Scatter Plot**: Interactive Plotly chart (outdoor vs Vorlauf)
  - Color-coded day/night
  - Hover info with exact values
  - Zoom/pan controls
- **Statistics Table**: Count, mean, std, min, max
- **Download Button**: Export simulated data as CSV

### Tab 2: Analysis

#### Data Input

| Option | Description |
|--------|-------------|
| Use Simulated | Analyze data from Simulation tab |
| Upload CSV | User provides own data file |

**Required CSV columns:**
- `t_outdoor`: Outdoor temperature (°C)
- `t_vorlauf`: Flow temperature (°C)
- `hour` (optional): For day/night detection

#### Analysis Options

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Algorithm | Multi-select | OLS, RANSAC | Both |
| Mode Detection | Checkbox | Auto-detect day/night | On |
| Show Ground Truth | Checkbox | If simulated data | On |

#### Outputs

- **Extracted Parameters Table**:
  - Slope K (extracted vs actual if available)
  - T_room_day, T_room_night
  - T_vorlauf_max, T_vorlauf_min (if detectable)
  - Error metrics

- **Fitted Curves Plot**:
  - Data points (day/night colored)
  - Regression lines overlay
  - Confidence regions (future)

- **Algorithm Comparison**:
  - OLS vs RANSAC side-by-side
  - Performance metrics (R², MAE)

### Tab 3: Documentation (Sidebar)

| Section | Content |
|---------|---------|
| About | App purpose, data sources |
| Heating Curve Theory | Heizkennlinie formula, parameters |
| Building Types | Slope recommendations by building |
| Algorithms | OLS vs RANSAC explanation |
| Data Format | CSV requirements for upload |

---

## 5. Execution Plan

### Part 1: Project Setup and Code Extraction

**Objective:** Set up app structure and extract functions from notebooks

**Activities:**
- Create `app/` directory structure
- Extract simulation functions from `model.ipynb` → `simulation.py`
- Extract analysis functions from `analysis.ipynb` → `analysis.py`
- Create `config.py` with presets and defaults
- Install Streamlit and Plotly

**Deliverables:**
- Working module structure
- Functions importable and testable
- `requirements.txt` for app dependencies

**Verification:**
```python
from app.simulation import calculate_vorlauf, apply_noise
from app.analysis import extract_parameters
from app.config import BUILDING_PRESETS
```

---

### Part 2: Simulation Tab

**Objective:** Implement data simulation with interactive controls

**Activities:**
- Create main Streamlit layout
- Implement parameter sliders with presets
- Add weather data fetching (cached)
- Generate scatter plot with Plotly
- Add statistics display
- Implement CSV download

**Deliverables:**
- Working Simulation tab
- Real-time plot updates
- Data export functionality

**Verification:**
- [ ] Sliders adjust parameters correctly
- [ ] Presets load correct values
- [ ] Scatter plot updates in real-time
- [ ] CSV download works

---

### Part 3: Analysis Tab

**Objective:** Implement parameter extraction interface

**Activities:**
- Add data source selection (simulated vs upload)
- Implement CSV upload with validation
- Add algorithm selection controls
- Display extracted parameters
- Create comparison visualizations
- Show error metrics vs ground truth

**Deliverables:**
- Working Analysis tab
- Upload functionality
- Algorithm comparison output

**Verification:**
- [ ] CSV upload validates format
- [ ] Algorithms run without errors
- [ ] Results match notebook outputs
- [ ] Ground truth comparison works

---

### Part 4: Visualization Enhancement

**Objective:** Create polished, interactive visualizations

**Activities:**
- Convert matplotlib plots to Plotly
- Add hover information
- Implement color coding (day/night, clusters)
- Add fitted curve overlays
- Create algorithm comparison charts

**Deliverables:**
- Interactive scatter plots
- Regression visualization
- Comparison bar charts

**Verification:**
- [ ] Plots are interactive (zoom, pan, hover)
- [ ] Day/night coloring works
- [ ] Fitted curves display correctly

---

### Part 5: Documentation and Polish

**Objective:** Add documentation and final polish

**Activities:**
- Write sidebar documentation
- Add tooltips and help text
- Implement error handling
- Test edge cases
- Create app README

**Deliverables:**
- Complete sidebar documentation
- User-friendly error messages
- App README with usage instructions

**Verification:**
- [ ] Documentation covers all features
- [ ] Error messages are helpful
- [ ] App handles invalid inputs gracefully

---

### Part 6: Testing and Handoff

**Objective:** Verify app works correctly and document

**Activities:**
- End-to-end testing
- Performance check (load times)
- Create Sprint 3 handoff document
- Update BACKLOG with findings

**Deliverables:**
- Tested, working application
- Sprint 3 handoff document
- Updated backlog

**Verification:**
- [ ] App runs with `streamlit run app/streamlit_app.py`
- [ ] All tabs functional
- [ ] No critical bugs
- [ ] Documentation complete

---

## 6. Technical Specifications

### Simulation Module (`simulation.py`)

```python
# Functions to extract from model.ipynb

def fetch_weather_data(
    latitude: float = 52.52,
    longitude: float = 13.41,
    start_date: str = "2023-11-01",
    end_date: str = "2024-03-31"
) -> pd.DataFrame:
    """Fetch weather data from Open-Meteo API."""

def interpolate_to_15min(df: pd.DataFrame) -> pd.DataFrame:
    """Convert hourly to 15-minute resolution."""

def calculate_vorlauf(
    t_outdoor: float,
    t_room: float,
    slope: float,
    t_base: float,
    t_min: float,
    t_max: float,
    summer_cutoff: float
) -> float:
    """Calculate Vorlauf temperature using Heizkennlinie."""

def apply_noise(
    df: pd.DataFrame,
    model_config: dict,
    random_seed: int = 42
) -> pd.DataFrame:
    """Apply noise model to ideal Vorlauf."""

def generate_simulation(config: dict) -> pd.DataFrame:
    """Main function: generate complete simulation dataset."""
```

### Analysis Module (`analysis.py`)

```python
# Functions to extract from analysis.ipynb

def detect_temperature_limits(
    df: pd.DataFrame,
    vorlauf_col: str = 't_vorlauf'
) -> tuple[float, float]:
    """Detect upper and lower temperature limits from data."""

def detect_day_night_modes(
    df: pd.DataFrame,
    vorlauf_col: str = 't_vorlauf'
) -> np.ndarray:
    """Detect day/night modes using clustering."""

def fit_ols(
    X: np.ndarray,
    y: np.ndarray
) -> dict:
    """Fit OLS regression and return parameters."""

def fit_ransac(
    X: np.ndarray,
    y: np.ndarray
) -> dict:
    """Fit RANSAC regression and return parameters."""

def extract_parameters(
    df: pd.DataFrame,
    vorlauf_col: str = 't_vorlauf',
    algorithms: list = ['OLS', 'RANSAC']
) -> dict:
    """Main function: extract heating curve parameters."""
```

### Configuration Module (`config.py`)

```python
# Building type presets
BUILDING_PRESETS = {
    "Heat Pump + Floor Heating": {
        "slope": 0.3,
        "t_vorlauf_max": 55,
        "description": "Modern, well-insulated"
    },
    "Radiators + Good Insulation": {
        "slope": 1.0,
        "t_vorlauf_max": 65,
        "description": "Renovated building"
    },
    "Radiators + Poor Insulation": {
        "slope": 1.4,
        "t_vorlauf_max": 75,
        "description": "Older building (default)"
    },
    "Historic Building": {
        "slope": 1.6,
        "t_vorlauf_max": 80,
        "description": "Unrenovated, high heat loss"
    }
}

# Noise model configurations
NOISE_MODELS = {
    "Model 1": {...},
    "Model 2": {...},
    "Model 3": {...}
}

# Default parameters
DEFAULT_CONFIG = {...}
```

---

## 7. Acceptance Criteria

### Must Have (MVP)

- [ ] App runs with `streamlit run app/streamlit_app.py`
- [ ] Simulation tab generates data with adjustable parameters
- [ ] Building presets work correctly
- [ ] Interactive scatter plot displays
- [ ] CSV export functional
- [ ] Analysis tab extracts parameters
- [ ] OLS and RANSAC algorithms work
- [ ] Results display in clear format

### Should Have

- [ ] CSV upload for user data
- [ ] Algorithm comparison visualization
- [ ] Day/night mode detection
- [ ] Ground truth comparison
- [ ] Sidebar documentation
- [ ] Weather data caching

### Nice to Have

- [ ] Multiple location support
- [ ] Winter presets (2010-11, etc.)
- [ ] Confidence intervals display
- [ ] Data quality scoring
- [ ] Export extracted parameters

---

## 8. Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Streamlit performance issues | Medium | Medium | Cache expensive operations |
| Open-Meteo API rate limits | Low | Medium | Cache weather data, add retry logic |
| Complex state management | Medium | Medium | Use st.session_state properly |
| Plotly rendering issues | Low | Low | Fall back to matplotlib if needed |
| Code extraction errors | Low | High | Test modules independently |

---

## 9. Items Deferred to Future Sprints

From BACKLOG_Improvements.md:

| Item | Priority | Reason for Deferral |
|------|----------|---------------------|
| Quantile regression | P2 | Not critical for MVP |
| Piecewise regression | P2 | Complexity, limited S-shape data |
| Confidence intervals | P3 | Enhancement, not core |
| Cold winter data | P3 | Data available, feature not critical |
| Data quality scoring | P3 | Enhancement |

---

## 10. Success Metrics

| Metric | Target |
|--------|--------|
| App loads successfully | 100% |
| Simulation generates correct data | Validated against notebook |
| Analysis extracts parameters | Within 5% of notebook results |
| User can complete simulation → analysis flow | < 30 seconds |
| All interactive features responsive | < 1 second response |

---

## 11. Future Roadmap (Beyond Sprint 3)

This heating curve module is the first component of a broader **Residential Energy Systems** collection:

### Planned Modules

| Module | Description | Priority |
|--------|-------------|----------|
| **Heating Curve** | Heizkennlinie simulation and analysis | Current |
| **Heat Pump** | COP modeling, performance curves | High |
| **District Heating** | Fernwärme optimization, return temp | High |
| **Solar Thermal** | Collector efficiency, storage | Medium |
| **Building Thermal Mass** | Thermal inertia, response times | Medium |
| **Hybrid Systems** | Combined heat sources optimization | Low |
| **Sector Coupling** | PV + Heat Pump + Storage | Low |

### Platform Evolution

| Phase | Focus |
|-------|-------|
| Phase 1 | Individual module apps (Streamlit) |
| Phase 2 | Unified dashboard with module selection |
| Phase 3 | API for programmatic access |
| Phase 4 | Community contributions and extensions |

---

## 12. Handoff Checklist

At sprint completion:

- [ ] App runs without errors
- [ ] All MVP criteria met
- [ ] Code is modular and documented
- [ ] Sprint 3 handoff document created
- [ ] BACKLOG updated with findings
- [ ] README for app created
- [ ] Code commented for educational purposes

---

**End of Sprint 3 Project Plan**

**Document Version:** 1.0
**Created:** 2024-12
**Status:** Ready for execution
