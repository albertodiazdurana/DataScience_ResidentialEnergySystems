# Sprint 2 Handoff: Heating Curve Analysis

**Project:** Heating Curve Model for Residential Energy Systems
**Sprint:** 2 - Algorithm Development (Analysis)
**Status:** Complete
**Date:** 2024-12

---

## 1. Sprint Objective

Develop algorithms to extract heating curve parameters from noisy sensor data without prior knowledge of the system configuration.

**Outcome:** Successfully implemented and validated two regression algorithms (OLS and RANSAC) that extract heating curve slope and room temperature setpoints from realistic building data.

---

## 2. Data Source

### Input Data (from Sprint 1)

| File | Description | Records |
|------|-------------|---------|
| heating_curve_lowtemp.pkl | 55°C low-temp scenario | 14,589 |
| config.json | Ground truth parameters | - |

### Data Characteristics

| Model | Gaussian σ | DHW Spikes | Missing | Outliers | Records |
|-------|------------|------------|---------|----------|---------|
| Model 1 | 1.5°C | 0% | 0% | 0% | 14,456 |
| Model 2 | 3.5°C | 2% | 0% | 0.5% | 14,456 |
| Model 3 | 5.0°C | 3% | 5% | 1.5% | 13,706 |

### Ground Truth Parameters

| Parameter | Value |
|-----------|-------|
| Slope (K) | 1.4 |
| T_room_day | 20.0°C |
| T_room_night | 16.0°C |
| T_vorlauf_max | 55.0°C |
| T_vorlauf_min | 25.0°C |

---

## 3. Approach: No Prior Knowledge

**Critical Design Decision:** All algorithms developed without using ground truth parameters during extraction. Ground truth only used for final validation.

**Detection Strategy:**
1. Identify day/night modes from data patterns (clustering)
2. Detect temperature limits from distribution analysis
3. Extract heating curve parameters via regression
4. Validate against ground truth

---

## 4. Algorithms Implemented

### Part 1: Pattern Detection

#### Day/Night Mode Detection (K-Means Clustering)
- **Approach:** Cluster residuals from simple linear fit into 2 groups
- **Result:** 94.8% accuracy without using `is_night` column
- **Separation:** 5.41°C between day/night modes

#### Temperature Limit Detection (Percentile Analysis)
- **Approach:** Analyze top/bottom 1% of Vorlauf distribution for clustering
- **Results:**
  - Upper limit detected: 56.4°C (actual: 55.0°C, error: 1.4°C)
  - Lower limit detected: 26.2°C (actual: 25.0°C, error: 1.2°C)
- **Detection criteria:** Low std (< overall_std/3) indicates plateau

### Part 2: Regression Algorithms

#### Algorithm 1: OLS (Ordinary Least Squares)
- **Purpose:** Baseline, fast, interpretable
- **Method:** Separate linear regression for day/night modes
- **Data prep:** Filter to linear region (between detected limits)

#### Algorithm 2: RANSAC (Random Sample Consensus)
- **Purpose:** Robust to outliers
- **Method:** Iterative fitting with inlier/outlier classification
- **Parameters:** `min_samples=0.8`, `random_state=42`

---

## 5. Results Summary

### Pattern Detection Performance

| Task | Result | Status |
|------|--------|--------|
| Day/Night clustering accuracy | 94.8% | ✓ Excellent |
| Upper limit detection error | 1.4°C | ✓ Good |
| Lower limit detection error | 1.2°C | ✓ Good |
| Linear region identified | 97.1% of data | ✓ Excellent |

### Algorithm Performance

#### Model 1 (Clean Data, σ=1.5°C)

| Algorithm | K Error | T_day Error | T_night Error | R² | Status |
|-----------|---------|-------------|---------------|-----|--------|
| OLS | 0.0395 | 0.38°C | 0.41°C | 0.938 | ✓ PASS |
| RANSAC | 0.0240 | 0.23°C | 0.23°C | 0.943 | ✓ PASS |

#### Model 2 (Moderate Noise, σ=3.5°C)

| Algorithm | K Error | T_day Error | T_night Error | R² | Status |
|-----------|---------|-------------|---------------|-----|--------|
| OLS | 0.1581 | 1.95°C | 1.97°C | - | ~ Acceptable |
| RANSAC | 0.1183 | 1.36°C | 1.42°C | - | ~ Acceptable |

**RANSAC improvement:** 25-30% error reduction vs OLS

#### Model 3 (Noisy/Realistic, σ=5.0°C, 5% missing)

| Algorithm | K Error | T_day Error | T_night Error | R² | Status |
|-----------|---------|-------------|---------------|-----|--------|
| OLS | 0.3063 | 4.25°C | 4.34°C | - | ✗ FAIL |
| RANSAC | 0.2495 | 3.21°C | 3.34°C | - | ~ Acceptable |

**RANSAC improvement:** 20-25% error reduction vs OLS

