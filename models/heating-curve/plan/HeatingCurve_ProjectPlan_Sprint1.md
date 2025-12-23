# Heating Curve Simulation - Project Plan

**Project:** Heating Curve Model for Residential Energy Systems
**Phase:** Sprint 1 - Functional Model (Structure)
**Duration:** 1 week

**Prepared by:** Alberto Diaz Durana
**Next Phase:** Sprint 2 - Complete Model (Realism)

---

## 1. Purpose

### Objective

Develop a Jupyter notebook (`model.ipynb`) that simulates realistic heating system temperature data for a residential building in Berlin. The simulation generates Vorlauftemperatur (flow temperature) readings based on real outdoor temperature data, incorporating Heizkennlinie (heating curve) control logic and Nachtabsenkung (night setback).

### Deliverable

A functional simulation producing three datasets with varying noise levels, each visualized as scatter plots (outdoor temp vs. flow temp), demonstrating different data quality scenarios encountered in real heating systems.

### Business Value

- Demonstrates understanding of heating system control fundamentals
- Creates ground-truth data for algorithm development in Sprint 2
- Simulates real-world data quality challenges from sensor systems

---

## 2. Inputs and Dependencies

### Input Data

| Source | Description | Format |
|--------|-------------|--------|
| Open-Meteo API | Historical hourly outdoor temperatures, Berlin | JSON via HTTP |
| Period | November 2023 - March 2024 (5 months heating season) | Timestamps |
| Resolution | Hourly (to be interpolated to 15-min) | ~3,600 hourly records |

### Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| Python environment (uv + .venv) | Required | Managed with uv |
| Internet connection | Required | For Open-Meteo API fetch |
| Domain knowledge | Available | Part I Domain Fundamentals (study guide) |

### Key Domain Parameters (from study guide)

| Parameter | Typical Value | Source |
|-----------|---------------|--------|
| Vorlauf at 4C outdoor | 60-65C (often too high) | Industry analysis |
| Night setback adoption | ~30% of systems | Industry data |
| Heating curve slope | 1.0-1.5 | Chapter 3.1 |
| Night setback hours | 22:00-06:00 typical | Chapter 3.5 |
| Summer cutoff | 15-18C outdoor | Chapter 3.5 |

---

## 3. Technical Prerequisites

### Environment Requirements (uv)

- [ ] uv installed
- [ ] Virtual environment created with uv
- [ ] Required packages installed via uv
- [ ] Jupyter kernel registered
- [ ] VS Code configured

### Environment Setup (Day 1)

```bash
# Create virtual environment with uv
uv venv

# Activate environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install packages
uv pip install pandas numpy requests matplotlib scipy jupyter ipykernel

# Register Jupyter kernel
python -m ipykernel install --user --name=heating-curve --display-name="Heating Curve"
```

### Project Structure

```
models/heating-curve/
    model.ipynb          # Main simulation notebook
    plan/
        HeatingCurve_ProjectPlan_Sprint1.md
        s01_dXX_checkpoint.md
    data/
        processed/       # Exported datasets
    .venv/               # Virtual environment (uv managed)
```

### Verification Checklist

- [ ] uv venv created successfully
- [ ] All packages import successfully
- [ ] Open-Meteo API accessible (test fetch)
- [ ] Jupyter notebook runs without errors

---

## 4. Execution Timeline

### Overview

| Day | Focus Area | Key Deliverable |
|-----|------------|-----------------|
| Day 1 | Setup and Data Acquisition | Weather data fetched and validated |
| Day 2 | Heating Curve Implementation | Basic Heizkennlinie + night setback |
| Day 3 | Noise Models (1, 2, 3) | Three datasets with varying quality |
| Day 4 | Visualization and Validation | Scatter plots + domain validation |
| Day 5 | Documentation and Review | Final notebook + sprint review |

---

### Day 1 - Setup and Data Acquisition

**Goal:** Set up environment with uv, fetch real Berlin weather data, prepare 15-minute resolution dataset

#### Part 0: Environment Setup with uv

**Objective:** Create reproducible development environment
**Activities:**
- Create virtual environment using uv
- Install required packages (pandas, numpy, requests, matplotlib, scipy, jupyter)
- Register Jupyter kernel
- Create notebook structure with markdown headers
**Deliverables:**
- Working virtual environment (.venv)
- Jupyter kernel registered
- Notebook skeleton with sections

