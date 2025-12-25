# Heating Curve Analysis - Project Plan

**Project:** Heating Curve Model for Residential Energy Systems
**Phase:** Sprint 2 - Algorithm Development (analysis.ipynb)
**Duration:** 1 week

**Prepared by:** Alberto Diaz Durana
**Previous Phase:** Sprint 1 - Functional Model (Complete)
**Next Phase:** Sprint 3 - Streamlit Application

---

## 1. Purpose

### Objective

Develop algorithms to extract heating curve parameters from noisy sensor data. The goal is to recover the known simulation parameters (slope, room targets, temperature limits) from the exported datasets, testing robustness across increasing noise levels.

### Deliverable

A Jupyter notebook (`analysis.ipynb`) implementing multiple extraction algorithms with comparative analysis, validated against known ground truth from Sprint 1.

### Success Priority

**Robustness over accuracy** - Algorithm should not break under extreme conditions or noisy data. Graceful degradation is acceptable.

---

## 2. Inputs

### Data Source

| File | Description | Scenario |
|------|-------------|----------|
| heating_curve_lowtemp.pkl | 55°C max scenario | Primary focus |
| config.json | Ground truth parameters | Validation reference |

### Ground Truth Parameters (from Sprint 1)

| Parameter | True Value |
|-----------|------------|
| Slope (K) | 1.4 |
| T_room_day | 20°C |
| T_room_night | 16°C |
| T_vorlauf_max | 55°C |
| T_vorlauf_min | 25°C |
| Night hours | 22:00 - 06:00 |

### Data Characteristics

| Model | Gaussian σ | Missing | Outliers | Records |
|-------|------------|---------|----------|---------|
| Model 1 | 1.5°C | 0% | 0% | 14,456 |
| Model 2 | 3.5°C | 0% | 0.5% | 14,456 |
| Model 3 | 5.0°C | 5% | 1.5% | ~13,700 |

---

## 3. Technical Approach

### Algorithm Progression (Simple → Complex)

| Level | Algorithm | Description |
|-------|-----------|-------------|
| 1 | Linear Regression (OLS) | Baseline, fast, interpretable |
| 2 | RANSAC Regression | Robust to outliers |
| 3 | Quantile Regression | Median-based, outlier resistant |
| 4 | Clustering + Regression | Separate day/night, then fit |
| 5 | Piecewise Linear | Capture S-shape with breakpoints |

### Missing Data Imputation Approaches

| Method | Description | Complexity |
|--------|-------------|------------|
| Drop NaN | Simple removal | Baseline |
| Forward fill | Use previous value | Simple |
| Linear interpolation | Interpolate gaps | Medium |
| Seasonal interpolation | Use same hour previous day | Medium |
| Model-based | Predict from outdoor temp | Complex |

### S-Shape Detection Strategy

The 55°C scenario produces an S-shape with:
- Upper plateau: T_vorlauf clamped at 55°C (cold outdoor)
- Linear slope: Normal Heizkennlinie operation
- Lower plateau: T_vorlauf clamped at 25°C (warm outdoor)

**Approach:** Detect breakpoints where clamping occurs, then fit linear model to middle segment.

---

## 4. Success Criteria

### Quantitative Metrics

| Metric | Target (Model 1) | Acceptable (Model 3) |
|--------|------------------|----------------------|
| Slope error | < 0.1 | < 0.3 |
| T_room_day error | < 1°C | < 2°C |
| T_room_night error | < 1°C | < 2°C |
| Day/night classification | > 95% | > 85% |
| R² (linear segment) | > 0.90 | > 0.70 |

### Qualitative Criteria

| Criterion | Requirement |
|-----------|-------------|
| Robustness | No crashes on any input |
| Missing data | Handles 5% gaps gracefully |
| Outlier resistance | Model 3 outliers don't dominate fit |
| Interpretability | All outputs have physical meaning |
| Performance | < 10 seconds on full dataset |
| Degradation | Smooth accuracy loss Model 1 → 3 |

---

## 5. Execution Timeline

### Overview

| Day | Focus | Key Deliverable |
|-----|-------|-----------------|
| Day 1 | Data Loading + EDA | Understand data characteristics |
| Day 2 | Baseline Algorithms | OLS, RANSAC, Quantile regression |
| Day 3 | Advanced Algorithms | Clustering + Piecewise linear |
| Day 4 | Imputation + Validation | Compare methods, test robustness |
| Day 5 | Documentation + Review | Results summary, Sprint 3 prep |

---

### Day 1 - Data Loading and EDA

**Goal:** Load Sprint 1 data and explore characteristics across noise models

#### Part 0: Setup and Data Loading