### Success Criteria Assessment

| Criterion | Target (Model 1) | Achieved | Status |
|-----------|------------------|----------|--------|
| Slope error | < 0.1 | 0.024 (RANSAC) | ✓ PASS |
| T_room_day error | < 1°C | 0.23°C (RANSAC) | ✓ PASS |
| T_room_night error | < 1°C | 0.23°C (RANSAC) | ✓ PASS |
| R² (linear segment) | > 0.90 | 0.943 (RANSAC) | ✓ PASS |

| Criterion | Target (Model 3) | Achieved | Status |
|-----------|------------------|----------|--------|
| Slope error | < 0.3 | 0.250 (RANSAC) | ✓ PASS |
| T_room error | < 2°C | 3.2-3.3°C (RANSAC) | ✗ FAIL |

---

## 6. Key Findings

### Successes

1. **Pattern detection works without prior knowledge**
   - 94.8% accuracy in day/night mode detection
   - Temperature limits detected within 1-2°C of actual

2. **OLS is sufficient for clean data (Model 1)**
   - Meets all success criteria
   - Fast, interpretable, reliable

3. **RANSAC provides consistent improvement**
   - 20-30% error reduction on noisy data
   - Inlier rates: 99%+ on all models
   - Graceful degradation as noise increases

4. **Algorithms extract physically meaningful parameters**
   - Slope K: 1.36-1.38 (actual: 1.4)
   - Room temp separation: ~4°C (actual: 4°C)
   - Results align with heating system physics

### Challenges

1. **Model 3 exceeds both algorithms' capabilities**
   - 5% missing data + σ=5°C noise + outliers is too challenging
   - Temperature errors: 3.2-4.3°C (target: < 2°C)
   - Suggests need for advanced techniques

2. **Limited upper clamping in data**
   - Only 1.78% of data at 55°C upper limit
   - Berlin 2023-24 winter was mild (mean 4.9°C)
   - S-shape detection not fully tested

3. **Assumption of T_base = 20°C**
   - Current algorithms assume base temperature
   - Future work: extract T_base from data

---

## 7. Deliverables

### Notebook

`analysis.ipynb` - 22 cells, fully documented

### Functions Implemented

| Function | Purpose | Lines |
|----------|---------|-------|
| `extract_parameters()` | Extract heating curve params for any noise model | ~60 |

**Key operations:**
- Filter to linear region
- Separate day/night modes
- Fit OLS and RANSAC
- Convert regression params to heating curve params
- Calculate errors vs ground truth

### Figures (6)

| File | Description |
|------|-------------|
| analysis_model_comparison.png | Scatter plots: Model 1/2/3 comparison |
| analysis_eda_patterns.png | 4-panel EDA: scatter, histograms, day/night, outdoor temp |
| analysis_mode_detection.png | Detected vs actual day/night modes |
| analysis_ols_regression.png | OLS fitted curves for day/night |
| analysis_algorithm_comparison.png | Bar charts: OLS vs RANSAC errors across models |

### Key Metrics Exported

Available in notebook variables:
- `all_results`: Dictionary with all algorithm results
- `GROUND_TRUTH`: Configuration parameters
- `detected_upper`, `detected_lower`: Detected limits
- `accuracy`: Day/night clustering accuracy

---

## 8. Technical Insights

### Why RANSAC Outperforms OLS

1. **Outlier resistance:** DHW spikes and sensor errors don't dominate fit
2. **Inlier identification:** 99%+ inlier rate preserves core data
3. **Stable on degraded data:** Model 3 performance degradation is graceful

### Algorithm Limitations

1. **Cannot handle extreme missing data (>10%)**
2. **Assumes linear heating curve** (valid for 97% of data in this dataset)
3. **Requires day/night separation** (works via clustering or time-based)
4. **T_base assumed, not extracted** (fixable with 3-parameter regression)

### Berlin Winter 2023-24 Characteristics

- Mean outdoor: 4.9°C
- Coldest: -10.6°C (brief, Jan 9)
- Warmest: 21.7°C (March)
- Heating season data quality: Good for algorithm development
- Upper clamping: Minimal (1.8% of data)

---

## 9. Future Improvements (Sprint 3+)

### Advanced Algorithms (High Priority)

1. **Quantile Regression**
   - Median-based (q=0.5) for outlier resistance
   - May outperform RANSAC on Model 3

2. **Piecewise Linear Regression**
   - Explicitly model upper/lower plateaus + linear region
   - Better S-shape handling
   - Extract T_vorlauf_max directly from data

3. **Ensemble Methods**
   - Combine OLS, RANSAC, Quantile predictions
   - Weighted average based on data quality

### Preprocessing Improvements (Medium Priority)

1. **Missing Data Imputation**
   - Seasonal interpolation (use same hour, previous day)
   - Model-based (predict from outdoor temp + hour)
   - Compare imputation methods on Model 3

