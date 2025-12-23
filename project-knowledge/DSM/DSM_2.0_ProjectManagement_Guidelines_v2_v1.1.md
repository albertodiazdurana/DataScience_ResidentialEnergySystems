# Project Management Guidelines for Data Science Projects

# Table of Contents - Project Management Guidelines v2

## Core Sections
- [Purpose](#purpose)
- [Project Structure Overview](#project-structure-overview)
  - [Technical Prerequisites](#technical-prerequisites)
  - [Technical Deliverables](#technical-deliverables)
  - [Phase 1 Readiness Checklist](#phase-1-readiness-checklist)

## Planning Templates
- [Plan Structure Templates](#plan-structure-templates)
  - [Template 1: Daily Task Breakdown Format](#template-1-daily-task-breakdown-format)
  - [Template 2: Phase Summary Format](#template-2-phase-summary-format)
  - [Template 3: Expected Outcomes Table Format](#template-3-expected-outcomes-table-format)
  - [Template 4: Phase Prerequisites Format](#template-4-phase-prerequisites-format)
  - [Template 5: Time Buffer Allocation Guidance](#template-5-time-buffer-allocation-guidance)

## Style and Best Practices
- [Recommended Style and Structure](#recommended-style-and-structure)
- [Tone and Style](#tone-and-style)
- [Example Project Flow](#example-project-flow)
- [Best Practices](#best-practices)
- [File Naming Standards](#file-naming-standards)

## Reference
- [Template Reference](#template-reference)

---

**Note:** For production/enterprise projects requiring governance, quality assurance, and risk management, reference **2.1_PM_ProdGuidelines_extension.md**

## Purpose

This document provides a standardized framework for planning, executing, and documenting data science projects.  
It ensures consistency, efficiency, and clarity across all phases â€” from data preparation to modeling and deployment.

**Objective:** Establish a clear, time-bound, and reproducible plan that delivers measurable outcomes aligned with business goals.

---

## Project Structure Overview

Each project plan should include the following core sections:

1. **Purpose**
   - Define the projectâ€™s main objective and deliverable.
   - Describe the expected impact or business value.
   - Specify available resources and time allocation.

2. **Inputs & Dependencies**
   - List all input datasets and their key characteristics (record count, features, source).
   - Reference outputs or dependencies from prior project phases.
   - Document data quality assumptions and preprocessing status.

### Technical Prerequisites

Before beginning Phase 1 work:

**Environment Setup:**
Run base environment setup script:
- Academic/exploratory: `setup_base_environment_minimal.py`
- Production/team: `setup_base_environment_prod.py`

**Environment Requirements:**
- Python virtual environment (`.venv`)
- Base packages installed (see Methodology Section 2.1 (Phase 0: Environment Setup))
- Jupyter kernel registered and functional
- VS Code configured with required extensions

**Note:** Minimal setup recommended for academic work (no formatting/linting).
See Collaboration Methodology Section 2.1 (Phase 0: Environment Setup) for details.

**Verification:**
- [ ] `requirements_base.txt` generated
- [ ] All base packages import successfully
- [ ] Jupyter kernel selectable in VS Code
- [ ] Code formatting and linting active

**Reference:** See Collaboration Methodology Section 2.1 (Phase 0: Environment Setup): Environment Setup for complete instructions.

3. **Execution Timeline**
   - Break the project into daily or sprint milestones.
   - Define key focus areas and deliverables for each time unit.
   - Provide estimated effort per phase (in hours or days).

4. **Detailed Deliverables**
   - Clearly outline goals, deliverables, and success metrics for each milestone.
   - Use bullet points to describe analytical steps, validation checks, and outputs.
   - Include both technical (code, models, reports) and analytical deliverables (insights, recommendations).
### Technical Deliverables

**Environment Documentation:**
- `requirements_base.txt` - Base environment packages
- `requirements_domain.txt` or `requirements_full.txt` - Complete package list
- `.vscode/settings.json` - VS Code configuration
- `setup_domain_extensions.py` - Custom extension script (if applicable)

**Purpose:** Enable environment reproduction by collaborators or for deployment

5. **Readiness Checklist**
   - Define preconditions for transitioning to the next phase (e.g., modeling readiness, deployment readiness).
   - Include data validation, documentation completeness, and reproducibility checks.

### Phase 1 Readiness Checklist

Before beginning data exploration:

**Environment Readiness:**
- [ ] Virtual environment created and activated
- [ ] All base packages installed and verified
- [ ] Jupyter kernel registered and selectable
- [ ] VS Code extensions installed and functional
- [ ] Domain-specific packages installed (if needed)
- [ ] Test notebook runs without import errors

6. **Success Criteria**
   - Quantitative: measurable indicators of completion or quality (e.g., number of features, model performance).
   - Qualitative: alignment with business logic, interpretability, or stakeholder expectations.
   - Technical: data quality, code reproducibility, and version control compliance.

7. **Documentation & Ownership**
   - Ensure all scripts, notebooks, and datasets are versioned and linked to the project plan.
   - Document assumptions, transformations, and limitations.
   - Include author name, role, and project timeline.

---

## Plan Structure Templates

The following templates provide standardized formats for organizing sprint/daily project plans. These templates help maintain consistency across all project phases.

### Template 1: Daily Task Breakdown Format

Break each day into timed parts with clear objectives and deliverables.

**Format:**
```markdown
### Day X - [Focus Area]
**Goal:** [One sentence objective]

**Total Time:** [X hours] (configure based on your sprint length - see DSM_0 Section 1.5)

#### Part 0: [Task Name] ([Duration])
**Objective:** [What this accomplishes]
**Activities:**
- [Activity 1]
- [Activity 2]
**Deliverables:**
- [Output 1]
- [Output 2]

#### Part 1: [Task Name] ([Duration])
**Objective:** [What this accomplishes]
**Activities:**
- [Activity 1]
- [Activity 2]
**Deliverables:**
- [Output 1]
- [Output 2]

[Repeat for Parts 2, 3, 4...]
```

**Example:**
```markdown
### Day 1 - Project Setup & Planning
**Goal:** Establish project structure and validate environment

**Total Time:** 4 hours

#### Part 0: Environment Configuration (30 min)
**Objective:** Set up development environment and validate database connection
**Activities:**
- Install required Python libraries
- Test database connectivity
- Create project folder structure
**Deliverables:**
- Working Jupyter environment
- Successful database connection
- Project directory structure

#### Part 1: Data Inventory (1 hour)
**Objective:** Document available datasets and schemas
**Activities:**
- Query table schemas
- Count records per table
- Identify primary/foreign keys
**Deliverables:**
- Data inventory report
- Schema documentation
```

---

### Template 2: Phase Summary Format

Provide standardized summaries at end of each day/phase showing time allocation and achievements.

**Format:**
```markdown
## [Day/Phase] Summary

### Time Allocation ([X] hours total):
| Task           | Duration      | Percentage |
| -------------- | ------------- | ---------- |
| Part 0: [Task] | [X] min/hours | [Y]%       |
| Part 1: [Task] | [X] min/hours | [Y]%       |
| Part 2: [Task] | [X] min/hours | [Y]%       |
| **Total**      | **[X] hours** | **100%**   |

### Key Achievements:
- [Achievement 1]
- [Achievement 2]
- [Achievement 3]

### Outputs Created:
- [File/deliverable 1]
- [File/deliverable 2]
- [File/deliverable 3]

### Issues Encountered:
- [Issue 1 and resolution]
- [Issue 2 and resolution]
- None (if applicable)

### Ready for Next Phase:
- [Prerequisite 1 met]
- [Prerequisite 2 met]
```

**Example:**
```markdown
## Day 1 Summary

### Time Allocation ([X] hours total):
| Task                            | Duration    | Percentage |
| ------------------------------- | ----------- | ---------- |
| Part 0: Environment Setup       | 30 min      | 12.5%      |
| Part 1: Data Inventory          | 1 hour      | 25%        |
| Part 2: Initial Data Extraction | 1.5 hours   | 37.5%      |
| Part 3: Documentation           | 1 hour      | 25%        |
| **Total**                       | **[X] hours** | **100%**   |

### Key Achievements:
- Development environment fully operational
- All 4 source tables documented
- Initial dataset extracted (5,765 users)

### Outputs Created:
- `environment_setup_log.txt`
- `data_inventory_report.csv`
- `users_initial.csv`

### Issues Encountered:
- Database timeout on large query (resolved by adding LIMIT during testing)

### Ready for Next Phase:
- Database connection validated
- Data structure understood
- Project repository organized
```

---

### Template 3: Expected Outcomes Table Format

Quantify expected results with before/after comparisons and measurable improvements.

**Format:**
```markdown
## Expected Outcomes

| Metric      | Before             | After             | Improvement     | Target Met        |
| ----------- | ------------------ | ----------------- | --------------- | ----------------- |
| [Metric 1]  | [Value]            | [Value]           | [+X%]           | Yes/No            |
| [Metric 2]  | [Value]            | [Value]           | [+X%]           | Yes/No            |
| **Summary** | **[Total before]** | **[Total after]** | **[Overall %]** | **[X/Y targets]** |

### Key Benefits:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]
```

**Example:**
```markdown
## Expected Outcomes

| Metric           | Before           | After           | Improvement       | Target Met      |
| ---------------- | ---------------- | --------------- | ----------------- | --------------- |
| Notebooks        | 15 files         | 6 files         | -60%              | Yes             |
| Total lines      | ~7,000           | ~3,200          | -54%              | Yes             |
| Code duplication | High             | Minimal         | N/A               | Yes             |
| Avg file size    | Variable         | 400-650 lines   | Standardized      | Yes             |
| **Summary**      | **15 notebooks** | **6 notebooks** | **60% reduction** | **4/4 targets** |

### Key Benefits:
- Easier code review and maintenance
- Consistent structure across all stages
- Professional repository organization
- Better modularity for iteration
```

---

### Template 4: Phase Prerequisites Format

Define clear handoff criteria between phases to ensure readiness.

**Format:**
```markdown
## Phase [X] Prerequisites

### Required Inputs:
- [ ] [Input 1 with specifications]
- [ ] [Input 2 with specifications]
- [ ] [Input 3 with specifications]

### Completion Criteria:
- [ ] [Criterion 1 - measurable]
- [ ] [Criterion 2 - measurable]
- [ ] [Criterion 3 - measurable]

### Quality Checks:
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

### Deliverables Ready:
- [ ] [Deliverable 1: filename/description]
- [ ] [Deliverable 2: filename/description]
- [ ] [Deliverable 3: filename/description]

### Next Phase Readiness:
After completing this phase, you will have:
- [Asset 1]
- [Asset 2]
- [Asset 3]
```

**Example:**
```markdown
## Phase 2 Prerequisites (Feature Engineering)

### Required Inputs:
- [ ] Clean user dataset (`users_cleaned.csv`, 5,765 rows)
- [ ] Validated cohort definition (>7 sessions, age 18-100)
- [ ] Data quality report showing <5% missing values

### Completion Criteria:
- [ ] All outliers removed using IQR method
- [ ] No missing values in critical fields
- [ ] User-level aggregation complete

### Quality Checks:
- [ ] Data types validated
- [ ] Range checks passed for all numerical fields
- [ ] Duplicate user_ids removed

### Deliverables Ready:
- [ ] `01_EDA_data_quality.ipynb` (runs without errors)
- [ ] `02_EDA_behavioral_analysis.ipynb` (runs without errors)
- [ ] `users_clean_final.csv` (validated dataset)

### Next Phase Readiness:
After completing Phase 1, you will have:
- Clean, validated user-level dataset ready for feature engineering
- Understanding of data distributions and patterns
- Documented data quality decisions
```

---

### Template 5: Time Buffer Allocation Guidance

**Recommended Buffer Strategy:**

When planning each phase, allocate buffers to account for unexpected issues:

| Phase Duration | Recommended Buffer | Example                          |
| -------------- | ------------------ | -------------------------------- |
| 1-2 days       | 15% buffer         | 4 hours work = 4.6 hours planned |
| 3-5 days       | 20% buffer         | 20 hours work = 24 hours planned |
| 1 sprint+      | 25% buffer         | 40 hours work = 50 hours planned |

**Buffer Allocation Guidelines:**
- Include buffer in timeline estimates, not as separate line item
- Use buffer for: unexpected data issues, stakeholder requests, learning new tools
- If buffer unused, apply to quality improvements or next phase prep
- Document actual time spent vs. planned to improve future estimates

**Example Planning:**
```markdown
Sprint 2: Feature Engineering
- Core work: 16 hours
- Buffer (20%): 4 hours
- Total planned: 20 hours (adjust daily breakdown based on sprint configuration)

Daily breakdown (example for 5-day sprint):
- Day 1: 3.2 hours core + 0.8 buffer = 4 hours
- Day 2: 3.2 hours core + 0.8 buffer = 4 hours
[...]
```

**Risk-Based Buffer Adjustment:**
- High uncertainty (new tools/methods): +25-30% buffer
- Medium uncertainty (familiar work): +15-20% buffer
- Low uncertainty (repeated tasks): +10-15% buffer

---

## Advanced Planning Framework: Version 2.0 Enhancements

**When to use Version 2.0 planning:**
- First time executing a complex phase with uncertain estimates
- Projects with substantial buffer (>20%) worth protecting
- Phases prone to scope creep (exploration, feature engineering, analysis)
- When daily reflection and mid-course correction add value
- Multi-day phases (3-5+ days) where early drift detection matters

**Core principle:** Invest 15 minutes daily in structured reflection to enable agile adaptation and protect buffer health.

---

### Template 6: Daily Checkpoint Framework

**Purpose:** Enable systematic daily review to detect drift, adjust scope, and maintain buffer discipline.

**Time allocation:** 15 minutes at end of each working day (built into buffer)

**Format:**
```markdown
## Day X Checkpoint - [Phase Name] (YYYY-MM-DD)

### Time Tracking
- **Allocated:** [X] hours ([X]h core + [X]h buffer)
- **Actual:** [X.X] hours
- **Variance:** [+/-X.X] hours
- **Reason for variance:** [Brief explanation]

### Scope Completion
- [ ] Part 0: [Task name] - [Complete/Partial/Not started]
- [ ] Part 1: [Task name] - [Complete/Partial/Not started]
- [ ] Part 2: [Task name] - [Complete/Partial/Not started]
- [ ] Part 3: [Task name] - [Complete/Partial/Not started]
- [ ] Part 4: [Task name] - [Complete/Partial/Not started]

**Completion Rate:** [X/Y parts complete] = [XX%]

### Key Findings
1. **Most important finding:** [1-2 sentences]
2. **Second most important finding:** [1-2 sentences]
3. **Unexpected discovery:** [1-2 sentences or "None"]

### Quality Assessment
- **Output quality:** [Excellent/Good/Needs improvement] - [Why?]
- **Validation results:** [All passed/Partial/Failed] - [Details]
- **Technical performance:** [Within/Over budget] - [Metrics]
- **Code/analysis quality:** [Clean/Needs work/Has issues]

### Blockers & Issues
- **Technical blockers:** [List or "None"]
- **Data/resource issues:** [List or "None"]
- **Conceptual challenges:** [List or "None"]
- **Mitigation actions taken:** [What did you do?]

### Buffer Status
- **Day X buffer allocated:** [X]h
- **Day X buffer used:** [X.X]h
- **Day X buffer remaining:** [X.X]h
- **Cumulative buffer remaining:** [X.X]h / [Y.Y]h total
- **Buffer health:** [Healthy (>threshold) / Caution / Critical]

### Progress Tracking (if using priority tiers)
**MUST Deliverables ([X] total):**
- [ ] [Item 1] - [Complete/In progress/Planned]
- [ ] [Item 2] - [Complete/In progress/Planned]

**SHOULD Deliverables ([X] total):**
- [ ] [Item 3] - [Complete/In progress/Planned]
- [ ] [Item 4] - [Complete/In progress/Planned]

**COULD Deliverables ([X] total):**
- [ ] [Item 5] - [Complete/Skipped/Planned]

**Total Progress Today:** [X] deliverables completed  
**Cumulative Progress:** [XX] / [YY] target

### Adjustment Decisions for Day X+1

**Scope Changes:**
- [ ] Keep plan as-is
- [ ] Add activity: [Specify what and why]
- [ ] Remove activity: [Specify what and why]
- [ ] Simplify approach: [Specify what and why]

**Time Reallocation:**
- [ ] No changes needed
- [ ] Increase time for: [Activity] by [X] minutes
- [ ] Decrease time for: [Activity] by [X] minutes

**Priority Adjustment:**
- [ ] Maintain current priority structure
- [ ] Focus only on MUST deliverables (contingency triggered)
- [ ] Skip COULD deliverables to preserve buffer

### Next Day Preview
**Day X+1 Primary Objectives:**
1. [Objective 1]
2. [Objective 2]

**Day X+1 Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Day X+1 Contingency Plan (if behind):**
- [What will you cut or simplify?]

### Decision Log Updates
- **DEC-XXX:** [Brief decision title]
  - Context: [1 sentence]
  - Decision: [1 sentence]
  - Impact: [What does this affect?]

### Notes & Learnings
- **What worked well today:** [1-2 items]
- **What could be improved:** [1-2 items]
- **Insights for next phase:** [Anything to carry forward]

### Appendix: Outputs Created

**Datasets:**
- `path/to/dataset.pkl` ([rows] rows x [cols] columns, [size] MB)

**Visualizations:**
- `path/to/figure.png` (description)

**Documentation:**
- `path/to/document.md` (purpose)

**Notebooks:**
- `path/to/notebook.ipynb` ([cells] cells, ~[lines] lines)

---

**Checkpoint completed by:** [Name]
**Time spent on checkpoint:** [X] minutes (target: <=15 min)
**Next checkpoint:** Day [X+1], [Date]
```

**Filename Convention:** `sXX_dXX_checkpoint.md` (e.g., s01_d03_checkpoint.md)

**Location:** `docs/checkpoints/` or `docs/plans/`

**Benefits of Daily Checkpoints:**
- Enables recovery if session interrupted
- Tracks progress systematically
- Documents decisions as they're made
- Identifies issues early
- Provides foundation for handoff documents

---

### Template 7: Progressive Expected Outcomes Table

**Purpose:** Track incremental progress across multi-day phases to enable early drift detection and scope adjustment.

**When to use:** Phases lasting 3+ days with clear mid-phase milestones

**Format:**
```markdown
## Expected Outcomes

| Metric      | Before Phase       | After Days [1-X]       | After Phase Complete | Target Met        |
| ----------- | ------------------ | ---------------------- | -------------------- | ----------------- |
| [Metric 1]  | [Baseline]         | [Intermediate]         | [Final]              | Yes/No            |
| [Metric 2]  | [Baseline]         | [Intermediate]         | [Final]              | Yes/No            |
| [Metric 3]  | [Baseline]         | [Intermediate]         | [Final]              | Yes/No            |
| **Summary** | **[Total before]** | **[Milestone status]** | **[Total after]**    | **[X/Y targets]** |

### Key Benefits
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]
```

**Example: 5-day Feature Engineering Phase**
```markdown
## Expected Outcomes

| Metric            | Before Sprint 2      | After Days 1-2              | After Sprint 2 (Days 3-5)  | Target Met      |
| ----------------- | -------------------- | --------------------------- | -------------------------- | --------------- |
| Feature count     | 28 columns           | 28 + 10 (core features)     | 54-58 columns              | Yes             |
| Core features     | 0                    | 10 complete                 | 10 validated               | Yes             |
| Advanced features | 0                    | 0 (planned Days 3-5)        | 15-20 complete             | Yes             |
| Optional features | 0                    | 0                           | 0-3 complete               | Conditional     |
| **Summary**       | **Baseline dataset** | **Core features milestone** | **Modeling-ready dataset** | **3/3 targets** |

### Key Benefits
- Early detection of scope issues (after Day 2 review)
- Mid-phase adjustment based on milestone achievement
- Clear go/no-go decision point before advanced work
```

---

### Template 8: Cumulative Buffer Tracking Table

**Purpose:** Monitor buffer health in real-time to trigger contingency plans before schedule crisis.

**When to use:** Projects with carryover buffer from previous phases or substantial initial buffer (>20%)

**Format:**
```markdown
## Cumulative Buffer Tracking

| Checkpoint             | Buffer Allocated | Buffer Used | Buffer Remaining       | Notes                         |
| ---------------------- | ---------------- | ----------- | ---------------------- | ----------------------------- |
| [Prior Phase] Complete | [X]h allocated   | [Y]h actual | +[X-Y]h surplus        | [Efficiency %]                |
| [Current Phase] Start  | +[Z]h ([%])      | 0h          | **[Total]h available** | Strong/Adequate/Weak position |
| End of Day 1           | [X]h             | TBD         | TBD                    | Update after Day 1 checkpoint |
| End of Day 2           | [X]h cumulative  | TBD         | TBD                    | Update after Day 2 checkpoint |
| End of Day 3           | [X]h cumulative  | TBD         | TBD                    | **Critical review point**     |
| End of Day 4           | [X]h cumulative  | TBD         | TBD                    | Update after Day 4 checkpoint |
| End of Day 5           | [X]h cumulative  | TBD         | TBD                    | Final buffer status           |

**Buffer Management Strategy:**
- If Days 1-2 under budget â†’ Proceed with full scope
- If Days 1-2 on budget â†’ Maintain current scope
- If Days 1-2 over budget â†’ Reduce scope (SHOULD â†’ MUST only)
- Critical threshold: If buffer drops below [X]h after Day 3, trigger contingency plan
```

**Example:**
```markdown
## Cumulative Buffer Tracking

| Checkpoint        | Buffer Allocated | Buffer Used | Buffer Remaining | Notes                            |
| ----------------- | ---------------- | ----------- | ---------------- | -------------------------------- |
| Sprint 1 Complete | 23.5h allocated  | 15h actual  | +8.5h surplus    | 64% efficiency                   |
| Sprint 2 Start    | +4h (20%)        | 0h          | **12.5h total**  | Strong buffer position           |
| End of Day 1      | 0.8h             | 0.5h        | 12.3h            | Ahead of schedule                |
| End of Day 2      | 1.6h cumulative  | 1.4h        | 11.6h            | On track                         |
| End of Day 3      | 2.4h cumulative  | 2.8h        | 10.9h            | **Healthy - proceed**            |
| End of Day 4      | 3.2h cumulative  | 3.5h        | 10.6h            | Slightly over, manageable        |
| End of Day 5      | 4h cumulative    | 4.2h        | 10.3h            | Final buffer: 10.3h for Sprint 3 |

**Buffer Management Strategy:**
- If Days 1-2 under budget â†’ Proceed with all SHOULD + COULD features
- If Days 1-2 on budget â†’ Complete all SHOULD, selective COULD
- If Days 1-2 over budget â†’ Focus on MUST + SHOULD only, skip COULD
- Critical threshold: If buffer drops below 8h after Day 3, trigger contingency
```

---

### Template 9: MUST/SHOULD/COULD Priority Framework

**Purpose:** Structured prioritization to prevent "everything is important" paralysis and enable clear scope reduction decisions.

**When to use:** Complex phases with >10 deliverables, risk of scope creep, or uncertain capacity

**Framework:**

**MUST Deliverables (20-30% of total):**
- Critical for phase completion
- Blocks next phase if incomplete
- Non-negotiable, even if behind schedule
- Complete first, validate thoroughly

**SHOULD Deliverables (50-60% of total):**
- High value, expected if on schedule
- Enhances quality but not strictly blocking
- Complete if Days 1-2 on/under budget
- Skip selectively if behind schedule

**COULD Deliverables (10-20% of total):**
- Bonus features if ahead of schedule
- Exploratory or "nice to have"
- First to cut when time constrained
- Defer to future phases if needed

**Format:**
```markdown
## Success Criteria - Structured by Priority

**MUST Deliverables ([X] total - Non-negotiable):**
- [ ] [Deliverable 1] - [Description]
- [ ] [Deliverable 2] - [Description]
- [ ] [Deliverable 3] - [Description]

**SHOULD Deliverables ([X] total - Complete if on schedule):**
- [ ] [Deliverable 4] - [Description]
- [ ] [Deliverable 5] - [Description]
- [ ] [Deliverable 6] - [Description]

**COULD Deliverables ([X] total - Only if ahead):**
- [ ] [Deliverable 7] - [Description]
- [ ] [Deliverable 8] - [Description]

**Contingency Rules:**
- If on schedule after Day 2 â†’ Full scope (MUST + SHOULD + COULD)
- If 10-20% behind after Day 2 â†’ MUST + SHOULD only
- If >20% behind after Day 2 â†’ MUST only, document deferred work
```

**Example:**
```markdown
## Success Criteria - Structured by Priority

**MUST Deliverables (4 total - Non-negotiable):**
- [ ] Data quality assessment complete (outliers, missing values, validation)
- [ ] Core temporal features created (date components, basic aggregations)
- [ ] Primary visualizations generated (time series, distributions, correlations)
- [ ] Clean dataset exported for next phase

**SHOULD Deliverables (6 total - Complete if on schedule):**
- [ ] Store-level analysis (performance comparison, clustering)
- [ ] Product dynamics analysis (fast/slow movers, Pareto)
- [ ] External factor investigation (holidays, promotions)
- [ ] Advanced visualizations (heatmaps, interaction plots)
- [ ] Preliminary feature importance analysis
- [ ] Comprehensive decision log with rationale

**COULD Deliverables (3 total - Only if ahead):**
- [ ] Three-method outlier detection (IQR + Z-score + Isolation Forest)
- [ ] Transaction pattern analysis (basket size, traffic)
- [ ] Perishable waste risk modeling

**Contingency Rules:**
- If on schedule after Day 2 â†’ Full scope (13 deliverables)
- If 10-20% behind after Day 2 â†’ MUST + SHOULD only (10 deliverables)
- If >20% behind after Day 2 â†’ MUST only (4 deliverables), document deferred
```

---

### Template 10: End-of-Day Checkpoint Questions

**Purpose:** Quality gates to prevent compounding errors and ensure readiness for next day.

**When to use:** Embed 3-5 critical questions at the end of each day's deliverables section.

**Categories of checkpoint questions:**

**1. Technical Validation Questions:**
- Is [technical requirement] correctly implemented?
- Did validation confirm [expected behavior]?
- Are [metrics] within expected ranges?
- Should we adjust [approach] based on findings?

**2. Quality Assessment Questions:**
- Does output meet [quality standard]?
- Are visualizations clear and interpretable?
- Is documentation complete and accurate?
- Are there any silent errors or edge cases?

**3. Scope Management Questions:**
- Did we complete all planned parts within [X]h budget?
- Should we add/remove analyses for next day?
- Are findings interesting enough to warrant deeper exploration?
- Do we need to adjust next day's scope?

**4. Readiness Questions:**
- Are prerequisites met for next day's work?
- Is intermediate dataset saved and validated?
- Are blockers documented and addressed?
- Do we have clarity on tomorrow's objectives?

**Format (embed at end of each day's section):**
```markdown
#### **End-of-Day X Checkpoint** âš ï¸

**Critical Review Questions:**
1. [Technical validation question]?
2. [Quality assessment question]?
3. [Scope management question]?
4. [Readiness question]?
5. [Budget/schedule question]?

**Adjustment Options:**
- If ahead of schedule â†’ [Expansion option]
- If behind schedule â†’ [Reduction option]
- If [condition] found â†’ [Mitigation action]

**Use Daily Checkpoint Template (Section [X]) to document decisions.**
```

**Example:**
```markdown
#### **End-of-Day 2 Checkpoint** âš ï¸

**Critical Review Questions:**
1. Are rolling windows (7/14/30 days) smoothing noise as expected?
2. Did min_periods=1 reduce NaN to <1% as planned?
3. Are high-volatility items identifiable for further analysis?
4. Should we add rolling max/min features tomorrow (optional)?
5. Are we on track for external data integration (Day 3)?

**Adjustment Options:**
- If ahead of schedule â†’ Add rolling max/min features on Day 3
- If behind schedule â†’ Reduce Day 3 scope to core features only
- If smoothing insufficient â†’ Revisit window sizes on Day 3

**Use Daily Checkpoint Template (Section 11) to document decisions.**
```

---

### Template 11: Q&A Preparation Document

**Purpose:** Prepare for presentation questions and reinforce understanding of work

**When to Create:** After each major sprint (especially Sprint 1, Sprint 3)

**Filename:** `Sprint[N]_QA_Presentation_Prep.md`

**Location:** `docs/`

**Structure:**

```markdown
# Sprint [N] Q&A - Presentation Preparation

**Project:** [Name]
**Scope:** [Sprint objectives]
**Total Questions:** ~35 (7 per major notebook/section)

## Table of Contents
1. [Topic 1 - Notebook/Analysis Area]
2. [Topic 2 - Notebook/Analysis Area]
...

---

## Topic 1 - [Notebook/Analysis Name]

### Q1: [Technical question about methodology]

**Technical Answer:**
[Detailed explanation with metrics, algorithms, statistical reasoning]

**Business Answer:**
[Stakeholder-friendly explanation focusing on outcomes and decisions]

**Key Insight:**
[One sentence takeaway that captures essence]

---

### Q2: [Business question about findings]

**Technical Answer:**
[Statistical details, correlation coefficients, test results]

**Business Answer:**
[Action-oriented response with ROI implications]

**Key Insight:**
[Memorable sound bite for presentations]
```

**Question Distribution Guidelines:**

**Sprint 1 (Exploration):**
- 40% Technical (data quality, methodology choices, statistical tests)
- 40% Business (insights, patterns discovered, implications)
- 20% Contextual (scope decisions, limitations, alternatives considered)

**Sprint 3 (Modeling):**
- 40% Technical (algorithms, hyperparameters, validation approach)
- 30% Business (performance metrics, deployment readiness)
- 30% Comparison (why Model A vs Model B, tradeoffs)

**Question Types to Cover:**

1. **Methodology Questions:**
   - "Why did you use [method X] instead of [method Y]?"
   - "How did you handle [specific challenge]?"
   - "What assumptions did you make?"

2. **Results Questions:**
   - "What was your most important finding?"
   - "What surprised you in the data?"
   - "How confident are you in these results?"

3. **Decision Questions:**
   - "Why did you choose [Option A] over [Option B]?"
   - "What alternatives did you consider?"
   - "How would you approach this differently next time?"

4. **Business Questions:**
   - "What should we do with these insights?"
   - "How much improvement can we expect?"
   - "What are the limitations we should know?"

**Benefits:**
- Forces deep understanding (teaching effect - if you can't explain it, you don't understand it)
- Identifies knowledge gaps early (before presentation)
- Builds presentation confidence (practiced responses)
- Creates reference material for final report
- Demonstrates systematic thinking to stakeholders

---

### Template 12: Scope Limitations Log

**Purpose:** Transparently document what is OUT of scope and why

**When to Create:** Sprint 1 (after scope finalized)

**When to Update:** Whenever scope boundary discovered or confirmed

**Filename:** `scope_limitations.md`

**Location:** `docs/`

**Template:**

```markdown
# Scope Limitations - [Project Name]

**Project:** [Name]
**Last Updated:** [Date]
**Version:** [X]

---

## In Scope

**Included in this analysis:**
- [What IS covered - be specific]
- [What IS covered - include metrics if relevant]
- [What IS covered - reference decisions if applicable]

**Example:**
- OK: Guayas region (11 stores, 73.8% in Guayaquil)
- OK: Top-3 product families: GROCERY I, BEVERAGES, CLEANING (59% of catalog)
- OK: Non-perishable items only (2,296 items, 0% perishable)
- OK: Daily sales forecasting (March 2014 test period)
- OK: 300K sample for development, full dataset for validation

---

## Out of Scope

**Excluded from this analysis:**
- [What is NOT covered] - **Reason:** [Why excluded - resource/time/data/priority]
- [What is NOT covered] - **Reason:** [Why excluded]

**Example:**
- ERROR: Perishable categories (PRODUCE, DAIRY, MEATS, BREAD/BAKERY)
  - **Reason:** Top-3 families contain 0% perishables (per DEC-010). Perishables require different forecasting approach (daily vs weekly), shorter forecast horizons, higher accuracy requirements. Out of scope for 4-sprint timeline.

- ERROR: Regions outside Guayas (43 stores in other provinces)
  - **Reason:** Guayas provides sufficient variety (11 stores, mixed types) for methodology validation. Other regions may have different climate, demographics, product mix. Expanding to national scope would triple data volume and complexity, exceeding 4-sprint timeline.

---

## Discovered Limitations

**Limitations identified during analysis:**

| Item | Discovered When | Impact | Mitigation | Status |
|------|-----------------|--------|------------|--------|
| [Limitation] | [Sprint X, Day Y] | [Effect on project] | [How we addressed it] | [Accepted/Workaround/Future] |

**Example:**
| Item | Discovered When | Impact | Mitigation | Status |
|------|-----------------|--------|------------|--------|
| Perishables 0% in sample | Sprint 1, Day 5 | Cannot forecast PRODUCE, DAIRY | Document limitation, note for Phase 2 | Accepted |
| 16% missing promotions (2013-2014) | Sprint 1, Day 3 | Cannot distinguish no-promo vs not-tracked | Fill with 0 (conservative assumption per DEC-003) | Workaround |

---

## Future Scope Expansion

**Potential additions for Phase 2 or future work:**

1. **[Potential addition]**
   - **Effort estimate:** [Hours/sprints]
   - **Value proposition:** [Business benefit]
   - **Prerequisites:** [What needs to happen first]
   - **Priority:** High / Medium / Low
```

**Benefits:**
- Prevents stakeholder surprise ("why didn't you do X?")
- Documents justification for scope decisions
- Creates roadmap for future phases
- Demonstrates project management discipline
- Protects against scope creep

---

### Enhanced Risk Management for Version 2.0 Plans

**Additional risks to consider when using v2.0 framework:**

| Risk                                             | Likelihood | Impact | Mitigation                                                |
| ------------------------------------------------ | ---------- | ------ | --------------------------------------------------------- |
| **Scope creep during exploration**               | Medium     | Medium | Daily checkpoints maintain MUST/SHOULD/COULD discipline   |
| **Daily checkpoint overhead exceeds 15 min**     | Low        | Low    | Template streamlines process, set timer                   |
| **Interesting findings trigger scope expansion** | Medium     | Medium | Defer deep dives to future phases, document for later     |
| **False precision in daily tracking**            | Low        | Low    | Focus on trends (ahead/on/behind), not exact minutes      |
| **Checkpoint fatigue in long phases**            | Low        | Medium | Reduce frequency after Sprint 1, maintain at key milestones |

---

### Communication Plan Enhancement for Version 2.0

**Add to existing communication plan:**

```markdown
### Daily Checkpoints ([Phase Name])
- **Timing:** End of each day (last 15 minutes)
- **Format:** Structured review using checkpoint template (Section [X])
- **Content:**
  - Time tracking (actual vs allocated)
  - Scope completion (all parts done?)
  - Quality assessment (outputs validated?)
  - Findings (unexpected discoveries?)
  - Adjustment decisions (add/remove tasks for next day?)
- **Output:** Daily checkpoint document (Day[X]_Checkpoint_[Phase].md)
- **Cumulative tracking:** Update buffer table after each checkpoint
- **Purpose:** Enable agile adaptation, prevent scope creep, maintain buffer discipline
```

---

### Decision Tree: Should You Use Version 2.0 Planning?

**Use Version 1.0 (Standard) if:**
- âœ“ Experienced with this type of work (know what to expect)
- âœ“ High confidence in estimates (Â±10% accuracy)
- âœ“ Limited documentation time (<5% of phase duration)
- âœ“ Straightforward scope with minimal uncertainty
- âœ“ Short phase duration (1-2 days)

**Use Version 2.0 (Enhanced) if:**
- âœ“ First time doing this type of work (uncertain estimates)
- âœ“ Low confidence in estimates (Â±20%+ uncertainty)
- âœ“ Substantial buffer worth protecting (>20% or carryover)
- âœ“ Complex scope prone to drift or creep
- âœ“ Multi-day phase where early detection matters (3-5+ days)
- âœ“ High value of systematic reflection and adjustment
- âœ“ Learning objective (want to improve estimation over time)

**Cost-Benefit Analysis:**
- **Cost:** 15 min/day Ã— [N] days = [X] hours overhead
- **Benefit:** Protect [Y] hours of buffer, enable [Z] adjustments
- **ROI:** If overhead <5% of phase duration and buffer >15%, use v2.0

---

### Version 2.0 Best Practices

**1. Commit to the discipline:**
- Set aside exactly 15 minutes at end of each day
- Use a timer to prevent checkpoint bloat
- Complete checkpoint before closing for the day

**2. Be honest in assessments:**
- Variance explanations are for learning, not blame
- Document real blockers, not excuses
- Adjust scope proactively when behind

**3. Focus on trends, not precision:**
- "Ahead/On/Behind" is sufficient granularity
- Don't obsess over exact minutes
- Buffer health (Healthy/Caution/Critical) guides decisions

**4. Use checkpoints for agility:**
- Scope adjustments are normal and expected
- MUST/SHOULD/COULD framework enables clean cuts
- Deferred work is documented, not abandoned

**5. Carry learnings forward:**
- Checkpoint notes inform next phase planning
- Variance patterns improve future estimates
- Adjustment decisions build project wisdom

**6. Know when to stop:**
- If phase consistently on schedule, reduce checkpoint frequency
- If estimates become accurate (Â±5%), revert to v1.0
- If checkpoint takes >20 min, simplify template

---

### Integration with Existing Templates

**Where to add Version 2.0 elements in project plans:**

**Section 3 (Timeline):**
- Add cumulative buffer tracking table (Template 8)

**Section 4 (Deliverables):**
- Add end-of-day checkpoint questions after each day (Template 10)

**Section 6 (Success Criteria):**
- Restructure using MUST/SHOULD/COULD framework (Template 9)

**Section 8 (Risk Management):**
- Add scope creep, checkpoint overhead, and exploration drift risks

**Section 9 (Expected Outcomes):**
- Replace 2-stage table with 3-stage progressive table (Template 7)

**Section 10 (Communication Plan):**
- Add "Daily Checkpoints" subsection with template reference

**New Section 11:**
- Add complete Daily Checkpoint Template (Template 6)

---

**End of Version 2.0 Planning Framework**

**Summary:** Version 2.0 planning adds structured daily discipline through 15-minute checkpoints, progressive tracking, and priority tiers to enable agile adaptation and protect buffer health in complex, multi-day phases with uncertain scope.

**When in doubt:** Use v2.0 for critical phases and first-time work; revert to v1.0 once confidence and accuracy are established.
---

## Recommended Style and Structure

| Section               | Format                                                 | Description                                                                       |
| --------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **Headers**           | Use H2/H3 hierarchy (`##`, `###`)                      | Maintain consistent hierarchy and clarity                                         |
| **Tables**            | Markdown tables for timelines and deliverables         | Use columns for *Day/Sprint*, *Focus Area*, and *Deliverables*                    |
| **Bullets**           | Concise, action-oriented                               | Begin each bullet with an actionable verb (e.g., *Define*, *Compute*, *Validate*) |
| **Metrics & Outputs** | Use bold formatting for key metrics and filenames      | e.g., **user_features.csv**, **RFM score**, **accuracy â‰¥ 0.85**                   |
| **Separation**        | Use `---` for visual separation between major sections | Enhances readability and consistency                                              |

---

## Tone and Style

All documentation, project plans, and notebooks should adhere to a **professional, concise, and objective tone**.  

**Requirements:**
- **Professional language only.** Avoid informal expressions and personal opinions.  
- **No emojis or decorative symbols** in any document or notebook.  
- **Each section** of a markdown or project plan must include a **short, informative description** summarizing its content and intent.  
- **Each Jupyter Notebook cell** must:
  - Contain a short markdown description explaining what the cell does.  
  - Generate **at least one visible output** (table, plot, metric, or print statement) to demonstrate results or intermediate checks.  
- **Formatting consistency** should be prioritized â€” all text, tables, and figures must be clear, aligned, and free of unnecessary embellishments.  
- **Comments in code** should be brief, meaningful, and written in complete sentences where relevant.

This section ensures the deliverables communicate technical rigor and are accessible to both technical and non-technical stakeholders.

### Character and Symbol Restrictions

To ensure compatibility across all systems and maintain professional standards:

**Prohibited:**
- Emojis of any kind (no âœ… âŒ âš ï¸ ðŸ“Š ðŸ” etc.)
- Unicode checkmarks or symbols (no âœ“ âœ—)
- Special decorative characters

**Required:**
- Standard markdown checkboxes: `[ ]` for incomplete, `[x]` for complete
- Plain text status prefixes: "OK:", "WARNING:", "ERROR:"
- ASCII-only characters in all documentation

**Applies to:**
- Project plans and reports
- Notebook markdown cells
- README files
- All markdown documentation
---

## Example Project Flow

| Sprint      | Focus Area                 | Key Outputs                                               |
| ----------- | -------------------------- | --------------------------------------------------------- |
| **Day 0**   | Environment Setup          | Virtual environment, base packages, VS Code configuration |
| **Sprint 1**| Data collection & cleaning | Validated datasets ready for analysis                     |
| **Sprint 2**| Feature engineering        | Analytical base and feature dictionary                    |
| **Sprint 3**| Modeling & validation      | Trained models, evaluation reports                        |
| **Sprint 4**| Deployment & reporting     | Production pipeline, stakeholder presentation             |

---

## Best Practices

- **Environment Setup:** Complete environment configuration (Day 0) before beginning analysis work. Generate domain-specific package scripts based on project documentation. See Methodology Section 2.1 (Phase 0: Environment Setup) for automated setup procedures.
- **Modularization:** Structure notebooks by phase (e.g., `01_data_cleaning.ipynb`, `02_feature_engineering.ipynb`).
- **Reproducibility:** Store parameters, transformations, and random seeds.
- **Transparency:** Keep assumptions and exclusions explicit.
- **Version Control:** Commit all code and documents to Git with descriptive messages.
- **Documentation:** Maintain a centralized README linking datasets, notebooks, and reports.
- **Validation:** Integrate both statistical and business validation for each phase.
- **Communication:** Provide concise daily or sprint summaries of progress and blockers.

---
## File Naming Standards

**Notebooks:**
- Working development: `sYY_dXX_PHASE_description.ipynb` (e.g., `s01_d01_EDA_data_quality.ipynb`)
- Final deliverables: `XX_PHASE_description.ipynb` (e.g., `01_EDA_data_quality_cohort.ipynb`)
- Consolidation occurs in Phase 4 (Sprint 4)

See Collaboration Methodology for complete naming conventions.
---

## Template Reference

**Filename Convention:**
`<ProjectName>_ProjectPlan_<Phase>.md`
Example: `CustomerChurn_ProjectPlan_Sprint1.md`

**Author Section:**
```
**Prepared by:** [Your Name]
**Timeline:** [Sprint/Phase/Duration]
**Next Phase:** [Next Planned Stage]
```
