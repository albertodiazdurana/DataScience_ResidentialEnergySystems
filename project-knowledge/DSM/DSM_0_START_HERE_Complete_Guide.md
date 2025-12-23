# Data Science with Claude - Complete Getting Started Guide
**Your complete guide to setting up and executing data science projects with Claude**

**Version:** 1.1.1  
**Last Updated:** 2025-11-19

---

## Quick Start (5 Minutes)

**New to this system? Start here:**

1. **Read this document** (5 minutes) - Understand how everything connects
2. **Run environment setup** (10 minutes) - Install required packages
3. **Create Claude Project** - Set up your workspace
4. **Upload to Project Knowledge** - Add methodology documents
5. **Write Custom Instructions** - Configure for your project

**Then:** Start your first chat following the patterns in Section 5.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Document Map](#2-document-map)
3. [File Inventory](#3-file-inventory)
4. [Hybrid Setup Guide](#4-hybrid-setup-guide)
5. [New Project Checklist](#5-new-project-checklist)
6. [Common Patterns](#6-common-patterns)
7. [Tips for Success](#7-tips-for-success)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. System Overview

### Four Core Documents, Four Purposes

This methodology system consists of four complementary documents that work together:

#### 1.1. Project Reference Documentation
**File:** `ProjectReference_Documentation.md` (you create per project)  
**Purpose:** Project-specific context and references

**Contains:**
- Business context and stakeholder profiles
- Data sources and schema documentation
- Domain-specific terminology and glossary
- Technical environment specifications
- Key assumptions and design decisions

**Use when:** Describing project domain, context, or technical specifications

#### 1.2. Collaboration Methodology (Execution Framework)
**Files:** Main document + consolidated appendices (v1.1.1)
- `1.0_Data_Science_Collaboration_Methodology_v1.1.md` (~3,000 lines)
- `1.0_Methodology_Appendices.md` (~3,565 lines) - Contains all 5 appendices:
  - Appendix A: Environment Setup Details
  - Appendix B: Phase Deep Dives
  - Appendix C: Advanced Practices Detailed
  - Appendix D: Domain Adaptations
  - Appendix E: Quick Reference + File Naming Standards

**Purpose:** Framework for HOW to execute work with Claude

**Core Content:**
- 4-phase workflow (Exploration → Features → Analysis → Communication)
- Notebook standards (~400 lines, 5-6 sections)
- Decision Log Framework
- Pivot Criteria & Failure Modes
- Stakeholder Communication Cadence
- Text conventions (WARNING/OK/ERROR)
- Advanced practices (10 optional complexity practices)

**Use when:** Executing work (building notebooks, making decisions, running analysis)

#### 1.3. Project Management Guidelines (Planning Framework)
**File:** `2_0_ProjectManagement_Guidelines_v2_v1.1.md` (core - always use)  
**Optional Extension:** `2.1_PM_ProdGuidelines_extension.md` (for production projects)

**Purpose:** Templates and standards for WRITING project plans

**Core Content:**
- 7 required sections (Purpose, Inputs, Timeline, Deliverables, Success Criteria)
- 5 base plan structure templates
- Optional: 5 v2.0 enhancement templates (daily checkpoints, progressive tracking)
- Governance, risk management, QA standards (in Production Extension)

**Use when:** 
- Writing sprint/daily project plans (all projects)
- Planning complex multi-day phases
- First-time execution of uncertain work

#### 1.4. Implementation Guide (System Setup)
**File:** `3_Methodology_Implementation_Guide_v1.1.md`

**Purpose:** Instructions for SETTING UP new projects

**Contains:**
- Where to put each document (Project Knowledge vs Custom Instructions)
- Custom Instructions template
- Quick start checklist
- Examples for different domains (Time Series, NLP)

**Use when:** Starting new project, configuring Project Knowledge and Custom Instructions

### Document Relationship Map

```
Project Start
    ↓
[Custom Instructions Template] ← refer to this FIRST
    ↓
    ├──> Upload to Project Knowledge:
    │   ├─ Project Reference Documentation
    │   ├─ Collaboration Methodology (main + consolidated appendices)
    │   ├─ Methodology Implementation Guide
    │   ├─ PM Guidelines v2 (core - always use)
    │   └─ PM Production Extension (add for enterprise projects)
    │
    └──> Write Custom Instructions:
        ├─ Add to "Instructions to tailor Claude's responses"
        └─ Project-specific context (timeline, stakeholders, domain)
    ↓
Sprint 1 Day 1: Create Project Plan
    ↓
[PM Guidelines] ← Reference for STRUCTURE
    ↓
    Create: ProjectName_Sprint1_Plan.md
    ↓
Sprint 1-4: Execute Work
    ↓
[Collaboration Methodology] ← Reference for EXECUTION
    ↓
    - Follow 4-phase workflow
    - Use notebook standards
    - Log decisions
    - Apply quality checks
    ↓
Project Complete
```

---

## 1.5. Project Timeline Configuration

### Flexible Sprint-Based Structure

This methodology uses a **4-sprint framework** where each sprint represents one of the four core phases:
- Sprint 1: Exploration & Understanding
- Sprint 2: Feature Development
- Sprint 3: Analysis & Modeling
- Sprint 4: Communication & Delivery

**Sprint Duration is Configurable** based on project complexity and timeline.

### Determining Sprint Length

**Key Question:** How much time does this project require?

**Sprint Length Guidelines:**

| Project Type      | Total Duration | Sprint Length    | Example Split         |
| ----------------- | -------------- | ---------------- | --------------------- |
| Quick Analysis    | 4-8 days       | 1-2 days/sprint  | 2-2-2-2 days          |
| Academic Project  | 4-6 weeks      | 1 week/sprint    | 1-1-1-1 weeks         |
| Standard Analysis | 6-8 weeks      | 1.5 weeks/sprint | 1.5-1.5-1.5-1.5 weeks |
| Complex Research  | 8-16 weeks     | 2-4 weeks/sprint | 2-3-3-2 weeks         |
| Production ML     | 12-24 weeks    | 3-6 weeks/sprint | 3-4-6-3 weeks         |

**Note:** Sprints need NOT be equal duration. Adjust based on phase complexity.

### Sprint Configuration Template

**At Project Start, Document:**

```markdown
# Project Timeline Configuration

**Total Project Duration:** [X weeks/months]

**Sprint Allocation:**
- Sprint 1 (Exploration): [X days/weeks] (allocated: [Y hours])
- Sprint 2 (Features): [X days/weeks] (allocated: [Y hours])
- Sprint 3 (Modeling): [X days/weeks] (allocated: [Y hours])
- Sprint 4 (Communication): [X days/weeks] (allocated: [Y hours])

**Rationale for Sprint Lengths:**
- Sprint 1: [Why this duration]
- Sprint 2: [Why this duration]
- Sprint 3: [Why this duration]
- Sprint 4: [Why this duration]

**Working Hours per Day:** [X hours of focused work]
**Working Days per Week:** [X days] (typically 5, but flexible)
```

### Configuration Examples

**Example 1: Quick Analysis (1 week total)**
```
Sprint 1 (EDA): 1 day (6 hours)
Sprint 2 (Features): 2 days (12 hours)
Sprint 3 (Modeling): 1 day (6 hours)
Sprint 4 (Reporting): 1 day (6 hours)
Total: 5 days, 30 hours
```

**Example 2: Academic Project (4 weeks total)**
```
Sprint 1 (EDA): 1 week (20 hours)
Sprint 2 (Features): 1 week (20 hours)
Sprint 3 (Modeling): 1 week (20 hours)
Sprint 4 (Presentation): 1 week (15 hours)
Total: 4 weeks, 75 hours
```

**Example 3: Production ML (16 weeks total)**
```
Sprint 1 (EDA): 3 weeks (60 hours)
Sprint 2 (Features): 4 weeks (80 hours)
Sprint 3 (Modeling): 6 weeks (120 hours)
Sprint 4 (Deployment): 3 weeks (60 hours)
Total: 16 weeks, 320 hours
```

### Best Practices

**DO:**
- Configure sprint lengths at project start
- Document in project plan
- Adjust if scope changes (record in decision log)
- Use "Sprint X" terminology in all documentation

**DON'T:**
- Assume all sprints must be equal length
- Default to "1 week" without considering project scope
- Change sprint configuration mid-project without justification
- Use "Week X" terminology (use "Sprint X" instead)

### Quick Reference

**Terminology:**
- "Week 1" → "Sprint 1"
- "Week 2 Plan" → "Sprint 2 Plan"
- "Weekly review" → "Sprint review"
- "4-week project" → "4-sprint project (duration: X weeks)"

**File Naming:**
- `Week1_Plan.md` → `Sprint1_Plan.md`
- `w01_d01_notebook.ipynb` → `s01_d01_notebook.ipynb`
- `Week1_to_Week2_Handoff.md` → `Sprint1_to_Sprint2_Handoff.md`

---

## 2. Document Map

### Priority 0: Getting Started Documents

#### This Document: Complete Getting Started Guide
**File:** `DSM_0_START_HERE_Complete_Guide.md`  
**Purpose:** Master map - HOW everything connects  
**Read:** First, before using any other document  

**Contains:**
- Quick start (5 minutes)
- System overview with document relationships
- Complete file inventory
- Hybrid setup step-by-step
- New project checklist with patterns
- Troubleshooting guide

---

### Priority 1: Collaboration Methodology v1.1.0 (Execution Framework)

#### Main Document: Data Science Collaboration Methodology
**File:** `DSM_1.0_Data_Science_Collaboration_Methodology_v1.1.md` (~3,000 lines)
**Purpose:** Core execution workflow - HOW to work with Claude

**Structure:**
- Section 1: Introduction & Philosophy
- Section 2: The Four-Phase Workflow
  - 2.1 Phase 0: Environment Setup
  - 2.2 Phase 1: Exploration
  - 2.3 Phase 2: Feature Engineering
  - 2.4 Phase 3: Analysis
  - 2.5 Phase 4: Communication & Deliverables
- Section 3: Communication & Working Style
- Section 4: Project Management Integration
- Section 5: Advanced Complexity Practices (10 optional practices)
- Section 6: Tools & Best Practices
- Section 7: Domain-Specific Considerations
- Section 8: Success Patterns & Anti-Patterns

**Tier 1 Practices (integrated into core workflow):**
- Decision Log Framework
- Pivot Criteria & Failure Modes
- Stakeholder Communication Cadence

**Advanced Practices (optional, activate as needed):**
- Experiment Tracking, Hypothesis Management
- Performance Baseline & Benchmarking
- Ethics & Bias Considerations
- Testing Strategy, Data Versioning & Lineage
- Technical Debt Register, Scalability Considerations
- Literature Review Phase, Risk Management

#### Appendix A: Environment Setup Details
**File:** `DSM_1.0_Methodology_Appendices.md` (Section A)
**Purpose:** Detailed package specifications and troubleshooting

**Contains:**
- Complete package versions and dependencies
- Setup script explanations (minimal vs. production)
- VS Code configuration details
- Common installation issues and solutions
- Environment validation procedures
- Domain-specific package extensions

#### Appendix B: Phase Deep Dives
**File:** `DSM_1.0_Methodology_Appendices.md` (Section B)
**Purpose:** Detailed guidance for each phase with examples

**Contains:**
- Phase 1 (Exploration): Data quality, profiling patterns, validation
- Phase 2 (Feature Engineering): Aggregations, transformations, encoding
- Phase 3 (Analysis): Model selection, validation, interpretation
- Phase 4 (Communication): Presentations, reports, documentation
- Real examples from TravelTide project
- Code templates and patterns

#### Appendix C: Advanced Practices Detailed
**File:** `DSM_1.0_Methodology_Appendices.md` (Section C)
**Purpose:** Implementation details for all 10 advanced practices

**Contains:**
- Complete implementation guides for each practice
- Templates and frameworks
- Integration patterns with core workflow
- When to activate each practice
- Example implementations
- Tool recommendations

#### Appendix D: Domain Adaptations
**File:** `DSM_1.0_Methodology_Appendices.md` (Section D)
**Purpose:** Domain-specific guidance and considerations

**Contains:**
- Time Series Forecasting (ARIMA, Prophet, seasonal patterns)
- NLP & Text Analysis (preprocessing, embeddings, transformers)
- Computer Vision (image preprocessing, CNNs, transfer learning)
- Clustering & Segmentation (K-means, hierarchical, DBSCAN)
- Recommendation Systems
- Anomaly Detection

#### Appendix E: Quick Reference
**File:** `DSM_1.0_Methodology_Appendices.md` (Section E)
**Purpose:** Checklists, commands, and quick lookup

**Contains:**
- Phase transition checklists
- Common bash/Python commands
- Git workflow patterns
- Quality check lists
- Notebook structure template
- Decision log template
- Communication templates

---

### Priority 2: Project Management Guidelines (Planning Framework)

#### Core: PM Guidelines v2
**File:** `DSM_2_0_ProjectManagement_Guidelines_v2_v1.1.md` (~1,220 lines)
**Purpose:** Core project plan structure for ALL data science projects

**Core Content:**
- 7 required sections (Purpose, Inputs, Timeline, Deliverables, Readiness, Success Criteria, Documentation)
- **5 Base Plan Structure Templates:**
  1. Daily Task Breakdown Format
  2. Phase Summary Format
  3. Expected Outcomes Table Format
  4. Phase Prerequisites Format
  5. Time Buffer Allocation Guidance
- **Optional: 5 v2.0 Enhancement Templates** (add when needed):
  6. Daily Checkpoint Framework
  7. Progressive Expected Outcomes Table
  8. Cumulative Buffer Tracking Table
  9. MUST/SHOULD/COULD Priority Framework
  10. End-of-Day Checkpoint Questions

**Versions:**
- **v1.0 (Standard):** Templates 1-5 only, straightforward planning
- **v2.0 (Enhanced):** Templates 1-10, includes daily checkpoints and progressive tracking

**Use when:**
- Writing sprint/daily project plans (all projects)
- Planning complex multi-day phases
- First-time execution of uncertain work

#### Optional Extension: PM Production Guidelines
**File:** `DSM_2.1_PM_ProdGuidelines_extension.md` (260 lines + TOC)  
**Purpose:** Production-specific additions for enterprise projects

**Extends:** `DSM_2.0_ProjectManagement_Guidelines_v2.md`

**Production-Only Content:**
- Project Governance & Roles (RACI matrix)
- Data Management & Versioning (audit trails, compliance)
- Quality Assurance & Peer Review (formal QA checklist)
- Risk Management framework (risk register, prioritization)
- Communication & Reporting Standards (stakeholder matrix, reports)
- Post-Project Review process (retrospective template, archival)

**Use when:**
- Enterprise/production projects with formal governance
- Multi-person teams requiring role clarity
- Regulatory compliance (GDPR, SOX, etc.)
- Formal QA and peer review processes

**How to use together:**
1. Use Guidelines_v2 for core planning structure
2. Add Extension sections for production requirements
3. Reference Extension templates (RACI, QA, Risk) as needed

---

### Priority 3: Implementation & Setup

#### Implementation Guide
**File:** `DSM_3_Methodology_Implementation_Guide_v1.1.md` (~500 lines)
**Purpose:** Setup instructions with complete examples

**Core Content:**
- Hybrid approach explanation (Project Knowledge + Custom Instructions)
- **Consolidated Custom Instructions Template**
- 2 Complete domain examples:
  - Time Series Forecasting
  - NLP Sentiment Analysis
- Tips for success
- Setup patterns

**Use when:** Starting new project, writing Custom Instructions

---

## 3. File Inventory

### Complete Repository Structure

#### Essential Repository Files
```
├── LICENSE                    # MIT License
├── _gitignore                 # Git ignore patterns
├── CONTRIBUTING.md            # Contribution guidelines
├── CODE_OF_CONDUCT.md         # Community standards
├── CHANGELOG.md               # Version history
├── SECURITY.md                # Security policies
└── README.md                  # Repository overview
```

#### Getting Started (Priority 0)
```
└── 0_START_HERE_Complete_Guide.md        # This document (merged from 3 files)
```

#### Methodology System v1.1.3 (Priority 1)
```
├── 1.0_Data_Science_Collaboration_Methodology_v1.1.md  # Main (~3,130 lines)
└── 1.0_Methodology_Appendices.md                       # All appendices (~3,920 lines)
    ├── Appendix A: Environment Setup Details
    ├── Appendix B: Phase Deep Dives
    ├── Appendix C: Advanced Practices Detailed
    ├── Appendix D: Domain Adaptations
    └── Appendix E: Quick Reference + File Naming Standards
```

#### Project Management (Priority 2)
```
├── 2_0_ProjectManagement_Guidelines_v2_v1.1.md    # Core planning framework
└── 2.1_PM_ProdGuidelines_extension.md             # Optional production extension
```

#### Implementation (Priority 3)
```
└── 3_Methodology_Implementation_Guide_v1.1.md     # Setup & Custom Instructions template
```

#### Quick Reference Cards (Priority 4)
```
└── 1.4_File_Naming_Quick_Reference.md             # Printable file naming card
```

#### Custom Instructions
```
└── IMPROVED_Custom_Instructions_v1.1.md           # Example Custom Instructions
```

#### Environment Setup Scripts
```
├── setup_base_environment_minimal.py    # Academic/exploratory (essential packages only)
└── setup_base_environment_prod.py       # Production (includes code quality tools)
```

#### Case Studies (Optional)
```
└── case-studies/
    └── traveltide/                      # TravelTide Customer Segmentation project
        ├── context/                     # Project background & stakeholders
        ├── methodology_application/     # How methodology was applied
        ├── decisions/                   # Key decision documentation
        └── lessons_learned/             # Retrospective & insights
```

### Total System Size

| Component             | Files  | Lines      | Purpose                  |
| --------------------- | ------ | ---------- | ------------------------ |
| Getting Started       | 1      | ~1,000     | Quick start & system map |
| Methodology v1.1.1    | 2      | 5,252      | Execution framework      |
| PM Guidelines         | 2      | ~750       | Planning framework       |
| Implementation        | 1      | 450        | Setup instructions       |
| Quick Reference Cards | 1      | 118        | Printable file naming    |
| Custom Instructions   | 1      | 350        | Example configuration    |
| Environment Scripts   | 2      | ~400       | Automated setup          |
| **Total Core System** | **10** | **~8,320** | **Complete framework**   |

---

## 4. Hybrid Setup Guide

### Step 1: Run Environment Setup

**Choose based on project type:**

```bash
# Academic/Exploratory work (RECOMMENDED for most projects):
python setup_base_environment_minimal.py

# Production/Team projects (includes code quality tools):
python setup_base_environment_prod.py

# Install VS Code extensions (both setups):
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter

# Select interpreter: Ctrl+Shift+P → Python: Select Interpreter → .venv
```

**What gets installed:**

**Minimal (Academic):**
- Core: pandas, numpy, matplotlib, seaborn
- ML: scikit-learn
- Notebooks: jupyter, ipykernel
- Stats: scipy, statsmodels

**Production (adds):**
- Code quality: black, flake8, autopep8
- Testing: pytest
- Type checking: mypy
- Documentation: sphinx

### Step 2: Create Claude Project

```
Project Name: [Descriptive name]
Purpose: [One sentence]
Initial Instructions: "Confirm that you understand what I need. 
Be concise in your work. Do not generate any artifacts before 
you provide a very short description and you have received my approval."
```

### Step 3: Upload to Project Knowledge

**Add these files to Project Knowledge:**

```
Required:
├─ 0_START_HERE_Complete_Guide.md
├─ 1.0_Data_Science_Collaboration_Methodology_v1.1.md
├─ 1.0_Methodology_Appendices.md
├─ 2_0_ProjectManagement_Guidelines_v2_v1.1.md
└─ 3_Methodology_Implementation_Guide_v1.1.md

Optional (for production):
└─ 2.1_PM_ProdGuidelines_extension.md

Project-specific:
└─ ProjectReference_Documentation.md (you create)
```

**Why upload to Project Knowledge:**
- Searchable when needed
- Available across all project chats
- No token/character limits
- Update once, applies everywhere

### Step 4: Write Custom Instructions

**Template location:** See `DSM_3_Methodology_Implementation_Guide_v1.1.md` for complete template

**Key sections to include:**

```markdown
# Project: [Name]
Domain: [Type]

## Document References
This project uses:
- **PM Guidelines** (Project Knowledge): Project planning structure
- **Collaboration Methodology v1.1.0** (Project Knowledge): Execution workflow
- **Project Reference Documentation** (Project Knowledge): Domain context

## Project Planning Context
- Scope, Resources, Success Criteria
- Data & Dependencies
- Stakeholders & Governance

## Execution Context
- Timeline & Phases
- Deliverables
- Domain Adaptations
- Advanced Practices (checkboxes)

## Communication & Style
- Artifact Generation preferences
- Environment Setup status
- Standards (no emojis, WARNING/OK/ERROR)
- Session Management (token monitoring)
```

**Key addition:** Explicitly reference both methodology AND PM guidelines

### Step 5: First Chat Message

**Prompt to use:**

```
"I'm starting a new [domain] project. Please:
0. Review the DSM - Data Science Methodology (Integrated Systems Guide) in the folder Project Knowledge
1. Review the Collaboration Methodology in DSM (core + relevant appendices) in Project Knowledge
2. Read Claude's Instructions in .claude .claude/CLAUDE.md
3. Confirm understanding of our working style

[Then continue line by line:]

4. Review the Project Description and project reference documentation in Project Knowledge
5. Create concise Project Plan artifact as a markdown file
    - Review PM Guidelines in Project Knowledge
    - Create a Sprint 1 project plan following PM Guidelines structure
    - Include sections described in PM Guidelines
    - Project duration: [specify weeks/sprints, e.g., "2-week sprint" or "4 sprints of 1 week each"]
    - Number of notebooks expected: [specify, e.g., "1 notebook per sprint" or "1 notebook a day" or "3 notebooks total"]
    - File location: docs/plan/Sprint1_Plan.md
6. Create the artifact in markdown for customized project-specific Instructions in .claude/CLAUDE.md
    - Use the Custom Instructions Template in Project Knowledge
    - Tailor it to this specific project
    - Include all relevant sections
   from DSM_3_Methodology_Implementation_Guide_v1.1.md. Be concise."
```

**Output:** Claude will confirm understanding and create initial project plan

---

## 5. New Project Checklist

### Complete Setup Sequence

**Day 0: Environment & Project Setup**

```
[ ] Run setup script (minimal or production)
[ ] Install VS Code extensions
[ ] Select Python interpreter (.venv)
[ ] Create Claude Project
[ ] Upload methodology documents to Project Knowledge
[ ] Write Custom Instructions using template
[ ] Send first chat message (setup confirmation)
[ ] Generate project directory structure
[ ] Optional: Generate domain-specific extension script
```

### Project Initialization Pattern

**Two-Step Environment Setup (Section 2.1.2):**

**Step 1: Run base environment script**
```bash
python setup_base_environment_minimal.py
```
This creates `.venv`, installs core packages (pandas, numpy, matplotlib, seaborn), and generates `requirements_base.txt`.

**Step 2: Install project-specific packages**

**Prompt to Claude:**
```
"Based on my project plan, determine which domain-specific packages
I need to install. Reference Section 2.1.4 and Appendix A.3 for
package options. Then provide the pip install commands and update
requirements_project.txt so that I can run them in the command line."
```

Claude will analyze your project requirements and provide appropriate installation commands, for example:
```bash
# Activate environment first
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install recommended packages (Claude will customize based on your project)
pip install tensorflow opencv-python  # Example for CV project

# Generate project requirements file
pip freeze > requirements_project.txt
```

**Directory Structure:**

**Prompt to Claude:**
```
"Create the standard project directory structure following
the Collaboration Methodology. Generate the folder tree and
initial README files."
```

**Expected output:**
```
project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
├── notebooks/
├── docs/
│   ├── plan/
│   ├── checkpoints/      # Daily checkpoint files (sYY_dXX_checkpoint.md)
│   └── decisions/        # Decision log files (DEC-XXX_description.md)
├── models/
└── outputs/
    ├── figures/
    └── reports/
```

### Phase Kickoff Pattern

**At start of each phase:**

```
"Starting Phase [X]: [Phase name]. Review methodology for Phase [X]
best practices, then help me create [specific deliverable]."
```

**Examples:**
- "Starting Phase 1: Data Exploration. Review methodology Section 2.2..."
- "Starting Phase 2: Feature Engineering. Review Appendix B..."
- "Starting Phase 3: Clustering Analysis. Review methodology Section 2.4..."

### Domain-Specific Extensions

After base environment setup, install project-specific packages per Section 2.1.4:

| Domain              | Installation                                    |
| ------------------- | ----------------------------------------------- |
| Time Series         | `pip install statsmodels prophet`               |
| Computer Vision     | `pip install tensorflow opencv-python`          |
| NLP                 | `pip install transformers nltk spacy`           |
| Deep Learning       | `pip install tensorflow` or `pip install torch` |
| Experiment Tracking | `pip install mlflow`                            |

Generate requirements file after installation:
```bash
pip freeze > requirements_project.txt
```

For full domain package lists, see Appendix A.3.

---

## 6. Common Patterns

### Pattern 1: Daily Workflow

```
Morning:
1. Check project plan (PM Guidelines structure)
2. Review previous day's checkpoint (docs/checkpoints/sYY_dXX_checkpoint.md)
3. Identify today's deliverable
4. Reference methodology for execution approach

During Work:
5. Work in notebooks following methodology standards
6. Add Notebook Summary Cell after completing each notebook (Section 6.1.4)

End of Day (5 min):
7. Create daily checkpoint file (docs/checkpoints/sYY_dXX_checkpoint.md)
8. Update decision log if major choices made (DEC-XXX format)
9. Commit to git if applicable
10. Note tomorrow's first priority

Reference: Section 6.1.4 Daily Documentation Protocol
```

### Pattern 1b: End of Notebook

```
Before closing any notebook:

1. Verify all cells execute (Kernel > Restart & Run All)
2. Add Notebook Summary Cell as final cell:

   # ============================================================
   # NOTEBOOK SUMMARY
   # ============================================================
   # Completed: [Brief description]
   # Key Outputs: [files created with paths]
   # Decisions Made: DEC-XXX (if any)
   # Next Steps: [next notebook or task]
   # ============================================================

3. Save processed data with naming convention (sYY_dXX_PHASE_description.pkl)
4. Validate outputs (shape, nulls, value ranges)

Reference: Section 6.1.4 End of Notebook Checklist
```

### Pattern 2: Sprint Transition

```
End of Sprint:
1. Review sprint's deliverables against PM Guidelines checklist
2. Create next sprint's plan (PM Guidelines structure)
3. Update risk register if applicable
4. Stakeholder update following methodology communication standards
5. Archive sprint's outputs
```

### Pattern 3: Decision Making

```
When making major decisions:
1. Use methodology's Decision Log Framework (see Appendix E)
2. Document in decision_log.md file
3. Reference in project plan
4. Update Custom Instructions if approach changes
```

### Pattern 4: Context Transfer (New Chat in Same Project)

```
"New chat continuation. Review methodology + custom instructions + 
previous chat summary, then let's continue with [next task]."
```

### Common Task Reference Table

| I need to...                | Use this document          | Prompt example                                              |
| --------------------------- | -------------------------- | ----------------------------------------------------------- |
| Start new project           | Implementation Guide       | "Help me set up new project following implementation guide" |
| Write sprint plan           | PM Guidelines              | "Create Sprint 2 plan following PM Guidelines structure"    |
| Build notebook              | Collaboration Methodology  | "Create Phase 1 notebook following methodology standards"   |
| Make major decision         | Methodology + Appendix E   | "Document this decision using methodology decision log"     |
| Manage risks                | PM Guidelines (Production) | "Update risk register per PM Guidelines"                    |
| Communicate to stakeholders | Methodology Section 2.5    | "Draft update using methodology communication template"     |
| Quality check               | Both PM + Methodology      | "QA check against both PM Guidelines and methodology"       |
| Phase transition            | Methodology + Appendix E   | "Complete Phase 1 checklist from Appendix E"                |
| Advanced practice setup     | Appendix C                 | "Implement experiment tracking per Appendix C"              |
| Domain-specific guidance    | Appendix D                 | "Review time series guidance in Appendix D"                 |
| Project retrospective       | PM Guidelines (Production) | "Create post-project review per PM Guidelines"              |

### Notebook Naming Convention

- **Sprints 1-3 (development):** `sXX_dYY_PHASE_description.ipynb`
  - Example: `s02_d03_FE_aggregations.ipynb`
- **Sprint 4 (final deliverables):** `XX_PHASE_description.ipynb`
  - Example: `03_FE_core_features.ipynb`

---

## 7. Tips for Success

### Tip 1: Start Simple
- Don't activate all advanced practices immediately
- Begin with core 4-phase workflow
- Add complexity only when justified
- Check advanced practice boxes in Custom Instructions as needed

### Tip 2: Reference, Don't Repeat
```
✓ Good: "Follow methodology's Section 2.3 structure for time series"
✗ Bad: [Copy-pasting entire Phase 2 section into Custom Instructions]
```

**Why:**
- Keep Custom Instructions concise (<8K characters)
- Methodology is searchable in Project Knowledge
- Avoid duplication and maintenance burden

### Tip 3: Update Custom Instructions Throughout Project
- Add constraints when discovered
- Check/uncheck advanced practices as needed
- Note project-specific decisions
- Update timeline when it changes
- Keep stakeholder info current

### Tip 4: Use Methodology Search Triggers

**Claude will search automatically when you mention:**
- Phase transitions ("Starting Phase 2...")
- Decision documentation ("Document this decision...")
- Quality checks ("Run Phase 1 quality checklist...")
- Specific practices ("experiment tracking", "pivot criteria", etc.)

**You can also explicitly request:**
```
"Search methodology for guidance on [specific topic]"
"Review Appendix D for NLP-specific considerations"
"Check Appendix E for phase transition checklist"
```

### Tip 5: Leverage Appendices

**When to use each appendix:**
- **Appendix A:** Environment issues, package conflicts, setup troubleshooting
- **Appendix B:** Detailed phase guidance, code examples, real project patterns
- **Appendix C:** Implementing advanced practices (experiment tracking, testing, etc.)
- **Appendix D:** Domain-specific considerations (time series, NLP, CV, clustering)
- **Appendix E:** Quick checklists, templates, command reference

### Tip 6: Maintain Decision Log

**Create:** `docs/decision_log.md` at project start

**Update when:**
- Choosing between multiple approaches
- Major pivots or strategy changes
- Deviating from standard practices
- Making business vs. technical tradeoffs

**Template:** See Appendix E for decision log format

### Tip 7: Monitor Token Usage

**Watch for 90% capacity:**
- Current chat approaching ~171K tokens
- Claude will alert you
- Create session handoff document
- Start fresh chat with handoff

**Session handoff template:** See Methodology Section 6.1

---

## 8. Troubleshooting

### Issue: Claude not following standards

**Symptoms:**
- Notebooks don't match methodology structure
- Plan doesn't follow PM Guidelines format
- Text conventions not applied (emojis instead of WARNING/OK)

**Solution:**
- Check if documents uploaded to Project Knowledge
- Verify Custom Instructions reference both frameworks
- Explicitly prompt: 
  - "Reference PM Guidelines for structure"
  - "Follow methodology standards from Section X"
  - "Use text conventions from methodology (WARNING/OK/ERROR)"

### Issue: Confusion about which document to use

**Rule of thumb:**
- **Planning** = PM Guidelines
- **Executing** = Collaboration Methodology
- **Setting up** = Implementation Guide
- **Quick lookup** = Appendix E

**When in doubt:**
```
"Which document should I reference for [task]?"
```

### Issue: Too many documents to track

**Solution:**
- All documents in Project Knowledge
- Claude searches automatically when needed
- You just prompt with the task
- Reference appendices explicitly when needed

**Example:**
```
"Create Phase 2 notebook following methodology standards"
→ Claude searches main methodology

"Show me time series examples from appendix"
→ Claude searches Appendix D
```

### Issue: Standards conflicting between documents

**Resolution hierarchy:**
1. **PM Guidelines** = Structure of deliverables (what sections, what format)
2. **Methodology** = Execution details (how to build, code standards, working patterns)
3. **Appendices** = Deep dives and examples (detailed implementations)

**If true conflict:**
- Methodology takes precedence for execution
- PM Guidelines for planning structure
- Ask Claude to clarify: "These seem to conflict, which applies here?"

### Issue: Custom Instructions too long (>8K characters)

**Solution:**
- Remove methodology content (already in Project Knowledge)
- Keep only project-specific details:
  - Timeline and milestones
  - Stakeholder names and roles
  - Project constraints
  - Active advanced practices (checked boxes only)
- Reference methodology documents, don't duplicate

**Template:** See Implementation Guide for concise version

### Issue: Environment setup fails

**Common issues:**
1. **Python version mismatch:** Ensure Python 3.8+
2. **Virtual environment not activated:** Run `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
3. **Package conflicts:** Delete `.venv`, recreate, run setup script again
4. **VS Code not finding interpreter:** Ctrl+Shift+P → "Python: Select Interpreter" → choose `.venv`

**Detailed troubleshooting:** See Appendix A

### Issue: Claude forgets context mid-session

**Causes:**
- Long conversation exceeding context window
- Multiple unrelated topics discussed
- Too many chats in same project

**Solution:**
1. Create session handoff document (Section 6.1 template)
2. Start new chat
3. Reference handoff in first message:
   ```
   "Continuing from previous chat. Review session handoff document 
   in [location], then let's proceed with [next task]."
   ```

### Issue: Don't know which advanced practices to activate

**Decision framework:**

**Activate when:**
- **Experiment Tracking:** Multiple model versions, hyperparameter tuning
- **Hypothesis Management:** Research-focused, exploring multiple approaches
- **Performance Baseline:** Production deployment, need clear benchmarks
- **Ethics & Bias:** Working with sensitive data, fairness concerns
- **Testing Strategy:** Production code, team environment
- **Data Versioning:** Multiple data sources, frequent updates
- **Technical Debt:** Long-term project, future maintenance
- **Scalability:** Large datasets, production deployment
- **Literature Review:** Novel techniques, research project
- **Risk Management:** High-stakes project, many uncertainties

**Start simple:**
- First project: Core workflow only (no advanced practices)
- Familiar domain: Add 1-2 practices as needed
- Complex project: Activate 3-5 practices upfront

**Reference:** Appendix C for detailed guidance on each practice

---

## When to Reference Which Document

| Situation                  | Primary Reference                 | Secondary Reference     |
| -------------------------- | --------------------------------- | ----------------------- |
| Starting new project       | This guide + Implementation Guide | -                       |
| Environment issues         | Appendix A                        | setup scripts           |
| Creating notebooks         | Methodology Section 2.X           | Appendix B (examples)   |
| Documenting decisions      | Methodology Section 4.1           | Appendix E (template)   |
| Stakeholder updates        | Methodology Section 2.5           | -                       |
| Pivot decision needed      | Methodology Section 4.2           | -                       |
| Writing sprint plan        | PM Guidelines Section X           | -                       |
| Complex multi-day planning | PM Guidelines v2.0 Templates      | -                       |
| Managing risks             | PM Production Extension           | -                       |
| Defining deliverables      | PM Guidelines Section X           | -                       |
| Quality assurance          | Methodology Section 6             | PM Production Extension |
| Governance & roles         | PM Production Extension           | -                       |
| Advanced practice setup    | Appendix C                        | Methodology Section 5   |
| Domain-specific guidance   | Appendix D                        | -                       |
| Quick command lookup       | Appendix E                        | -                       |
| Phase transition           | Methodology Section 2.X           | Appendix E (checklist)  |
| Project retrospective      | PM Production Extension           | -                       |

---

## What Makes This System Unique

### 1. Battle-Tested Foundation
- Built from successful the TravelTide customer segmentation and the Favorita demand forecasting projects
- Proven patterns that actually worked

### 2. Clear Organization
- Numbered priority system (0_ START HERE → 1_ Execution → 2_ Planning → 3_ Setup)
- Self-documenting with hierarchical numbering (no TOC maintenance)
- Quick start (5 minutes) to comprehensive guide
- Modular appendices for targeted deep dives

### 3. Complete Integration
- Project Reference + Methodology + PM Guidelines + Implementation
- All documents reference each other appropriately using section numbers
- No duplication, clear boundaries between document purposes
- Hybrid approach (Project Knowledge + Custom Instructions)

### 4. Academic-Optimized, Production-Ready
- Standard edition for coursework/thesis/portfolio
- Production edition for industry work with governance
- Advanced Practices activate as needed (10 optional complexity practices)
- Professional standards throughout (no emojis, WARNING/OK/ERROR)

### 5. Claude-Specific Design
- Uses Project Knowledge effectively (searchable, unlimited size)
- Custom Instructions template optimized (<8K characters)
- Progressive execution patterns (cell-by-cell, review outputs)
- Token monitoring built-in (alert at 90%, handoff templates)
- Automatic methodology search on trigger phrases

### 6. Hierarchical Structure (v1.1.3)
- Main methodology: ~3,130 lines (focused on core workflow)
- Consolidated appendices: ~3,920 lines (5 appendices in one file)
- Total: ~7,050 lines of methodology content
- Section numbering: "See Section 4.1.2" instead of "See Phase X"
- Easy referencing and navigation
- Better maintainability with consolidated structure

---

## Quality Checklist: Integrated Approach

### Project Planning (PM Guidelines)
- [ ] Purpose clearly defined with business value
- [ ] All inputs and dependencies documented
- [ ] Timeline with daily/sprint milestones
- [ ] Deliverables with success criteria
- [ ] Readiness checklist for phase transitions
- [ ] Documentation and ownership assigned

### Execution (Collaboration Methodology)
- [ ] 4-phase workflow followed
- [ ] Notebooks ~400 lines, 5-6 sections each
- [ ] Decision log maintained for major choices
- [ ] Quality checks at each phase
- [ ] Stakeholder communication cadence followed
- [ ] Text conventions followed (WARNING/OK/ERROR, no emojis)

### Style (Both Documents)
- [ ] Professional tone throughout
- [ ] No emojis or decorative symbols
- [ ] Each notebook cell has markdown description + visible output
- [ ] Code commented appropriately
- [ ] Markdown hierarchy consistent (##, ###, ####)

### Governance (Production PM Guidelines)
- [ ] Roles clearly assigned (RACI)
- [ ] Risk register maintained
- [ ] Data versioning implemented
- [ ] Peer review completed
- [ ] Post-project review scheduled

---

## Maintenance

### Update Methodology When:
- Learn new best practices
- Discover common failure patterns
- Add domain-specific adaptations
- Project complexity increases
- New tools or techniques emerge

### Update Custom Instructions When:
- Timeline changes
- Stakeholders change
- Requirements evolve
- Activate new advanced practices
- Discover project-specific constraints
- Deliverables scope changes

### Archive After Project:
- Export final notebooks
- Save decision log
- Document lessons learned
- Create project retrospective (PM Production Extension template)
- Add key insights to Project Knowledge for future reference

---

## Common Mistakes to Avoid

**WARNING: Custom Instructions character limit (~8K characters)**
- Keep concise, reference methodology documents
- Don't duplicate methodology content
- Focus on project-specific details only
- Use checkboxes for advanced practices (checked = active)

**WARNING: Don't skip Custom Instructions**
- Claude needs project context to work effectively
- Generic methodology isn't enough for personalization
- Stakeholder info is critical for communication
- Timeline helps Claude pace the work

**WARNING: Update as you go**
- Don't set and forget
- Projects evolve, instructions should too
- Dead/outdated instructions worse than no instructions
- Review and update each sprint

**OK: This approach scales**
- Same methodology for all projects
- Only Custom Instructions change per project
- Reusable, maintainable, efficient
- Proven across multiple domains

---

## Complete Project Lifecycle Example

### Project: Customer Segmentation Analysis

**Setup Phase (Day 0)**
```
0. Run environment setup:
   # Academic/exploratory:
   python setup_base_environment_minimal.py
   
   # Production (with code quality):
   python setup_base_environment_prod.py
   
   - Install VS Code extensions
   - Select interpreter
1. Create Claude Project: "Customer Segmentation Q1 2025"
2. Upload to Project Knowledge:
   - Data_Science_Collaboration_Methodology (main + appendices)
   - PM_Guidelines_v2 (core - always)
   - PM_ProdGuidelines_extension (add if production/enterprise)
   - Implementation_Guide
3. Write Custom Instructions (using template from Implementation Guide)
4. First message: "Review system guide and help create Sprint 1 plan"
```

**Sprint 1: Planning & EDA**
```
Day 1:
- Reference: PM Guidelines v2 (add Production Extension if needed)
- Create: CustomerSeg_Sprint1_Plan.md (project plan)
- Sections: Purpose, Inputs, Timeline, Deliverables, Success Criteria

Day 2-5:
- Reference: Methodology Section 2.2 + Appendix B
- Create: 01_EDA_data_quality.ipynb, 02_EDA_behavioral.ipynb
- Follow: Methodology notebook standards (~400 lines, 5-6 sections)
- Document: Decision log entries as needed
```

**Sprint 2: Feature Engineering**
```
Day 1:
- Reference: PM Guidelines v2
- Create: CustomerSeg_Sprint2_Plan.md

Day 2-5:
- Reference: Methodology Section 2.3 + Appendix B
- Create: 03_FE_core.ipynb, 04_FE_advanced.ipynb
- Follow: Feature engineering standards
- Document: Major feature decisions
```

**Sprint 3: Clustering Analysis**
```
Day 1:
- Reference: PM Guidelines v2 + Appendix D (clustering guidance)
- Create: CustomerSeg_Sprint3_Plan.md

Day 2-5:
- Reference: Methodology Section 2.4 + Appendix D
- Create: 05_CLUSTERING_prep.ipynb, 06_CLUSTERING_assignment.ipynb
- Document: Major decision on K selection (decision log)
- Validate: Silhouette, Davies-Bouldin, Calinski-Harabasz scores
```

**Sprint 4: Communication**
```
Day 1:
- Reference: PM Guidelines v2
- Create: CustomerSeg_Sprint4_Plan.md

Day 2-5:
- Reference: Methodology Section 2.5
- Create: Presentation, reports, documentation
- Follow: Communication standards
- Deliver: Stakeholder presentations
```

---

## Summary: Integrated System Benefits

**Separation of Concerns:**
- PM Guidelines = WHAT to deliver and HOW to structure plans
- Methodology = HOW to execute and work with Claude
- Appendices = Detailed implementations and examples
- Implementation Guide = HOW to set up the system

**Flexibility:**
- Choose standard or production PM Guidelines based on project type
- Activate methodology advanced practices as needed (checkboxes in Custom Instructions)
- Use appendices for targeted deep dives
- Customize via Custom Instructions (project-specific only)

**Efficiency:**
- All documents in Project Knowledge (searchable, unlimited size)
- Custom Instructions stay concise (project-specific context only)
- No duplication across documents
- Hierarchical numbering enables easy referencing

**Quality:**
- Consistent planning structure (PM Guidelines)
- Consistent execution workflow (Methodology)
- Professional standards throughout (both documents)
- Battle-tested patterns from real projects

**Scalability:**
- Same system for simple projects (core workflow only)
- Same system for complex projects (activate advanced practices)
- Same system across domains (appendices provide domain guidance)
- Grows with your needs

---

## What Goes Where - Quick Reference

| Content Type                        | Location                            | Why                              |
| ----------------------------------- | ----------------------------------- | -------------------------------- |
| Complete methodology (~6,565 lines) | Project Knowledge                   | Searchable, reusable, no limits  |
| Project-specific context            | Custom Instructions                 | Always active, concise           |
| 4-phase workflow details            | Methodology (search when needed)    | Generic framework                |
| This project's timeline             | Custom Instructions                 | Specific to current work         |
| Decision log templates              | Appendix E (reference)              | Reusable format                  |
| This project's key decisions        | docs/decision_log.md (project file) | Track actual choices             |
| Notebook structure guide            | Methodology Section 2.X             | Generic standard                 |
| This project's notebooks            | notebooks/ (working files)          | Actual deliverables              |
| Advanced practices catalog          | Methodology Section 5 + Appendix C  | Reference library                |
| Which practices for this project    | Custom Instructions (checkboxes)    | Activation flags                 |
| Environment setup details           | Appendix A                          | Troubleshooting                  |
| Phase examples with code            | Appendix B                          | Detailed guidance                |
| Domain-specific patterns            | Appendix D                          | Time series, NLP, CV, clustering |
| Quick checklists & commands         | Appendix E                          | Fast reference                   |
| File naming standards               | Appendix E.11 (detailed)            | Complete conventions             |
| File naming quick card              | 1.4_File_Naming_Quick_Reference.md  | Printable daily reference        |

---

## Next Steps

**For Your First Project:**

1. **Read this document** (you're here!) ✓
2. **Run environment setup** (10 minutes)
3. **Create Claude Project** with initial instructions
4. **Upload to Project Knowledge:**
   - 0_START_HERE_Complete_Guide.md
   - 1.0_Data_Science_Collaboration_Methodology_v1.1.md
   - 1.0_Methodology_Appendices.md
   - 2_0_ProjectManagement_Guidelines_v2_v1.1.md
   - 3_Methodology_Implementation_Guide_v1.1.md
5. **Write Custom Instructions** (use template from file 3)
6. **Send first chat message** (pattern in Section 5)
7. **Create project structure** (directories, README files)
8. **Start Sprint 1 planning** (PM Guidelines)
9. **Execute phases 1-4** (Methodology)

**For Your Second Project:**

1. Copy Custom Instructions template from first project
2. Update project-specific sections (timeline, stakeholders, domain)
3. Adjust advanced practices checkboxes as needed
4. Start immediately with Sprint 1 planning

**Same methodology, different projects. That's the power of this system.**

---

**Version Notes**

- **v1.0.0** (2025-11-13): Initial release with separate files
- **v1.1.0** (2025-11-19): Methodology reorganization (main + 5 separate appendices)
- **v1.1.1** (2025-11-19): File consolidation (getting started: 3→1, appendices: 5→1)

**Your complete, integrated, professional data science project management system is ready to use!**

Start with the Quick Start (Section 1), follow the Hybrid Setup (Section 4), and execute using the patterns in Section 6. When in doubt, reference the troubleshooting guide (Section 8) or explicitly ask Claude which document to use.