#### Part 1: Open-Meteo API Integration

**Objective:** Fetch historical hourly temperatures for Berlin
**Activities:**
- Construct API request for Berlin coordinates (52.52N, 13.41E)
- Fetch data for Nov 2023 - Mar 2024
- Parse JSON response into pandas DataFrame
- Handle API errors and rate limits
**Deliverables:**
- Raw hourly temperature data (~3,600 records)
- API fetch function (reusable)

#### Part 2: Data Interpolation

**Objective:** Convert hourly data to 15-minute resolution
**Activities:**
- Interpolate temperatures using linear or cubic method
- Validate interpolation quality (no artifacts)
- Add datetime features (hour, day_of_week, month)
**Deliverables:**
- 15-minute resolution dataset (~14,400 records)
- Datetime feature columns

#### Part 3: Data Validation

**Objective:** Verify data quality and domain plausibility
**Activities:**
- Check for missing values
- Validate temperature ranges (typical Berlin winter: -15C to +15C)
- Plot time series to visual inspect
- Calculate basic statistics (mean, std, min, max by month)
**Deliverables:**
- Validated outdoor temperature dataset
- Summary statistics output

#### End-of-Day 1 Checkpoint

**Critical Review Questions:**
1. Is outdoor temperature data complete for Nov 2023 - Mar 2024?
2. Are interpolated values smooth without artifacts?
3. Do temperature ranges match expected Berlin winter conditions?
4. Is the data saved for reuse (avoid repeated API calls)?

---

### Day 2 - Heating Curve Implementation

**Goal:** Implement Heizkennlinie formula with night setback logic

#### Part 0: Review Domain Formulas

**Objective:** Confirm heating curve mathematics
**Activities:**
- Review Chapter 3.1 (Heizkennlinie)
- Define parameters: slope (K), base temp, room target
- Document formula: T_Vorlauf = T_base + K * (T_room - T_outdoor)
**Deliverables:**
- Documented formula with parameter definitions

#### Part 1: Basic Heating Curve Function

**Objective:** Implement core Heizkennlinie calculation
**Activities:**
- Create function `calculate_vorlauf(t_outdoor, slope, t_base, t_room_target)`
- Implement linear heating curve
- Add summer cutoff logic (T_outdoor > 15C: heating off)
- Test with sample outdoor temperatures
**Deliverables:**
- Working heating curve function
- Test outputs showing correct behavior

#### Part 2: Night Setback Implementation

**Objective:** Add Nachtabsenkung logic
**Activities:**
- Define night hours (22:00-06:00)
- Implement reduced room target during night (e.g., 16C vs 20C)
- Calculate resulting Vorlauf reduction
- Handle transition periods (smooth or step change)
**Deliverables:**
- Night setback function integrated
- Visualization showing day/night difference

#### Part 3: Apply to Full Dataset

**Objective:** Generate ideal Vorlauf time series
**Activities:**
- Apply heating curve to all 14,400 records
- Store as "ideal" or "Model 0" reference
- Validate output ranges (typical: 30-70C)
**Deliverables:**
- Complete Vorlauf time series (ideal, no noise)
- Scatter plot: outdoor temp vs Vorlauf (should show clear curve + night band)

#### End-of-Day 2 Checkpoint

**Critical Review Questions:**
1. Does the heating curve produce plausible Vorlauf temperatures?
2. Is night setback visible as a separate band in the scatter plot?
3. Does summer cutoff work correctly (no heating above 15C)?
4. Are function parameters easily adjustable for Sprint 2?

---

### Day 3 - Noise Models (1, 2, 3)

**Goal:** Create three datasets with progressively degraded data quality

#### Part 0: Define Noise Strategy

**Objective:** Plan noise characteristics for each model
**Activities:**
- Model 1: Low Gaussian noise (sigma=1-2C)
- Model 2: Moderate noise + occasional spikes (DHW simulation)
- Model 3: High noise + missing values + outliers
- Document noise parameters
**Deliverables:**
- Noise specification table

#### Part 1: Model 1 - Clean Data

**Objective:** Generate low-noise dataset where heating curve is clearly visible
**Activities:**
- Add Gaussian noise (sigma=1.5C)
- Apply to ideal Vorlauf
- Validate: scatter plot should clearly show Heizkennlinie
**Deliverables:**
- Model 1 dataset
- Scatter plot showing clear heating curve pattern