**Objective:** Load exported datasets and configuration
**Activities:**
- Import libraries
- Load heating_curve_lowtemp.pkl
- Load config.json for ground truth
- Verify data integrity
**Deliverables:**
- Loaded DataFrame
- Ground truth parameters accessible

#### Part 1: Exploratory Data Analysis

**Objective:** Understand data distributions and noise characteristics
**Activities:**
- Compare Model 1/2/3 distributions
- Visualize scatter plots with ground truth overlay
- Identify outliers and missing patterns
- Analyze day/night separation
**Deliverables:**
- EDA visualizations
- Noise characterization summary

#### Part 2: S-Shape Analysis

**Objective:** Identify clamping regions in 55°C scenario
**Activities:**
- Find temperature plateaus (upper/lower)
- Identify linear region boundaries
- Estimate breakpoint temperatures
**Deliverables:**
- Breakpoint estimates
- Segmented data view

#### End-of-Day 1 Checkpoint

**Questions:**
1. Are clamping regions clearly identifiable in Model 1?
2. How does noise obscure breakpoints in Model 2/3?
3. What outdoor temp range corresponds to linear region?

---

### Day 2 - Baseline Algorithms

**Goal:** Implement simple regression approaches

#### Part 0: Data Preparation

**Objective:** Prepare data for regression
**Activities:**
- Handle missing values (baseline: drop NaN)
- Separate day and night data using hour
- Filter to linear region (exclude clamped zones)
**Deliverables:**
- Clean datasets for regression

#### Part 1: Linear Regression (OLS)

**Objective:** Establish baseline performance
**Activities:**
- Fit OLS to full data
- Fit OLS to linear region only
- Fit separate models for day/night
- Extract slope and intercept
- Calculate errors vs ground truth
**Deliverables:**
- OLS results table
- Visualization of fitted curves

#### Part 2: RANSAC Regression

**Objective:** Add outlier robustness
**Activities:**
- Fit RANSAC with default parameters
- Tune residual threshold
- Compare inlier/outlier classification
- Extract parameters
**Deliverables:**
- RANSAC results
- Comparison with OLS

#### Part 3: Quantile Regression

**Objective:** Median-based robust regression
**Activities:**
- Fit quantile regression (median, q=0.5)
- Compare to OLS and RANSAC
- Assess outlier resistance
**Deliverables:**
- Quantile regression results
- Three-way comparison table

#### End-of-Day 2 Checkpoint

**Questions:**
1. Which baseline performs best on Model 1?
2. How much does RANSAC improve on Model 3?
3. Is day/night separation improving accuracy?

---

### Day 3 - Advanced Algorithms

**Goal:** Implement clustering and piecewise approaches

#### Part 0: Day/Night Clustering

**Objective:** Automatically separate operating modes
**Activities:**
- K-means clustering (k=2) on Vorlauf residuals
- Gaussian Mixture Model for soft assignment
- Compare to ground truth hour-based separation
- Evaluate classification accuracy
**Deliverables:**
- Clustering results
- Mode classification accuracy

#### Part 1: Cluster-Based Regression

**Objective:** Fit separate curves per cluster
**Activities:**
- Fit regression to each cluster
- Extract day/night room targets
- Calculate combined accuracy
**Deliverables:**
- Per-cluster parameters
- Improved estimates

#### Part 2: Piecewise Linear Regression

**Objective:** Capture S-shape with breakpoints
**Activities:**
- Define piecewise model (3 segments)
- Estimate breakpoints (optimization or grid search)
- Fit slopes to each segment
- Extract clamping temperatures
**Deliverables:**
- Breakpoint estimates
- Segment parameters

#### Part 3: Algorithm Comparison

**Objective:** Compare all approaches
**Activities:**
- Create comparison table (all algorithms × all models)
- Visualize fitted curves overlay
- Rank by robustness and accuracy
**Deliverables:**
- Comparison matrix
- Best algorithm recommendation

#### End-of-Day 3 Checkpoint

**Questions:**
1. Does clustering improve day/night separation?
2. Does piecewise model recover T_vorlauf_max accurately?
3. Which algorithm is most robust across Model 1→3?

---

### Day 4 - Imputation and Validation

**Goal:** Test missing data handling and final validation

#### Part 0: Imputation Methods

**Objective:** Compare approaches for handling missing data
**Activities:**
- Implement: drop, forward fill, linear interp, seasonal interp
- Apply each to Model 3 data
- Measure impact on parameter estimates
**Deliverables:**
- Imputation comparison table
- Best method recommendation

#### Part 1: Robustness Testing

