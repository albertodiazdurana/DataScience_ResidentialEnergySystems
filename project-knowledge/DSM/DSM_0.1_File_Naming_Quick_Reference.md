# File Naming Quick Reference Card

**Convention:** `sYY_dXX_PHASE_description.ext`

**Version:** 1.1
**Last Updated:** 2025-12-13

---

## Phase Codes
- `SETUP` - Environment, data acquisition
- `EDA` - Exploratory data analysis
- `FE` - Feature engineering
- `MODEL` - Modeling and validation
- `REPORT` - Communication

---

## By File Type

| Type | Working (S1-3) | Final (S4) |
|------|----------------|------------|
| **Notebook** | `s02_d01_FE_lags.ipynb` | `03_FE_lags-rolling.ipynb` |
| **Dataset** | `s02_d01_FE_with-lags.pkl` | `FE_features_v1.pkl` |
| **Visualization** | `s02_d01_FE_lag-validation.png` | `fig03_FE_lags.png` |
| **Decision** | `DEC-011_lag-nan-strategy.md` | (unchanged) |
| **Checkpoint** | `s02_d01_checkpoint.md` | (unchanged) |

---

## Examples by Sprint

**Sprint 1 (EDA):**
- `s01_d01_SETUP_data-inventory.ipynb`
- `s01_d02_EDA_data-loading.ipynb`
- `s01_d03_EDA_quality-check.ipynb`
- `s01_d04_EDA_temporal-patterns.ipynb`
- `s01_d05_EDA_context-export.ipynb`

**Sprint 2 (Feature Engineering):**
- `s02_d01_FE_lags.ipynb`
- `s02_d02_FE_rolling.ipynb`
- `s02_d03_FE_oil.ipynb`
- `s02_d04_FE_aggregations.ipynb`
- `s02_d05_FE_final.ipynb`

**Sprint 3 (Modeling):**
- `s03_d01_MODEL_baseline-naive.ipynb`
- `s03_d02_MODEL_baseline-arima.ipynb`
- `s03_d03_MODEL_prophet.ipynb`
- `s03_d04_MODEL_lstm.ipynb`
- `s03_d05_MODEL_comparison.ipynb`

**Sprint 4 (Consolidation):**
- `01_SETUP_environment-data.ipynb`
- `02_EDA_comprehensive.ipynb`
- `03_FE_lags-rolling-aggregations.ipynb`
- `04_MODEL_baseline-advanced.ipynb`
- `05_REPORT_final-presentation.ipynb`

---

## Locations

```
notebooks/           # sYY_dXX_*.ipynb
data/
  processed/         # sYY_dXX_*.pkl (working)
  results/           # PHASE_*_vX.pkl (final)
outputs/
  figures/
    eda/             # sYY_dXX_EDA_*.png
    features/        # sYY_dXX_FE_*.png
    models/          # sYY_dXX_MODEL_*.png
    final/           # figXX_*.png (Sprint 4)
docs/
  decisions/         # DEC-XXX_*.md
  plans/             # sYY_dXX_checkpoint.md
  reports/           # sYY_PHASE_report.md
```

---

## Rules

1. **Sprint-first:** `sYY_dXX` not `dXX_sYY`
2. **Lowercase descriptions:** `lag-validation` not `Lag_Validation`
3. **Hyphens, not underscores:** `temporal-patterns` not `temporal_patterns`
4. **1-3 words max:** `rolling-smoothing` not `rolling-smoothing-validation-plot`
5. **Phase code required:** `s02_d01_FE_lags` not `s02_d01_lags`

---

## Sprint 4 Consolidation

**Notebooks:** Merge daily → Sequential (01, 02, 03...)
**Datasets:** Move final to results/, archive working
**Visualizations:** Select best → figXX prefix, archive working
**Documentation:** Keep all (timestamped record)

---

## Quick Checklist

Before creating any file, ask:
- [ ] Is sprint number first? (`sYY_dXX`)
- [ ] Is phase code included?
- [ ] Is description lowercase with hyphens?
- [ ] Is description 1-3 words?
- [ ] Does it match the pattern for this file type?

---

**Print this card and keep it visible while working!**

**For detailed guidance, see:** Appendix E.11 in `1.0_Methodology_Appendices.md`

**Part of:** Data Science with Claude Methodology v1.1.1
