# Backlog: Heating Curve Analysis Improvements

**Project:** Heating Curve Model for Residential Energy Systems
**Created:** 2024-12
**Last Updated:** 2024-12
**Source:** Sprint 2 Analysis Findings

---

## Purpose

This document tracks identified improvements, enhancements, and technical debt discovered during Sprint 1 and Sprint 2. Items are prioritized and categorized for future sprint planning.

---

## Priority Legend

| Priority | Description |
|----------|-------------|
| P1 | Critical - Required for production use |
| P2 | High - Significant improvement to accuracy/robustness |
| P3 | Medium - Nice to have, improves user experience |
| P4 | Low - Future enhancement |

---

## 1. Algorithm Improvements

### 1.1 Quantile Regression
**Priority:** P2
**Sprint:** Future
**Source:** Sprint 2 - Model 3 struggles with OLS/RANSAC

**Description:**
Implement quantile regression (median-based, q=0.5) as an alternative robust regression method.

**Rationale:**
- May outperform RANSAC on highly noisy data (Model 3)
- Less sensitive to outliers than OLS
- Provides different robustness characteristics than RANSAC

**Implementation Notes:**
- Use `statsmodels.regression.quantile_regression.QuantReg`
- Test q=0.5 (median) and q=0.25/0.75 for bounds
- Compare with RANSAC on Model 2/3

**Acceptance Criteria:**
- [ ] Quantile regression implemented
- [ ] Performance compared with OLS/RANSAC
- [ ] Model 3 temperature error < 2.5°C

---

### 1.2 Piecewise Linear Regression
**Priority:** P2
**Sprint:** Future
**Source:** Sprint 2 - S-shape handling limited

**Description:**
Implement piecewise linear regression to explicitly model the S-shape heating curve with upper/lower plateaus.

**Rationale:**
- Current algorithms treat entire curve as linear
- Piecewise model captures T_vorlauf_max and T_vorlauf_min directly
- Better for buildings with significant clamping

**Implementation Notes:**
- Three segments: lower plateau, linear region, upper plateau
- Breakpoint detection via optimization or grid search
- Consider `pwlf` library or custom implementation

**Acceptance Criteria:**
- [ ] Piecewise model with 3 segments implemented
- [ ] Breakpoints detected automatically
- [ ] T_vorlauf_max extracted within 1°C

---

### 1.3 Ensemble Methods
**Priority:** P3
**Sprint:** Future
**Source:** Sprint 2 - No single algorithm optimal for all conditions

**Description:**
Combine predictions from multiple algorithms using weighted averaging or voting.

**Rationale:**
- Different algorithms have different strengths
- Ensemble may provide more stable predictions
- Can weight by estimated data quality

**Implementation Notes:**
- Simple average of OLS, RANSAC, Quantile
- Weighted average based on R² or residual analysis
- Consider stacking with meta-learner

**Acceptance Criteria:**
- [ ] Ensemble method implemented
- [ ] Outperforms best single algorithm on average
- [ ] Weights interpretable

---

### 1.4 T_base Extraction
**Priority:** P2
**Sprint:** Future
**Source:** Sprint 2 - T_base assumed as 20°C

**Description:**
Extract T_base from data instead of assuming 20°C.

**Rationale:**
- Current algorithm assumes T_base = 20°C
- Real systems may have different base temperatures
- 3-parameter regression could extract T_base

**Implementation Notes:**
- Reformulate: T_vorlauf = T_base + K * (T_room - T_outdoor)
- Non-linear regression with 3 parameters
- Or use domain knowledge: T_base typically = T_room_day

**Acceptance Criteria:**
- [ ] T_base extracted from data
- [ ] Error < 1°C compared to ground truth
- [ ] Works across different building types

---

## 2. Preprocessing Improvements

### 2.1 Missing Data Imputation
**Priority:** P1
**Sprint:** Future
**Source:** Sprint 2 - Model 3 has 5% missing data

**Description:**
Implement and compare multiple imputation strategies for missing sensor data.

**Rationale:**
- Model 3 performance degrades significantly with 5% missing
- Different imputation methods have different trade-offs
- Real building data will have gaps

**Implementation Methods:**
| Method | Description | Complexity |
|--------|-------------|------------|
| Drop NaN | Simple removal | Baseline |
| Forward fill | Use previous value | Simple |
| Linear interpolation | Interpolate gaps | Medium |
| Seasonal interpolation | Use same hour, previous day | Medium |
| Model-based | Predict from outdoor temp + hour | Complex |

