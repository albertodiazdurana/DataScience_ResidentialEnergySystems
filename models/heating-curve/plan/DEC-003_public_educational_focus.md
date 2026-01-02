# Decision: Public Educational Focus for Models

**Decision ID:** DEC-003
**Date:** 2024-12
**Status:** Approved
**Context:** End of Sprint 2, before Sprint 3

---

## Decision

The `models/` directory will be developed as a **public, generic, educational resource** independent of any specific company or interview context.

---

## Rationale

### Long-Term Vision

The goal is to create an **open-source collection of models and simulations for residential energy systems** that serves:

- Energy engineers validating system configurations
- Building managers understanding heating behavior
- Students and researchers learning fundamentals
- Data scientists seeking reference implementations
- General public exploring energy concepts

### Separation of Concerns

| Directory | Purpose | Audience |
|-----------|---------|----------|
| `models/` | Public educational modules | General public |
| `project-knowledge/` | Personal reference materials | Author only |

### Benefits

1. **Reusability**: Models can be shared, forked, and contributed to
2. **Credibility**: Generic tools are more trustworthy than company-specific demos
3. **Longevity**: Not tied to any specific interview or job application
4. **Community**: Enables future open-source contributions

---

## Changes Made

### Documents Updated

| Document | Change |
|----------|--------|
| `Sprint2_Handoff.md` | Changed "Green Fusion GmbH interview context" → "Algorithm selection based on data quality" |
| `BACKLOG_Improvements.md` | Changed "interview presentation" → "educational value and public reference" |
| `HeatingCurve_ProjectPlan_Sprint3.md` | Added Long-Term Vision, Target Audience, Value Proposition, Future Roadmap sections |

### Scope Boundaries

**In Scope (models/):**
- Heating curve simulation and analysis
- Future modules: Heat pump, district heating, solar thermal, etc.
- Generic domain knowledge and documentation
- Educational explanations and examples

**Out of Scope (models/):**
- Company-specific references
- Interview preparation context
- Job application materials

---

## Future Modules Roadmap

| Module | Description | Priority |
|--------|-------------|----------|
| Heating Curve | Heizkennlinie simulation and analysis | Current |
| Heat Pump | COP modeling, performance curves | High |
| District Heating | Fernwärme optimization, return temp | High |
| Solar Thermal | Collector efficiency, storage | Medium |
| Building Thermal Mass | Thermal inertia, response times | Medium |
| Hybrid Systems | Combined heat sources optimization | Low |
| Sector Coupling | PV + Heat Pump + Storage | Low |

---

## Platform Evolution

| Phase | Focus |
|-------|-------|
| Phase 1 | Individual module apps (Streamlit) |
| Phase 2 | Unified dashboard with module selection |
| Phase 3 | API for programmatic access |
| Phase 4 | Community contributions and extensions |

---

## Consequences

### Positive

- Broader audience reach
- More professional portfolio piece
- Foundation for open-source project
- Clear separation of personal vs public content

### Considerations

- Must maintain educational quality in documentation
- Code comments should be instructive, not just functional
- Examples should be generic and widely applicable

---

**Approved by:** Alberto Diaz Durana
**Implementation:** Sprint 3 onwards
