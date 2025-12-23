# Decision: Lower Vorlauf Maximum Temperature Scenario

**Decision ID:** DEC-002
**Date:** 2024-12
**Status:** Approved
**Context:** Sprint 1, Day 4 - Visualization revealed missing "S-shape" in scatter plots

---

## Problem Statement

The initial simulation with T_vorlauf_max = 75°C produced scatter plots showing only the diagonal heating curve slope, without the expected horizontal bands at temperature limits. This occurred because Berlin's mild 2023-24 winter (min -10.6°C) never triggered the upper temperature clamp.

**Expected shape:** S-pattern with:
1. Upper horizontal band (max Vorlauf reached on coldest days)
2. Diagonal slope (normal Heizkennlinie operation)
3. Lower horizontal band (min Vorlauf near summer cutoff)

---

## Decision

Create an additional scenario with T_vorlauf_max = 55°C to demonstrate full heating curve behavior including temperature clamping.

---

## Rationale

### Domain Justification

A 55°C maximum Vorlauftemperatur is realistic and represents:

1. **Heat pump compatible systems** - Heat pumps operate most efficiently with Vorlauf 35-55°C
2. **Well-optimized buildings** - Modern or renovated buildings with adequate radiator sizing
3. **Condensing boiler operation** - Ensures return temp stays below 55°C for Brennwertnutzung
4. **Industry benchmark** - 17% of German buildings already operate at Vorlauf < 55°C at -5°C outdoor

### Educational Value

- Demonstrates temperature clamping behavior
- Shows "S-shape" pattern visible in real heating data
- Illustrates how different building types produce different scatter patterns

---

## Consequences

### Positive Effects

| Benefit | Explanation |
|---------|-------------|
| Condensing operation | Gas boilers achieve Brennwertnutzung when return temp < 55°C |
| Heat pump efficiency | COP improves 30-50% at lower flow temps |
| Distribution losses | Lower ΔT = less heat lost in pipes |
| Heat pump readiness | Building can switch to heat pump without major renovation |

### Negative Effects / Risks

| Risk | Explanation |
|------|-------------|
| Undersized radiators | Old radiators designed for 70/55°C may underperform |
| Comfort issues | On coldest days, rooms may not reach 20°C target |
| Longer heating cycles | System runs longer to compensate |
| DHW limitations | 55°C is minimum for legionella prevention |

---

## Implementation

### New Configuration

```python
CONFIG_LOW_TEMP = {
    "slope": 1.4,
    "t_base": 20.0,
    "t_room_day": 20.0,
    "t_room_night": 16.0,
    "t_outdoor_summer_cutoff": 15.0,
    "t_vorlauf_min": 25.0,
    "t_vorlauf_max": 55.0,  # Changed from 75.0
    "night_start_hour": 22,
    "night_end_hour": 6,
}
```

### Expected Behavior

At T_outdoor = -10°C (coldest in dataset):
- Original: T_vorlauf = 62.8°C (no clamping)
- Low temp: T_vorlauf = 55.0°C (clamped)

Clamping occurs when T_outdoor < -5°C:
- T_vorlauf = 20 + 1.4 × (20 - (-5)) = 55°C

---

## Notebook Structure

New section added after main simulation:
1. Section header explaining scenario
2. Updated CONFIG_LOW_TEMP
3. Regenerate ideal Vorlauf with new limits
4. Apply same noise models
5. Generate comparison scatter plots showing S-shape

---

## Sprint 3 Integration

The Streamlit app will include T_vorlauf_max as a configurable slider (range: 45-80°C) allowing users to explore different building scenarios.

---

**Approved by:** Alberto Diaz Durana
**Implementation:** Sprint 1, Day 4 (continued)
