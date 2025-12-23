# Decision: Sprint 3 Streamlit Interactive Application

**Decision ID:** DEC-001
**Date:** 2024-12
**Status:** Approved
**Context:** End of Sprint 1, Day 2

---

## Decision

Develop an interactive Streamlit application in Sprint 3 that allows users to explore heating curve scenarios by adjusting configurable parameters.

## Rationale

The CONFIG dictionary defined in `model.ipynb` contains parameters that significantly affect heating curve behavior. An interactive application enables:
1. Exploration of different building types (heat pump vs. old radiator systems)
2. Visualization of night setback effects
3. Comparison of noise model impacts
4. Educational demonstration of Heizkennlinie principles

---

## Application Features

### Input Parameters (Sliders/Inputs)

**Weather Data Selection:**

| Parameter | Range | Default | Unit |
|-----------|-------|---------|------|
| Location | City selector or coordinates | Berlin | - |
| Start date | 1940-01-01 to present | 2023-11-01 | date |
| End date | Start date to present | 2024-03-31 | date |

*Note: Open-Meteo Historical API provides data from 1940 onwards. Interesting winters to explore:*
- *2010-2011: Very cold Berlin winter*
- *2012-2013: Long, cold winter*
- *2023-2024: Mild winter (current default)*

**Heating Curve Parameters:**

| Parameter | Range | Default | Unit |
|-----------|-------|---------|------|
| Slope (K) | 0.2 - 2.0 | 1.4 | - |
| Room target day | 18 - 24 | 20 | °C |
| Room target night | 14 - 20 | 16 | °C |
| T_vorlauf_max | 45 - 80 | 75 | °C |
| T_vorlauf_min | 20 - 35 | 25 | °C |
| Summer cutoff | 12 - 20 | 15 | °C |
| Night start hour | 20 - 24 | 22 | hour |
| Night end hour | 4 - 8 | 6 | hour |
| Noise level | Model 1/2/3 | Model 1 | - |

### Outputs

- Real-time scatter plot (outdoor vs. Vorlauf)
- Heating curve visualization with day/night bands
- Summary statistics table
- Downloadable simulated dataset (CSV)

---

## Building Type Presets

| Preset | Slope | Description |
|--------|-------|-------------|
| Heat Pump + Floor Heating | 0.3 | Modern, well-insulated |
| Radiators + Good Insulation | 1.0 | Renovated building |
| Radiators + Poor Insulation | 1.4 | Older building (default) |
| Historic Building | 1.6 | Unrenovated, high heat loss |

**Source:** [Viessmann Heizkurve Guide](https://www.viessmann.de/de/wissen/anleitungen-und-tipps/heizkurve-einstellen.html)

---

## Technical Stack

- **Framework:** Streamlit
- **Visualization:** Plotly (interactive) or Matplotlib
- **Data:** Reuse functions from model.ipynb
- **Deployment:** Local or Streamlit Cloud

---

## File Structure (Proposed)

```
models/heating-curve/
    app/
        streamlit_app.py      # Main application
        config.py             # Default configurations
        heating_curve.py      # Core functions (extracted from notebook)
    model.ipynb               # Sprint 1-2: Simulation
    analysis.ipynb            # Sprint 2: Algorithm development
    outputs/
        figures/
        data/
```

---

## Dependencies on Prior Sprints

| Sprint | Dependency |
|--------|------------|
| Sprint 1 | CONFIG dictionary, calculate_vorlauf(), night setback functions |
| Sprint 2 | Noise model functions, analysis algorithm (optional integration) |

---

## Acceptance Criteria

- [ ] Application runs locally with `streamlit run streamlit_app.py`
- [ ] All CONFIG parameters adjustable via UI
- [ ] Building type presets load correct values
- [ ] Scatter plot updates in real-time
- [ ] CSV export functional
- [ ] Documentation in app sidebar

---

**Approved by:** Alberto Diaz Durana
**Implementation:** Sprint 3