#### Part 2: Model 2 - Moderate Noise

**Objective:** Generate dataset with visible clusters but more scatter
**Activities:**
- Increase Gaussian noise (sigma=3-4C)
- Add occasional spikes (+10-15C) simulating DHW interference
- Apply temporal correlation (sensor lag)
- Validate: clusters for day/night/transition visible
**Deliverables:**
- Model 2 dataset
- Scatter plot showing clustered but noisier data

#### Part 3: Model 3 - Noisy/Realistic

**Objective:** Generate dataset resembling real sensor data with quality issues
**Activities:**
- High Gaussian noise (sigma=5-6C)
- Add 5-10% missing values (random blocks)
- Add outliers (1-2% of data, +/- 20C)
- Add stuck sensor values (repeated readings)
- Validate: scatter plot shows significant scatter
**Deliverables:**
- Model 3 dataset
- Scatter plot showing noisy, realistic data

#### End-of-Day 3 Checkpoint

**Critical Review Questions:**
1. Are the three models visually distinct in scatter plots?
2. Does Model 1 clearly show the heating curve?
3. Does Model 2 show identifiable clusters (day/night)?
4. Does Model 3 represent realistic sensor challenges?

---

### Day 4 - Visualization and Validation

**Goal:** Create publication-quality scatter plots and validate domain correctness

#### Part 0: Visualization Setup

**Objective:** Configure matplotlib for consistent, professional plots
**Activities:**
- Set figure size, DPI, font sizes
- Define color scheme for three models
- Create subplot layout (1x3 or 2x2)
**Deliverables:**
- Plotting configuration

#### Part 1: Scatter Plot Generation

**Objective:** Create main deliverable visualizations
**Activities:**
- Plot outdoor temp (x) vs Vorlauf (y) for each model
- Add heating curve reference line
- Add night setback reference line
- Include legend, axis labels, titles
**Deliverables:**
- Three scatter plots (Model 1, 2, 3)
- Combined comparison figure

#### Part 2: Domain Validation

**Objective:** Verify outputs match real-world expectations
**Activities:**
- Compare Vorlauf ranges to industry benchmarks (60-65C at 4C outdoor)
- Verify Spreizung (spread) is realistic
- Check night setback reduction magnitude
- Validate summer cutoff behavior
**Deliverables:**
- Validation report (printed outputs in notebook)
- Confirmation of domain plausibility

#### Part 3: Statistical Summary

**Objective:** Generate summary statistics for each model
**Activities:**
- Calculate mean, std, min, max for Vorlauf by model
- Count missing values, outliers per model
- Compare noise characteristics
- Create summary table
**Deliverables:**
- Summary statistics table
- Model comparison metrics

#### Part 4: Time Series Visualization

**Objective:** Show Vorlauf behavior over time
**Activities:**
- Plot Vorlauf time series for sample week
- Overlay outdoor temperature
- Highlight day/night transitions
**Deliverables:**
- Time series plot

#### End-of-Day 4 Checkpoint

**Critical Review Questions:**
1. Are scatter plots publication-quality?
2. Do domain experts validate the patterns as realistic?
3. Are statistics documented for Sprint 2 reference?
4. Is the notebook narrative coherent?

---

### Day 5 - Documentation and Review

**Goal:** Finalize notebook, document decisions, prepare for Sprint 2

#### Part 0: Notebook Cleanup

