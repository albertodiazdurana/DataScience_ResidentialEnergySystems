# Methodology Implementation Guide

**Purpose:** Quick setup guide for new data science projects using Claude  
**Version:** 1.1.1  
**Last Updated:** 2025-11-19

---

## 1. Overview

### What This Guide Provides

**Complete Custom Instructions Template** for configuring Claude projects with:
- Project planning context (scope, stakeholders, timeline)
- Execution standards (notebook format, code quality, communication)
- Domain-specific adaptations
- Advanced practices selection

**Two Complete Examples:**
- Time Series Forecasting (operational predictions)
- NLP Sentiment Analysis (classification with deployment)

### Quick Start (5 Steps)

1. **Read:** `0_START_HERE_Complete_Guide.md` (system overview)
2. **Upload to Project Knowledge:**
   - Main methodology + appendices
   - PM Guidelines
   - This implementation guide
3. **Copy template** (Section 2) → Customize for your project
4. **Add to Custom Instructions** in Claude Project settings
5. **Start first chat** with project plan request

**For detailed setup, see:** `0_START_HERE_Complete_Guide.md` Section 4

---

## 2. Custom Instructions Template

**Copy this template and customize bracketed sections:**

```markdown
# Project: [PROJECT_NAME]
Domain: [Time Series / NLP / Computer Vision / Clustering / Regression / Classification]

## Framework Documents
This project uses:
- **PM Guidelines** (Project Knowledge): Project planning structure and templates
- **Collaboration Methodology v1.1.1** (Project Knowledge): Execution workflow with hierarchical numbering
- **Project Reference Documentation** (Project Knowledge): Domain context (create if needed)
- **Complete Getting Started Guide** (Project Knowledge): Integrated system overview

## Project Planning Context

### Scope
- **Purpose**: [Main objective and business value in 1-2 sentences]
- **Resources**: [Time: X sprints, Team: Y people, Budget/constraints]
- **Success Criteria**:
  - Quantitative: [Measurable metrics, e.g., "RMSE < 10%", "F1 > 0.85"]
  - Qualitative: [Business alignment, e.g., "Actionable insights for marketing"]
  - Technical: [Reproducibility, documentation quality]

### Data & Dependencies
- **Primary dataset**: [Name, size (rows/GB), source, access method]
- **Secondary data**: [External sources, APIs, if applicable]
- **Dependencies**: [Outputs from prior work, team deliverables]
- **Data quality**: [Known issues: missing values, outliers, bias]

### Stakeholders & Governance
- **Primary**: [Name, role] - needs [information type, e.g., "executive summary"]
- **Secondary**: [Name, role] - needs [information type, e.g., "technical details"]
- **Communication**: [Frequency: per sprint/biweekly, Format: email/Slack/presentation]
- **Governance** (Production only): [Project Lead, Data Owner, RACI matrix if multi-team]

## Execution Context

### Timeline & Phases
- **Duration**: [X sprints total]
- **Phase 1 - Exploration** (Sprint 1): [Specific focus for your domain]
- **Phase 2 - Feature Engineering** (Sprint 2): [Key features to create]
- **Phase 3 - Analysis** (Sprint 3): [Models/algorithms to test - might iterate to phase 2 if major changes are identified]
- **Phase 4 - Communication** (Sprint 4): [Deliverables to produce]

### Deliverables
- [ ] Notebooks: [Number, e.g., "6 notebooks following methodology structure"]
- [ ] Project plans: [Sprint plans following PM Guidelines templates]
- [ ] Presentation: [Slide count, audience, e.g., "15 slides for executives"]
- [ ] Report: [Length, format, e.g., "20-page technical report"]
- [ ] Other: [Code package, API, dashboard, etc.]

## Domain Adaptations

### Key Techniques (Reference: Appendix D for domain-specific guidance)
- [Technique 1 specific to this domain/problem]
- [Technique 2 specific to this domain/problem]
- [Technique 3 specific to this domain/problem]

### Known Challenges
- [Challenge 1] → [Mitigation strategy]
- [Challenge 2] → [Mitigation strategy]

### Solved Challenges (Update as you progress)
- [Challenge X] → [Solution applied]

## Advanced Practices

**Select from Methodology Section 5 (activate as needed):**
- [ ] Experiment Tracking (ML-heavy, comparing >10 model variants)
- [ ] Hypothesis Management (research/academic projects)
- [ ] Performance Baseline & Benchmarking (production benchmarking required)
- [ ] Ethics & Bias Considerations (sensitive data, fairness concerns)
- [ ] Testing Strategy (production deployment, team collaboration)
- [ ] Data Versioning & Lineage (frequent data updates, multiple sources)
- [ ] Technical Debt Register (long-term maintenance, production systems)
- [ ] Scalability Considerations (large datasets >10GB, production deployment)
- [ ] Literature Review Phase (novel domain, research validation)
- [ ] Risk Management (high-stakes decisions, production requirements)

**For implementation details, see:** Appendix C

## Communication & Style

### Artifact Generation
- Ask clarifying questions before generating artifacts
- Confirm understanding: "Confirm that you understand what I need"
- Be concise in work
- Progressive execution: Execute cell-by-cell, each output becomes reference
- ~400 lines per notebook, 5-6 sections
- Follow methodology notebook structure (Section 3.1)
- File naming: See Appendix E.11 for detailed conventions

### Environment Setup
- Run `setup_base_environment_minimal.py` (academic) or `setup_base_environment_prod.py` (production)
- Generate domain extensions as needed (see Appendix A for guidance)
- Always resolve paths relative to project root using `.resolve()`
- Document functions with docstrings
- See Methodology Section 2.1 (Environment Setup) for complete guide

### Standards (CRITICAL - Always Follow)

**Text Formatting:**
- Never use emojis (no ✅ ❌ ⚠️ 📊 etc.)
- Use plain text: "OK:", "WARNING:", "ERROR:"
- Checkboxes: `[ ]` incomplete, `[x]` complete
- ASCII-only characters in all documentation

**Code Output:**
- Show actual values/metrics (shapes, counts, correlations)
- Avoid generic confirmations: "Complete!", "Done!", "Success!"
- Use: `print(f"Correlation: {value:.3f}")` or `print(df.shape)`
- Avoid: `print("Data loaded successfully!")`

**Print Statement Patterns (See Appendix E.4 for details):**
- Use DataFrame string methods: `print(df.to_string(index=False))`
- Use f-strings for metrics: `print(f"RMSE: {rmse:.4f}")`
- Let pandas/numpy handle formatting

**Notebook Standards:**
- Always precede code cells with markdown description
- Format: "### Section X: [Name]" with 1-2 sentence explanation
- Each code cell must show visible output
- See Methodology Section 3 for complete standards

### Session Management
- Monitor tokens continuously
- Alert at 80% capacity (~160K tokens)
- Provide session summary as Handoff for the following chat if nearing limit
- Reference Methodology Section 6.1 for session handoff templates
- Upload critical handoffs to Project Knowledge for continuity

### Language & Formatting
- Primary language: [English / German / Spanish]
- Presentation language: [If different from primary]
- Number format: [1,234.56 or 1.234,56]
- Date format: [YYYY-MM-DD or DD/MM/YYYY]
- Code examples: [Language/framework if specific]

## Project-Specific Requirements
- [Unique constraints: regulatory, compliance, business rules]
- [Required/prohibited tools or libraries]
- [Output format specifications: file types, schemas]
- [Performance requirements: runtime, memory, latency]
- [Privacy/security considerations]
```