**Objective:** Stress test algorithms
**Activities:**
- Test with increasing noise levels
- Test with higher missing rates (simulate 10%, 15%)
- Test with extreme outliers
- Document failure modes
**Deliverables:**
- Robustness report
- Failure mode documentation

#### Part 2: Final Validation

**Objective:** Comprehensive validation against ground truth
**Activities:**
- Run best algorithm on all models
- Calculate final error metrics
- Verify success criteria met
- Document any limitations
**Deliverables:**
- Final results table
- Success criteria checklist

#### Part 3: Sensitivity Analysis

**Objective:** Understand parameter sensitivity
**Activities:**
- Vary algorithm hyperparameters
- Assess stability of estimates
- Identify critical parameters
**Deliverables:**
- Sensitivity plots
- Hyperparameter recommendations

#### End-of-Day 4 Checkpoint

**Questions:**
1. Which imputation method works best?
2. Are all success criteria met?
3. What are the algorithm limitations?

---

### Day 5 - Documentation and Review

**Goal:** Finalize notebook and prepare Sprint 3

#### Part 0: Results Summary

**Objective:** Create comprehensive results section
**Activities:**
- Summary statistics table
- Algorithm comparison visualization
- Key findings narrative
**Deliverables:**
- Results markdown section
- Publication-quality figures

#### Part 1: Notebook Cleanup

**Objective:** Ensure notebook is clean and reproducible
**Activities:**
- Remove debug cells
- Ensure sequential execution
- Add cell numbers
- Verify all outputs display
**Deliverables:**
- Clean notebook

#### Part 2: Function Export

**Objective:** Prepare functions for Sprint 3 Streamlit
**Activities:**
- Identify functions to export
- Document function interfaces
- Test standalone execution
**Deliverables:**
- Function list for Sprint 3
- Interface documentation

#### Part 3: Sprint 2 Review

**Objective:** Complete sprint documentation
**Activities:**
- Write Sprint 2 handoff
- Document lessons learned
- Finalize Sprint 3 scope
**Deliverables:**
- Sprint 2 handoff document
- Sprint 3 refined plan

#### End-of-Day 5 Checkpoint

**Questions:**
1. Does notebook run end-to-end?
2. Are results reproducible?
3. Are functions ready for Streamlit integration?

---

## 6. Deliverables Summary

### Notebook

`analysis.ipynb` - Algorithm development and validation

### Functions to Implement

| Function | Purpose |
|----------|---------|
| `load_data()` | Load exported datasets |
| `impute_missing()` | Handle missing values |
| `detect_breakpoints()` | Find S-shape transitions |
| `fit_ols()` | Linear regression baseline |
| `fit_ransac()` | Robust regression |
| `fit_quantile()` | Quantile regression |
| `cluster_modes()` | Day/night clustering |
| `fit_piecewise()` | S-shape piecewise model |
| `extract_parameters()` | Get slope, room targets |
| `validate_results()` | Compare to ground truth |

### Figures

| Figure | Description |
|--------|-------------|
| EDA scatter plots | Model 1/2/3 comparison |
| S-shape analysis | Breakpoint identification |
| Algorithm comparison | Fitted curves overlay |
| Robustness plots | Performance vs noise level |
| Final results | Best algorithm validation |

### Documents

| Document | Description |
|----------|-------------|
| Sprint2_Handoff.md | Complete handoff for Sprint 3 |
| Algorithm comparison table | Accuracy × robustness matrix |

---

## 7. Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Algorithms fail on Model 3 | Medium | High | Start simple, add robustness iteratively |
| Breakpoint detection unstable | Medium | Medium | Use multiple detection methods |
| Day/night clustering incorrect | Low | Medium | Fall back to hour-based separation |
| Performance too slow | Low | Low | Optimize critical loops, sample data |
| Overfitting piecewise model | Medium | Medium | Cross-validation, regularization |

---

## 8. Dependencies on Sprint 1

| Dependency | Status | Notes |
|------------|--------|-------|
| heating_curve_lowtemp.pkl | Ready | 55°C scenario, primary focus |
| config.json | Ready | Ground truth parameters |
| Noise model definitions | Ready | NOISE_CONFIG documented |

---

## 9. Sprint 3 Preparation

Sprint 2 will produce functions ready for Streamlit integration:

**Analysis functions for Sprint 3:**
- Parameter extraction from user-uploaded data
- Real-time algorithm comparison
- Visualization of fitted curves
- Export of estimated parameters

**Integration points:**
- User uploads CSV or uses simulated data
- App runs extraction algorithm
- Results displayed with confidence intervals
- Comparison to simulation parameters (if available)

---

**End of Sprint 2 Project Plan**

**Document Version:** 1.0
**Created:** 2024-12
**Status:** Ready for execution