**Objective:** Ensure notebook is clean and reproducible
**Activities:**
- Remove debug/scratch cells
- Ensure cells run in sequence
- Add cell numbers (# Cell N)
- Verify all outputs display correctly
**Deliverables:**
- Clean, sequential notebook

#### Part 1: Documentation

**Objective:** Add comprehensive markdown documentation
**Activities:**
- Introduction: project context, objectives
- Methodology: heating curve formula, noise models
- Results: key findings, observations
- Next steps: Sprint 2 preview
**Deliverables:**
- Fully documented notebook
- Clear narrative flow

#### Part 2: Data Export

**Objective:** Save datasets for Sprint 2 analysis
**Activities:**
- Export Model 1, 2, 3 as CSV or pickle
- Include metadata (parameters used)
- Document file locations
**Deliverables:**
- Exported datasets in data/processed/
- Data dictionary

#### Part 3: Sprint 1 Review

**Objective:** Complete sprint documentation
**Activities:**
- Write sprint summary
- Document lessons learned
- Identify Sprint 2 scope adjustments
**Deliverables:**
- Sprint 1 summary document
- Sprint 2 scope recommendations

#### End-of-Day 5 Checkpoint

**Critical Review Questions:**
1. Does notebook run end-to-end without errors?
2. Are all three scatter plots generated successfully?
3. Is documentation sufficient for handoff?
4. Are datasets exported for Sprint 2?

---

## 5. Deliverables Summary

### Sprint 1 Deliverables

| Deliverable | Description | Location |
|-------------|-------------|----------|
| model.ipynb | Main simulation notebook | models/heating-curve/ |
| Outdoor temp data | Berlin Nov 2023 - Mar 2024, 15-min resolution | In notebook / data/ |
| Model 1 dataset | Low noise, clear heating curve | data/processed/ |
| Model 2 dataset | Moderate noise, visible clusters | data/processed/ |
| Model 3 dataset | High noise, realistic sensor issues | data/processed/ |
| Scatter plots | 3 visualizations comparing models | In notebook |
| Time series plot | Vorlauf behavior over time | In notebook |
| Summary statistics | Metrics for each model | In notebook |
| Sprint 1 summary | Lessons learned, Sprint 2 prep | plan/ |

### Functions Implemented

| Function | Purpose |
|----------|---------|
| `fetch_weather_data()` | Retrieve Berlin temperatures from Open-Meteo |
| `interpolate_to_15min()` | Convert hourly to 15-minute resolution |
| `calculate_vorlauf()` | Compute Vorlauf from outdoor temp using Heizkennlinie |
| `apply_night_setback()` | Reduce room target during night hours |
| `add_noise_model_1()` | Low Gaussian noise |
| `add_noise_model_2()` | Moderate noise + DHW spikes |
| `add_noise_model_3()` | High noise + missing values + outliers |

---

## 6. Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Open-Meteo API unavailable | Low | High | Backup: DWD OpenData or cached data |
| Heating curve formula incorrect | Medium | Medium | Validate against Chapter 3.1, compare to industry benchmarks |
| Noise models too similar | Medium | Low | Increase parameter differentiation, visual comparison |
| uv environment issues | Low | Medium | Fallback to standard pip/venv if needed |

---

## 7. Expected Outcomes

| Metric | Before Sprint 1 | After Sprint 1 |
|--------|-----------------|----------------|
| Notebooks | 0 functional | 1 complete (model.ipynb) |
| Datasets | 0 | 3 (Model 1, 2, 3) |
| Visualizations | 0 | 4 (3 scatter + 1 time series) |
| Domain functions | 0 | 7 (see functions list) |

### Key Benefits

- Ground-truth data for algorithm development (Sprint 2)
- Demonstrated understanding of Heizkennlinie control
- Realistic sensor data simulation for testing

---

## 8. Sprint 2 Outline (Complete Model)

### Objective

Enhance `model.ipynb` with realistic physical effects and begin `analysis.ipynb` for heating curve extraction algorithm.

### Duration

1 week

### Scope (Preliminary)

**model.ipynb Enhancements:**
- Building thermal inertia (lag tau = 2-6h)
- Hysteresis effects (1-2K dead band)
- DHW interference spikes (improved realism)
- Weekend/weekday patterns
- Boiler cycling (Taktverhalten)
- Sensor-specific issues (stuck values, timestamp drift)

**analysis.ipynb (New):**
- Data loading and exploration
- Heating curve extraction algorithm (regression-based)
- Parameter estimation (slope, base temp)
- Validation against known parameters

### Detailed Planning

Sprint 2 detailed plan will be created based on Sprint 1 results, incorporating:
- Lessons learned from Sprint 1
- Scope adjustments based on Sprint 1 deliverables
- Refined noise model parameters

---

## 9. Daily Checkpoint Template Reference

Use Template 6 from DSM_2.0_ProjectManagement_Guidelines for daily checkpoints.

**Filename Convention:** `s01_dXX_checkpoint.md`

**Location:** `models/heating-curve/plan/`

---

**End of Sprint 1 Project Plan**

**Document Version:** 1.0
**Created:** 2024-12
**Status:** Ready for execution