---

## 3. Template Usage Guide

### Filling Out the Template

**Project Planning Context:**
- **Purpose:** One clear sentence. Business value first, technical second.
- **Success Criteria:** Be specific. "Improve model" is vague. "RMSE < 10% of baseline" is clear.
- **Stakeholders:** Include communication preferences (technical depth, frequency).

**Execution Context:**
- **Timeline:** Methodology assumes 4-sprint academic project structure unless specified. See DSM_0 Section 1.5 for sprint configuration.
- **Phase Focus:** Customize based on domain (see Appendix D for domain-specific guidance).

**Domain Adaptations:**
- **Key Techniques:** List 3-5 domain-specific methods you'll use.
- **Known Challenges:** Document upfront. Add solutions as you discover them.

**Advanced Practices:**
- Start simple: Check only 2-3 practices initially.
- Add more as project complexity increases.
- Each checked practice has detailed implementation in Appendix C.

**Communication & Style:**
- Keep this section mostly as-is (proven standards).
- Customize language/formatting based on location and audience.

### When to Update Custom Instructions

**During project:**
- ✓ Activate new advanced practices (check boxes)
- ✓ Add newly discovered challenges and solutions
- ✓ Update timeline if scope changes
- ✓ Add project-specific requirements as discovered

**Don't update:**
- Core standards (text formatting, notebook structure)
- Methodology references (keep stable)