2. **Outlier Pre-filtering**
   - Z-score filtering before regression
   - Isolation forest for anomaly detection
   - Adaptive thresholds based on local variance

3. **Data Quality Scoring**
   - Compute noise level estimate from residuals
   - Flag low-quality periods
   - Weight data by quality in regression

### Uncertainty Quantification (Low Priority)

1. **Confidence Intervals**
   - Bootstrap for parameter uncertainty
   - Provide ± ranges for extracted params

2. **Prediction Intervals**
   - Show uncertainty in fitted curves
   - Useful for customer communication

---

## 10. Sprint 3 Integration Plan

### Functions Ready for Streamlit

The `extract_parameters()` function can be integrated into Sprint 3 app:

**Streamlit workflow:**
1. User uploads CSV or selects simulated data
2. App runs pattern detection (limits, modes)
3. App fits OLS and RANSAC
4. Results displayed with comparison table
5. Visualization of fitted curves
6. Export estimated parameters

**Additional features for Sprint 3:**
- Algorithm selector (OLS vs RANSAC)
- Data quality assessment widget
- Confidence interval display
- Comparison with simulation ground truth (if available)

---

## 11. Environment

### Packages Used

- pandas 2.3.3
- numpy 2.4.0
- matplotlib
- scikit-learn 1.8.0
- scipy 1.16.3
- jupyter
- ipykernel

### Setup Commands

```bash
cd models/heating-curve
.venv\Scripts\activate
uv pip install scikit-learn
jupyter notebook
```

---

## 12. File Structure

```
models/heating-curve/
├── model.ipynb                 # Sprint 1 simulation
├── analysis.ipynb              # Sprint 2 analysis (THIS SPRINT)
├── outputs/
│   ├── figures/
│   │   ├── analysis_model_comparison.png
│   │   ├── analysis_eda_patterns.png
│   │   ├── analysis_mode_detection.png
│   │   ├── analysis_ols_regression.png
│   │   └── analysis_algorithm_comparison.png
│   └── data/
│       ├── heating_curve_lowtemp.csv
│       ├── heating_curve_lowtemp.pkl
│       └── config.json
├── plan/
│   ├── HeatingCurve_ProjectPlan_Sprint1.md
│   ├── HeatingCurve_ProjectPlan_Sprint2.md
│   ├── Sprint1_Handoff.md
│   ├── Sprint2_Handoff.md (this document)
│   ├── DEC-001_sprint3_streamlit_app.md
│   └── DEC-002_vorlauf_max_55C_scenario.md
└── .venv/
```

---

## 13. Validation Checklist

- [x] Notebook runs end-to-end without errors
- [x] All figures generated and saved
- [x] Pattern detection achieves >90% accuracy
- [x] OLS meets success criteria on Model 1
- [x] RANSAC outperforms OLS on Model 2/3
- [x] Parameters physically interpretable
- [x] Ground truth only used for validation, not extraction
- [x] Results documented and reproducible
- [x] Functions ready for Sprint 3 integration

---

## 14. Sprint 2 Metrics

| Metric | Value |
|--------|-------|
| Days planned | 5 |
| Days actual | 1 |
| Notebook cells | 22 |
| Figures generated | 5 |
| Algorithms implemented | 2 |
| Models tested | 3 |
| Success criteria met | 5/6 (Model 1) |
| Code lines (estimates) | ~300 |

---

## 15. Conclusions

### What Worked Well

1. **No-prior-knowledge approach is viable**
   - Pattern detection and parameter extraction successful
   - Demonstrates real-world applicability

2. **RANSAC is the recommended algorithm**
   - Better performance across all noise levels
   - Minimal complexity increase vs OLS
   - Production-ready for Models 1 and 2

3. **Sprint plan was effective**
   - Clear progression: EDA → Detection → Regression → Validation
   - Iterative approach revealed insights

### What Needs Improvement

1. **Model 3 performance**
   - Current algorithms insufficient for highly degraded data
   - Advanced techniques needed (quantile, piecewise)

2. **S-shape handling**
   - Limited testing due to mild winter
   - Piecewise regression needed for full S-curve extraction

3. **T_base assumption**
   - Currently hardcoded to 20°C
   - Should be extracted from data

### Recommendation for Production Use

**Algorithm selection based on data quality:**

- **Model 1 data quality (clean sensors):** Use OLS (fast, interpretable)
- **Model 2 data quality (typical sensors):** Use RANSAC (robust, minimal overhead)
- **Model 3 data quality (degraded sensors):** Requires advanced preprocessing + quantile/piecewise regression
- **Real buildings:** Most likely Model 2 quality → RANSAC recommended

---

**Handoff prepared by:** Claude (AI Assistant)
**Reviewed by:** Alberto Diaz Durana
**Date:** 2024-12
**Next Sprint:** Sprint 3 - Streamlit Application