**Implementation Notes:**
- Compare all methods on Model 3
- Measure impact on parameter extraction accuracy
- Consider hybrid approaches for long gaps

**Acceptance Criteria:**
- [ ] All 5 imputation methods implemented
- [ ] Comparison table showing impact on accuracy
- [ ] Best method reduces Model 3 error by >20%

---

### 2.2 Outlier Pre-filtering
**Priority:** P2
**Sprint:** Future
**Source:** Sprint 2 - Outliers affect OLS significantly

**Description:**
Implement outlier detection and filtering before regression.

**Rationale:**
- DHW spikes and sensor errors create outliers
- Pre-filtering may improve OLS performance
- Multiple detection methods available

**Implementation Methods:**
| Method | Description |
|--------|-------------|
| Z-score filtering | Remove points > 3σ from mean |
| IQR filtering | Remove points outside 1.5×IQR |
| Isolation Forest | ML-based anomaly detection |
| Local Outlier Factor | Density-based detection |

**Acceptance Criteria:**
- [ ] At least 2 outlier detection methods implemented
- [ ] OLS with pre-filtering approaches RANSAC performance
- [ ] False positive rate < 5%

---

### 2.3 Data Quality Scoring
**Priority:** P3
**Sprint:** Future
**Source:** Sprint 2 - No quality assessment

**Description:**
Compute data quality metrics to guide algorithm selection and warn users.

**Rationale:**
- Different data quality requires different algorithms
- Users should know when results are unreliable
- Quality score can weight regression samples

**Implementation Notes:**
- Noise level estimate from residual variance
- Missing data percentage
- Outlier rate estimate
- Overall quality score (0-100)

**Acceptance Criteria:**
- [ ] Quality scoring function implemented
- [ ] Score correlates with extraction accuracy
- [ ] Threshold recommendations for each algorithm

---

## 3. Uncertainty Quantification

### 3.1 Confidence Intervals
**Priority:** P3
**Sprint:** Future
**Source:** Sprint 2 - No uncertainty reported

**Description:**
Provide confidence intervals for extracted parameters.

**Rationale:**
- Point estimates don't convey uncertainty
- Confidence intervals help with decision-making
- Important for customer communication

**Implementation Notes:**
- Bootstrap resampling (N=1000)
- Calculate 95% CI for K, T_room_day, T_room_night
- Consider Bayesian approach for full posterior

**Acceptance Criteria:**
- [ ] Bootstrap CI implemented
- [ ] CI covers true value 95% of time
- [ ] Visualization of parameter uncertainty

---

### 3.2 Prediction Intervals
**Priority:** P4
**Sprint:** Future
**Source:** Sprint 2 - Fitted curves have no bounds

**Description:**
Show prediction intervals around fitted heating curves.

**Rationale:**
- Helps visualize model uncertainty
- Useful for anomaly detection
- Professional presentation for customers

**Acceptance Criteria:**
- [ ] Prediction intervals plotted on heating curves
- [ ] Intervals widen appropriately in sparse data regions

---

## 4. Simulation Improvements

### 4.1 Cold Winter Data
**Priority:** P3
**Sprint:** Future
**Source:** Sprint 1 & 2 - Berlin 2023-24 was mild

**Description:**
Generate simulation data using a colder winter (e.g., 2010-2011) to stress-test algorithms.

**Rationale:**
- Berlin 2023-24 mean: 4.9°C, only 25 freezing days
- Upper clamping barely triggered (1.8% of data)
- Need colder data to fully test S-shape detection

**Implementation Notes:**
- Use Open-Meteo API for 2010-2011 Berlin data
- Or use other cold European cities
- Document differences in heating curve behavior

**Acceptance Criteria:**
- [ ] Cold winter dataset generated
- [ ] Upper clamping > 10% of data
- [ ] Algorithms tested on cold scenario

---

### 4.2 Building Thermal Inertia
**Priority:** P4
**Sprint:** Future
**Source:** Sprint 1 - Not implemented

**Description:**
Add building thermal inertia (lag τ = 2-6h) to simulation.

**Rationale:**
- Real buildings have thermal mass
- Vorlauf response lags behind outdoor temp changes
- More realistic for algorithm testing

**Implementation Notes:**
- Exponential moving average or low-pass filter
- τ configurable by building type
- Compare algorithm performance with/without lag