### What NOT to Include

**Avoid duplicating:**
- Complete methodology content (it's in Project Knowledge, searchable)
- Detailed templates (reference section numbers instead)
- Generic guidance (focus on project-specific only)

**Character limit:** Keep under 8K characters for best performance.

---

## 4. Domain-Specific Examples

### Example 1: Time Series Forecasting

```markdown
# Project: Energy Demand Forecasting
Domain: Time Series Analysis

## Framework Documents
[Standard framework references - see template]

## Project Planning Context

### Scope
- **Purpose**: Forecast daily energy demand 7 days ahead for grid optimization and cost reduction
- **Resources**: 4 sprints unless specified
- **Success Criteria**:
  - Quantitative: MAPE < 8%, MAE < 500 kWh
  - Qualitative: Actionable 7-day forecasts for operations team
  - Technical: Reproducible pipeline, <2hr runtime

### Data & Dependencies
- **Primary dataset**: Historical demand (PostgreSQL), 3 years hourly data (~26K rows)
- **Secondary data**: Weather data (CSV), daily temperature/humidity
- **Dependencies**: None
- **Data quality**: Missing values from sensor failures (known 2% rate), holiday outliers

### Stakeholders & Governance
- **Primary**: Operations Manager (non-technical) - needs forecast accuracy and confidence intervals
- **Secondary**: Engineering team (technical) - needs reproducible pipeline
- **Communication**: Per sprint email updates, final presentation

## Execution Context

### Timeline & Phases
- **Duration**: 4 sprints
- **Phase 1 - Exploration** (Sprint 1): Stationarity tests, seasonality decomposition, trend analysis
- **Phase 2 - Feature Engineering** (Sprint 2): Lag features (1-7 days), rolling stats (7/14/30 day), datetime components (day-of-week, month)
- **Phase 3 - Analysis** (Sprint 3): ARIMA baseline, Prophet seasonal model, LSTM comparison
- **Phase 4 - Communication** (Sprint 4): Multi-step predictions with confidence intervals, deployment function

### Deliverables
- [ ] Notebooks: 6 (following 4-phase structure)
- [ ] Project plans: Per sprint following PM Guidelines v2.0 templates
- [ ] Presentation: 15 slides for operations team (non-technical focus)
- [ ] Report: 20 pages technical documentation
- [ ] Other: Python forecasting function for deployment

## Domain Adaptations

### Key Techniques (See Appendix D.1: Time Series for details)
- Augmented Dickey-Fuller test for stationarity
- ACF/PACF plots for lag selection
- Time-series cross-validation (no shuffling, expanding window)
- Prophet for handling holidays and seasonality
- Multi-step forecasting with uncertainty quantification

### Known Challenges
- Missing values from sensor failures → Forward fill <6hrs, interpolate >6hrs
- Holiday effects need explicit modeling → Use Prophet holiday calendar
- Outliers during extreme weather → Winsorization at 1st/99th percentiles

## Advanced Practices

- [x] Experiment Tracking (comparing ARIMA/Prophet/LSTM variants)
- [x] Performance Baseline (naive forecast: yesterday's demand)
- [ ] Ethics & Bias Review (not applicable - operational data)
- [x] Testing Strategy (deployment requires unit tests for forecast function)

## Communication & Style
[Use standard template - no changes needed]

### Language & Formatting
- Primary language: English
- Presentation: English with simplified terminology for operations
- Numbers: US format (1,234.56)
- Dates: YYYY-MM-DD

## Project-Specific Requirements
- Focus on interpretability (operations team must understand model behavior)
- Uncertainty quantification critical (confidence intervals mandatory for all forecasts)
- Forecast horizon: Exactly 7 days (weekly planning cycle)
```

### Example 2: NLP Sentiment Analysis

```markdown
# Project: Customer Review Sentiment Analysis
Domain: Natural Language Processing (NLP)

## Framework Documents
[Standard framework references - see template]

## Project Planning Context

### Scope
- **Purpose**: Classify product reviews as positive/negative/neutral for marketing insights and product improvement
- **Resources**: 3 sprints, solo project
- **Success Criteria**:
  - Quantitative: F1-score > 0.80 on balanced test set, precision > 0.85 (minimize false positives)
  - Qualitative: Marketing-actionable insights by product category
  - Technical: Inference latency <100ms per review, model explainability

### Data & Dependencies
- **Primary dataset**: 50K product reviews from company database (SQL export to CSV)
- **Secondary data**: Product metadata (IDs, categories, timestamps, star ratings)
- **Dependencies**: None
- **Data quality**: Class imbalance (70% positive, 20% neutral, 10% negative), some multilingual reviews

### Stakeholders & Governance
- **Primary**: Marketing Director (non-technical) - needs aggregate sentiment trends by product
- **Secondary**: Product team (semi-technical) - needs per-product breakdown with examples
- **Communication**: Bi-weekly check-ins, Slack updates for questions

## Execution Context

### Timeline & Phases
- **Duration**: 3 sprints
- **Phase 1 - Exploration** (Sprint 1): Text length distributions, vocabulary analysis, class balance, language detection
- **Phase 2 - Feature Engineering** (Sprint 1-2): Text preprocessing pipeline, TF-IDF vectors, word embeddings, BERT tokenization
- **Phase 3 - Analysis** (Sprint 2-3): Logistic regression baseline, LSTM with embeddings, fine-tuned BERT comparison
- **Phase 4 - Communication** (Sprint 3): Model cards, API design, monitoring recommendations, deployment guide

### Deliverables
- [ ] Notebooks: 6 (EDA, preprocessing, baseline, advanced models, evaluation, deployment prep)
- [ ] Project plans: Per sprint following PM Guidelines v1.0 templates (simple planning sufficient)
- [ ] Presentation: 12 slides for marketing team (business focus, sample predictions)
- [ ] Report: 15 pages with model cards and bias analysis
- [ ] Other: Inference API documentation, preprocessing function package

## Domain Adaptations

### Key Techniques (See Appendix D.2: NLP for details)
- Text preprocessing pipeline (cleaning, tokenization, stopword removal, lemmatization)
- Handling class imbalance (weighted loss functions or SMOTE for minority classes)
- Transfer learning with pre-trained transformers (BERT, RoBERTa)
- Model explainability (SHAP or LIME for prediction interpretation)
- Multi-class evaluation (per-class precision/recall, confusion matrix)

### Known Challenges
- Imbalanced classes (70% positive, 20% neutral, 10% negative) → Weighted loss, stratified sampling
- Sarcasm and nuanced language detection → Focus on clear cases first, flag ambiguous for review
- Multilingual reviews (English + Spanish) → Focus on English subset first (80%), expand if time permits

## Advanced Practices

- [x] Experiment Tracking (comparing TF-IDF/LSTM/BERT architectures and hyperparameters)
- [x] Performance Baseline (majority class predictor, then logistic regression with TF-IDF)
- [x] Ethics & Bias Review (avoid demographic bias in sentiment detection, test on diverse examples)
- [x] Testing Strategy (unit tests for preprocessing, integration tests for end-to-end pipeline)
- [ ] Hypothesis Management (academic rigor not required for business project)

## Communication & Style
[Use standard template - no changes needed]

### Language & Formatting
- Primary: English
- Presentation: Business-friendly language (avoid ML jargon, use examples)
- Include sample predictions with explanations for stakeholder understanding

## Project-Specific Requirements
- Model interpretability needed (SHAP or LIME for explaining individual predictions to product team)
- Inference latency: <100ms per review (real-time application requirement)
- Cannot use customer names or PII in examples (privacy requirement)
- Must handle out-of-vocabulary words gracefully (robust to typos, slang)
- Confidence scores required (flag low-confidence predictions for manual review)
```

---

## 5. Quick Reference

### Key Methodology References

| Need                       | Location                                      | Section         |
| -------------------------- | --------------------------------------------- | --------------- |
| Complete system overview   | `0_START_HERE_Complete_Guide.md`              | All             |
| Environment setup          | Main Methodology                              | Section 2.1     |
| Phase guidance             | Main Methodology                              | Section 2.2-2.5 |
| Phase detailed examples    | Appendix B                                    | All sections    |
| Notebook standards         | Main Methodology                              | Section 3.1     |
| Code quality               | Main Methodology                              | Section 3.2     |
| Decision log framework     | Main Methodology                              | Section 4.1     |
| Advanced practices         | Main Methodology                              | Section 5       |
| Advanced practices details | Appendix C                                    | All sections    |
| Session management         | Main Methodology                              | Section 6.1     |
| File naming standards      | Appendix E                                    | E.11            |
| File naming quick card     | `1.4_File_Naming_Quick_Reference.md`          | All             |
| Domain adaptations         | Appendix D                                    | D.1-D.5         |
| Quick checklists           | Appendix E                                    | E.1-E.10        |
| PM Guidelines templates    | `2_0_ProjectManagement_Guidelines_v2_v1.1.md` | All             |

### Common Prompts for First Chat

**Setup & Planning:**
```
"I'm starting a new [domain] project. Please:
1. Review the Complete Getting Started Guide in Project Knowledge
2. Review the Collaboration Methodology (core + relevant appendices)
3. Read my Custom Instructions
4. Confirm understanding of our working style
5. Help me create Sprint 1 project plan following PM Guidelines structure"
```

**Domain Extension:**
```
"Based on my project documentation, generate domain-specific package 
installation script (setup_domain_extensions.py) that extends the base 
environment with packages for [time series/NLP/computer vision/etc.]"
```

**Phase Kickoff:**
```
"Starting Phase [X]: [Phase name]. Review methodology Section 2.[X] for 
best practices, then help me create [specific deliverable following 
methodology standards]."
```

### Tips for Success

**DO:**
- ✓ Start simple (core workflow only, add advanced practices as needed)
- ✓ Reference methodology sections (don't duplicate in Custom Instructions)
- ✓ Update Custom Instructions as project evolves
- ✓ Use file naming conventions from Day 1 (Appendix E.11)
- ✓ Create decision log early (track major choices)
- ✓ Follow text conventions (WARNING/OK/ERROR, no emojis)

**DON'T:**
- ✗ Copy entire methodology sections into Custom Instructions
- ✗ Activate all advanced practices immediately
- ✗ Skip environment setup (causes issues later)
- ✗ Use emojis or special characters in documentation
- ✗ Print generic confirmations ("Done!", "Complete!")
- ✗ Forget to update Custom Instructions when scope changes

### Troubleshooting

**Issue:** Claude not following standards  
**Solution:** Explicitly reference section numbers: "Follow methodology Section 3.1 notebook standards"

**Issue:** Custom Instructions too long (>8K characters)  
**Solution:** Remove methodology content, keep only project-specific details

**Issue:** Lost context between sessions  
**Solution:** Create session handoff document (Section 6.1 template), upload to Project Knowledge

**Issue:** Unsure which advanced practices to activate  
**Solution:** Start with 0-2 practices, add as complexity increases. See Appendix C for guidance.

**For complete troubleshooting guide, see:** `0_START_HERE_Complete_Guide.md` Section 8

---

## Version History

**v1.1.1** (2025-11-19):
- Updated all references to v1.1.1 file structure
- Consolidated content, removed duplication
- Updated file naming references to Appendix E.11
- Streamlined examples with reference-based approach
- Added Quick Reference section
- Aligned with consolidated methodology system

**v1.1.0** (2025-11-19):
- Updated references to hierarchical numbering
- Added appendix references

**v1.0** (2025-11-13):
- Initial release with comprehensive template
- Two domain examples (Time Series, NLP)

---

**End of Implementation Guide**

**For complete methodology system, see:** `0_START_HERE_Complete_Guide.md`  
**For detailed phase guidance, see:** `1.0_Methodology_Appendices.md`