**Acceptance Criteria:**
- [ ] Thermal lag implemented in model.ipynb
- [ ] Configurable τ parameter
- [ ] Analysis notebook handles lagged data

---

### 4.3 Hysteresis Effects
**Priority:** P4
**Sprint:** Future
**Source:** Sprint 1 - Not implemented

**Description:**
Add controller hysteresis (1-2K dead band) to simulation.

**Rationale:**
- Real heating controllers have hysteresis
- Prevents rapid cycling (Taktverhalten)
- Adds realistic scatter to data

**Acceptance Criteria:**
- [ ] Hysteresis implemented in model.ipynb
- [ ] Configurable dead band parameter
- [ ] Analysis notebook handles hysteresis patterns

---

### 4.4 Boiler Cycling (Taktverhalten)
**Priority:** P4
**Sprint:** Future
**Source:** Sprint 1 - Not implemented

**Description:**
Simulate boiler on/off cycling patterns.

**Rationale:**
- Real boilers cycle on/off
- Creates characteristic patterns in Vorlauf data
- Important for energy efficiency analysis

**Acceptance Criteria:**
- [ ] Cycling pattern implemented
- [ ] Configurable cycle frequency
- [ ] Cycle detection algorithm developed

---

## 5. Visualization Improvements

### 5.1 Interactive Plots
**Priority:** P3
**Sprint:** Sprint 3 (Streamlit)
**Source:** Sprint 2 - Static matplotlib only

**Description:**
Create interactive plots using Plotly or Altair for Streamlit app.

**Rationale:**
- Users can zoom, pan, hover for details
- Better data exploration experience
- Professional presentation

**Acceptance Criteria:**
- [ ] Interactive scatter plots
- [ ] Hover tooltips with data values
- [ ] Zoom/pan functionality

---

### 5.2 Results Dashboard
**Priority:** P2
**Sprint:** Sprint 3 (Streamlit)
**Source:** Sprint 2 - Text-based results only

**Description:**
Create a visual dashboard summarizing extraction results.

**Rationale:**
- Easier to interpret than tables
- Highlights pass/fail status
- Comparison with benchmarks

**Acceptance Criteria:**
- [ ] Key metrics displayed prominently
- [ ] Color-coded pass/fail indicators
- [ ] Comparison with typical values

---

## 6. Technical Debt

### 6.1 Function Refactoring
**Priority:** P2
**Sprint:** Sprint 3
**Source:** Sprint 2 - Functions embedded in notebook

**Description:**
Extract key functions into a Python module for reuse.

**Rationale:**
- `extract_parameters()` function needed in Streamlit
- Avoid code duplication
- Enable unit testing

**Implementation Notes:**
- Create `heating_curve_analysis.py` module
- Extract: pattern detection, regression, parameter extraction
- Add type hints and docstrings

**Acceptance Criteria:**
- [ ] Module created with key functions
- [ ] Functions have type hints
- [ ] Unit tests written

---

### 6.2 Configuration Management
**Priority:** P3
**Sprint:** Future
**Source:** Sprint 2 - Hardcoded thresholds

**Description:**
Centralize algorithm configuration and thresholds.

**Rationale:**
- Thresholds scattered throughout notebook
- Difficult to tune and compare
- Should be configurable from one place

**Acceptance Criteria:**
- [ ] Config file or dataclass for all parameters
- [ ] Easy to modify for experiments
- [ ] Documentation of each parameter

---

## 7. Documentation

### 7.1 Algorithm Documentation
**Priority:** P3
**Sprint:** Future
**Source:** Sprint 2 - Limited algorithm explanations

**Description:**
Create detailed documentation of each algorithm's approach, assumptions, and limitations.

**Rationale:**
- Important for educational value and public reference
- Helps future developers and contributors
- Supports understanding for end users

**Acceptance Criteria:**
- [ ] Each algorithm documented
- [ ] Mathematical formulation included
- [ ] Assumptions and limitations listed

---

## Summary by Priority

### P1 - Critical
- [ ] 2.1 Missing Data Imputation

### P2 - High
- [ ] 1.1 Quantile Regression
- [ ] 1.2 Piecewise Linear Regression
- [ ] 1.4 T_base Extraction
- [ ] 2.2 Outlier Pre-filtering
- [ ] 5.2 Results Dashboard
- [ ] 6.1 Function Refactoring

### P3 - Medium
- [ ] 1.3 Ensemble Methods
- [ ] 2.3 Data Quality Scoring
- [ ] 3.1 Confidence Intervals
- [ ] 4.1 Cold Winter Data
- [ ] 5.1 Interactive Plots
- [ ] 6.2 Configuration Management
- [ ] 7.1 Algorithm Documentation

### P4 - Low
- [ ] 3.2 Prediction Intervals
- [ ] 4.2 Building Thermal Inertia
- [ ] 4.3 Hysteresis Effects
- [ ] 4.4 Boiler Cycling

---

## Sprint Assignment Suggestions

### Sprint 3 (Streamlit App)
- 5.1 Interactive Plots
- 5.2 Results Dashboard
- 6.1 Function Refactoring

### Sprint 4 (Algorithm Enhancement)
- 1.1 Quantile Regression
- 1.2 Piecewise Linear Regression
- 2.1 Missing Data Imputation

### Sprint 5 (Robustness)
- 1.4 T_base Extraction
- 2.2 Outlier Pre-filtering
- 2.3 Data Quality Scoring

### Future Sprints
- Remaining P3/P4 items as time permits

---

## 8. Sprint 3 Specific Items (from DEC-001)

### 8.1 Streamlit Application Core Features
**Priority:** P1
**Sprint:** Sprint 3
**Source:** DEC-001

**Weather Data Selection:**
- Location selector (city or coordinates)
- Date range picker (1940-present via Open-Meteo)
- Notable winter presets (2010-2011 cold, 2023-2024 mild)

**Heating Curve Parameter Controls:**
| Parameter | Range | Default |
|-----------|-------|---------|
| Slope (K) | 0.2 - 2.0 | 1.4 |
| Room target day | 18 - 24 | 20°C |
| Room target night | 14 - 20 | 16°C |
| T_vorlauf_max | 45 - 80 | 75°C |
| T_vorlauf_min | 20 - 35 | 25°C |
| Summer cutoff | 12 - 20 | 15°C |
| Night start hour | 20 - 24 | 22 |
| Night end hour | 4 - 8 | 6 |
| Noise level | Model 1/2/3 | Model 1 |

**Building Type Presets:**
| Preset | Slope | Description |
|--------|-------|-------------|
| Heat Pump + Floor Heating | 0.3 | Modern, well-insulated |
| Radiators + Good Insulation | 1.0 | Renovated building |
| Radiators + Poor Insulation | 1.4 | Older building (default) |
| Historic Building | 1.6 | Unrenovated, high heat loss |

**Outputs:**
- Real-time scatter plot (outdoor vs. Vorlauf)
- Heating curve visualization with day/night bands
- Summary statistics table
- Downloadable simulated dataset (CSV)
- Documentation in app sidebar

### 8.2 Sprint 3 File Structure
**Priority:** P2
**Sprint:** Sprint 3
**Source:** DEC-001

```
models/heating-curve/
    app/
        streamlit_app.py      # Main application
        config.py             # Default configurations
        heating_curve.py      # Core functions (extracted from notebook)
    model.ipynb
    analysis.ipynb
    outputs/
```

### 8.3 Analysis Algorithm Integration
**Priority:** P2
**Sprint:** Sprint 3
**Source:** Sprint 2 findings

Integrate Sprint 2 extraction algorithms into Streamlit app:
- User uploads CSV or uses simulated data
- App runs pattern detection (limits, modes)
- App fits OLS and RANSAC
- Results displayed with comparison table
- Visualization of fitted curves
- Export of estimated parameters
- Algorithm selector (OLS vs RANSAC)

---

## 9. Items from Sprint 1 (Deferred)

### 9.1 Weekend/Weekday Patterns
**Priority:** P4
**Sprint:** Future
**Source:** Sprint 1 plan Section 8

**Description:**
Add different heating schedules for weekdays vs weekends.

**Rationale:**
- Real buildings often have different schedules on weekends
- May affect day/night mode detection algorithms

---

## 10. Change Log

| Date | Change | Author |
|------|--------|--------|
| 2024-12 | Initial creation from Sprint 2 findings | Claude |
| 2024-12 | Added Sprint 3 items from DEC-001 | Claude |
| 2024-12 | Added deferred Sprint 1 items | Claude |

---

**Document maintained by:** Alberto Diaz Durana
**Last review:** 2024-12
