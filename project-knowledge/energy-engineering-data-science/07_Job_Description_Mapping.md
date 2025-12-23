# Job Description to Study Guide Mapping

## Green Fusion - Senior Data Scientist (m/f/d)

This document maps each requirement and task from the job description to relevant sections in the study guide, enabling targeted preparation.

---

## Tasks Mapping

### Task 1: Data Cleaning and Analysis
> "You clean and analyze data to identify patterns and trends, uncovering insights that drive our solutions."

| Topic | File | Section |
|-------|------|---------|
| Time series data handling | Part II | Chapter 6.2: Resampling and Interpolation |
| Missing data strategies | Part II | Chapter 6.2: Gap handling policies |
| Outlier detection | Part IV | Chapter 16.2: detect_sensor_outliers() |
| Pattern identification | Part II | Chapter 11.3: Identifying Operational Regimes |
| Baseline analysis | Part V | Chapter 18.1: Phase 2 - Baseline Analysis |
| Data quality assessment | Part III | Chapter 12.3: BatchETLPipeline._assess_quality() |

---

### Task 2: Statistical Analysis
> "You apply statistical techniques to interpret data, ensuring the reliability and accuracy of your findings."

| Topic | File | Section |
|-------|------|---------|
| Statistical anomaly detection | Part II | Chapter 8.1: Z-score, IQR, Grubbs' test |
| Hypothesis testing for drift | Part III | Chapter 14.4: KS test, PSI calculation |
| Correlation analysis | Part II | Chapter 6.1: Autocorrelation function |
| Confidence intervals | Part V | Chapter 18.1: Weather-normalized comparison |
| Distribution analysis | Part III | Chapter 14.4: DataDriftMonitor |

---

### Task 3: Predictive Modeling
> "You build data models to predict heating system behavior and patterns using advanced analytics and machine learning."

| Topic | File | Section |
|-------|------|---------|
| Heat demand forecasting | Part II | Chapter 7: Complete chapter |
| ARIMA/SARIMA models | Part II | Chapter 7.1: Classical Time Series Methods |
| Gradient boosting (XGBoost, LightGBM) | Part II | Chapter 7.2: ML Approaches |
| LSTM for sequences | Part II | Chapter 7.3: Deep Learning |
| COP estimation | Part II | Chapter 10.1: COP estimation code |
| Building thermal models | Part IV | Chapter 16.2: fit_building_thermal_model() |
| Feature engineering | Part II | Chapter 6.3: Complete section |
| Cross-validation for time series | Part IV | Chapter 16.3: BlockingTimeSeriesSplit |

---

### Task 4: Production Algorithm Development
> "You develop production-ready algorithms and data pipelines to optimize energy system components, reduce CO₂ emissions, and enhance energy efficiency."

| Topic | File | Section |
|-------|------|---------|
| Heating curve optimization | Part I | Chapter 3.1: Heizkennlinie |
| Control algorithms | Part II | Chapter 9: Complete chapter |
| Model Predictive Control | Part II | Chapter 9.2: MPC implementation |
| Peak shaving | Part II | Chapter 9.5: Peak shaving schedule |
| Data pipeline design | Part III | Chapter 12: Complete chapter |
| ETL patterns | Part III | Chapter 12.3: Stream and batch processing |
| Code quality standards | Part III | Chapter 13.1: Type hints, SOLID principles |
| Production deployment | Part III | Chapter 15: Complete chapter |

---

### Task 5: Full Development Lifecycle
> "You're responsible for the full development cycle of product features — from understanding customer requirements to final deployment — collaborating closely with energy engineers, frontend and backend developers, and product and customer success managers."

| Topic | File | Section |
|-------|------|---------|
| Requirements translation | Part V | Chapter 20.2: Translating Customer Requirements |
| Working with engineers | Part V | Chapter 20.1: Working with Energy Engineers |
| API design for frontend/backend | Part IV | Chapter 17.3: REST API Design |
| GraphQL for data access | Part IV | Chapter 17.2: GraphQL schema and client |
| CI/CD pipelines | Part III | Chapter 14.3: GitHub Actions workflow |
| A/B testing | Part III | Chapter 15.3: ABTestRouter |
| Gradual rollout | Part III | Chapter 15.3: GradualRollout class |
| Communicating results | Part V | Chapter 20.3: Communicating ML Results |

---

### Task 6: Experimental Analysis
> "You analyze experimental data to refine and improve energy optimization algorithms."

| Topic | File | Section |
|-------|------|---------|
| Baseline vs. optimized comparison | Part V | Chapter 18.1: measure_optimization_impact() |
| Weather normalization | Part V | Chapter 18.1: consumption_per_hdd() |
| Experiment tracking | Part III | Chapter 14.1: MLflow integration |
| Model performance monitoring | Part III | Chapter 14.4: ModelPerformanceMonitor |
| Case study: WSL Leipzig | Part V | Chapter 18.1: 16.5% savings analysis |
| Case study: GWU Eckernförde | Part V | Chapter 18.2: Heat pump efficiency diagnosis |

---

### Task 7: Communication
> "You present your findings in a clear, concise, and understandable way."

| Topic | File | Section |
|-------|------|---------|
| Non-technical summaries | Part V | Chapter 20.3: create_executive_summary() |
| Visualization best practices | Part V | Chapter 20.3: create_savings_visualization() |
| Engineer-friendly reports | Part V | Chapter 20.1: present_anomaly_findings() |
| Translating DS to domain | Part V | Chapter 20.1: collaboration_principles |

---

### Task 8: Energy Time Series Prediction
> "You support the team in creating data models for predicting energy time series data (e.g., heat demand, solar production, electricity consumption)."

| Topic | File | Section |
|-------|------|---------|
| Time series fundamentals | Part II | Chapter 6: Complete chapter |
| Seasonality handling | Part II | Chapter 6.1: Multiple seasonality scales |
| Fourier features | Part II | Chapter 6.3: fourier_features() |
| Weather data integration | Part II | Chapter 7.4: Weather Data Integration |
| Lag features | Part IV | Chapter 16.1: create_lag_features() |
| Rolling statistics | Part IV | Chapter 16.1: create_rolling_features() |

---

### Task 9: ML Techniques (Supervised, Unsupervised, RL)
> "...optimizing energy systems using machine learning techniques, including supervised, unsupervised, and reinforcement learning."

| Topic | File | Section |
|-------|------|---------|
| **Supervised Learning** | | |
| Regression for consumption | Part II | Chapter 10.1: Energy Consumption Prediction |
| Classification for faults | Part II | Chapter 10.2: Fault Detection |
| Feature importance (SHAP) | Part II | Chapter 10.3: Interpretability |
| Scikit-learn pipelines | Part IV | Chapter 16.3: create_heating_demand_pipeline() |
| **Unsupervised Learning** | | |
| Building clustering | Part II | Chapter 11.1: Portfolio clustering |
| Dimensionality reduction | Part II | Chapter 11.2: PCA, UMAP |
| Regime identification | Part II | Chapter 11.3: HMM, change point detection |
| Anomaly detection | Part II | Chapter 8.2: Isolation Forest, autoencoders |
| **Reinforcement Learning** | | |
| State/action/reward design | Part II | Chapter 9.3: RL for HVAC |
| Multi-objective optimization | Part II | Chapter 9.4: Pareto optimization |

---

## Requirements Mapping

### Requirement 1: Full Product Lifecycle Experience
> "You are familiar with full product lifecycles — from feasibility studies and requirement engineering to production-ready tool development, code reviews, feature deployments, and ongoing maintenance and improvement."

| Topic | File | Section |
|-------|------|---------|
| Requirements engineering | Part V | Chapter 20.2: translate_customer_requirement() |
| Code review practices | Part III | Chapter 13.3: Code review checklist |
| Testing strategies | Part III | Chapter 13.2: Unit, integration, property-based |
| Deployment patterns | Part III | Chapter 15: Batch vs. real-time, edge |
| Model monitoring | Part III | Chapter 14.4: Drift detection, performance monitoring |
| System design | Part V | Chapter 19: Complete chapter |

---

### Requirement 2: Statistics, Data Modeling, ML Skills
> "You bring strong skills in statistics, data modeling, data analysis, and machine learning."

| Topic | File | Section |
|-------|------|---------|
| Statistical methods | Part II | Chapter 8.1: Statistical anomaly detection |
| Thermal modeling | Part IV | Chapter 16.2: fit_building_thermal_model() |
| ML model comparison | Part II | Chapter 10.1: Model comparison code |
| Hyperparameter tuning | Part IV | Chapter 16.3: tune_pipeline_hyperparameters() |
| Time series modeling | Part II | Chapter 7: Complete chapter |

---

### Requirement 3: Engineering/Physics Background with Energy Foundation
> "You have an educational background in electrical engineering, mechanical engineering, physics, computer science, data science, or mathematics — with a solid foundation in energy technologies."

| Topic | File | Section |
|-------|------|---------|
| Thermodynamics | Part I | Chapter 1: Heat transfer, thermal mass |
| Heating system types | Part I | Chapter 2: Gas, district, heat pump, CHP |
| Heat pump physics (COP, Carnot) | Part I | Chapter 2.3: COP equations |
| Building energy balance | Part I | Chapter 1.3: Heat load calculation |
| Control theory basics | Part I | Chapter 3: Control variables |
| Hydraulics | Part I | Chapter 4: Hydraulic balancing |

---

### Requirement 4: Prediction Models and Energy Time Series
> "You have expertise in developing prediction models and working with energy time series data."

| Topic | File | Section |
|-------|------|---------|
| Time series characteristics | Part II | Chapter 6.1: Seasonality, trend, autocorrelation |
| Resampling/interpolation | Part II | Chapter 6.2: Physics-aware aggregation |
| Forecasting methods | Part II | Chapter 7: ARIMA to deep learning |
| Feature engineering | Part II | Chapter 6.3: Lag, rolling, cyclical |
| Domain-specific features | Part IV | Chapter 16.3: Custom transformers |

---

### Requirement 5: Python, SQL, GraphQL, REST, Data Science Libraries
> "You are proficient in Python, SQL, GraphQL, and REST, and you work confidently with data science libraries like Pandas, SciPy, and Scikit-Learn."

| Topic | File | Section |
|-------|------|---------|
| **Python** | | |
| Pandas time series | Part IV | Chapter 16.1: DatetimeIndex, resampling |
| NumPy/SciPy | Part IV | Chapter 16.2: Signal processing, optimization |
| Scikit-learn pipelines | Part IV | Chapter 16.3: Pipelines, custom transformers |
| **SQL** | | |
| Window functions | Part IV | Chapter 17.1: Rolling averages, lag |
| Time series queries | Part IV | Chapter 17.1: HDD calculation, aggregations |
| **GraphQL** | | |
| Schema design | Part IV | Chapter 17.2: Building hierarchy schema |
| Python client | Part IV | Chapter 17.2: EnergyDataClient |
| **REST** | | |
| FastAPI design | Part IV | Chapter 17.3: Endpoints, models |
| Versioning/pagination | Part IV | Chapter 17.3: PaginatedResponse |

---

### Requirement 6: MLOps Experience (Plus)
> "Experience with Machine Learning Operations (MLOps) is a plus."

| Topic | File | Section |
|-------|------|---------|
| Experiment tracking | Part III | Chapter 14.1: MLflow integration |
| Model registry | Part III | Chapter 14.2: Model versioning |
| CI/CD for ML | Part III | Chapter 14.3: GitHub Actions |
| Data drift monitoring | Part III | Chapter 14.4: DataDriftMonitor |
| Model performance monitoring | Part III | Chapter 14.4: ModelPerformanceMonitor |

---

### Requirement 7: Version Control (Git)
> "You have hands-on experience with version control systems like Git and follow collaborative coding practices."

| Topic | File | Section |
|-------|------|---------|
| Branching strategy | Part III | Chapter 13.3: GitFlow variant |
| Commit conventions | Part III | Chapter 13.3: Commit message format |
| Code review | Part III | Chapter 13.3: Review checklist |

---

### Requirement 8: Testing and Quality Assurance
> "You are familiar with testing frameworks and quality assurance processes to ensure robust, reliable product features."

| Topic | File | Section |
|-------|------|---------|
| Unit testing (pytest) | Part III | Chapter 13.2: TestHeatingCurve |
| Integration testing | Part III | Chapter 13.2: TestOptimizationPipeline |
| Property-based testing | Part III | Chapter 13.2: Hypothesis examples |
| Test coverage | Part III | Chapter 14.3: CI workflow with coverage |

---

### Requirement 9: Clean, Maintainable Code
> "Your code is clean, well-structured, maintainable, and easy for others to understand and build upon."

| Topic | File | Section |
|-------|------|---------|
| Type hints | Part III | Chapter 13.1: Function signatures |
| Docstrings | Part III | Chapter 13.1: NumPy-style documentation |
| SOLID principles | Part III | Chapter 13.1: SRP, OCP, DI examples |
| Dataclasses | Part III | Chapter 13.1: BuildingConfig, OptimizationResult |

---

### Requirement 10: Cross-Functional Collaboration
> "You are comfortable collaborating and communicating effectively with energy engineers, developers (frontend and backend), and customer success managers."

| Topic | File | Section |
|-------|------|---------|
| Working with engineers | Part V | Chapter 20.1: Collaboration principles |
| Technical translation | Part V | Chapter 20.1: Bidirectional translation |
| API design for developers | Part IV | Chapter 17.2, 17.3: GraphQL, REST |
| Customer communication | Part V | Chapter 20.3: Executive summaries |
| Behavioral questions | Part V | Chapter 20.4: STAR responses |

---

### Requirement 11: Customer Needs Translation
> "You have a strong understanding of customer needs and know how to translate them into technical solutions."

| Topic | File | Section |
|-------|------|---------|
| Requirements process | Part V | Chapter 20.2: translate_customer_requirement() |
| Success criteria definition | Part V | Chapter 20.2: Measurable metrics |
| Technical approach planning | Part V | Chapter 20.2: Phase 1/Phase 2 structure |
| Milestone definition | Part V | Chapter 20.2: Project milestones |

---

## Domain Knowledge Quick Reference

### Heating System Types (Part I, Chapter 2)

| System | Key Metrics | Optimization Focus |
|--------|-------------|---------------------|
| Gas/Oil Boiler | Brennwertnutzung, cycling | Return temp < 55°C, cascade sequencing |
| District Heating | Anschlussleistung, Arbeitspreis | Peak shaving, return temp penalties |
| Heat Pump | COP (3-5 typical) | Minimize auxiliary heater, low flow temps |
| Hybrid | System COP | Prioritize high-efficiency source |
| CHP (BHKW) | Stromkennzahl | Heat-led operation, storage management |

### Control Parameters (Part I, Chapter 3)

| Parameter | German Term | Typical Range | Impact |
|-----------|-------------|---------------|--------|
| Heating curve slope | Heizkennlinie Steilheit | 0.5-2.0 | 1-2% per 0.1 change |
| Flow temperature | Vorlauftemperatur | 35-75°C | 1.5% per °C reduction |
| Return temperature | Rücklauftemperatur | 25-55°C | Condensing threshold: 55°C |
| Night setback | Nachtabsenkung | 2-5°C reduction | 5-10% savings |
| Storage setpoint | Speicher-Solltemperatur | 55-65°C | Legionella min: 60°C |

### Key Metrics from Green Fusion Data (Part V, Chapter 18)

| Metric | Value | Source |
|--------|-------|--------|
| Average Vorlauf at 4°C outdoor | 64.4°C | 800 systems analysis |
| Systems without night setback | 70% | 800 systems analysis |
| Systems with legionella risk | 10% | Circulation < 50°C |
| Heat-pump-ready without renovation | 17% | Vorlauf < 55°C at -5°C |
| Average savings potential | 16% | 1000+ optimized systems |
| Hydraulic balancing urgently needed | 17.5% | Data-driven assessment |

---

## Interview Preparation Checklist

### Technical Depth
- [ ] Explain COP and Carnot efficiency (Part I, 2.3)
- [ ] Describe heating curve optimization approach (Part I, 3.1)
- [ ] Walk through time series feature engineering (Part II, 6.3)
- [ ] Compare forecasting methods trade-offs (Part II, 7)
- [ ] Explain MPC vs. RL for control (Part II, 9.2-9.3)
- [ ] Design ML pipeline with sklearn (Part IV, 16.3)
- [ ] Write SQL window functions for energy analysis (Part IV, 17.1)

### System Design
- [ ] Architect 3000-building platform (Part V, 19.1)
- [ ] Design real-time anomaly detection (Part V, 19.2)
- [ ] Explain multi-tenant data isolation (Part V, 19.3)

### Domain Knowledge
- [ ] Describe all heating system types (Part I, 2)
- [ ] Explain hydraulic balancing Verfahren A vs B (Part I, 4)
- [ ] Discuss sector coupling challenges (Part I, 5)
- [ ] Reference German regulations: GEG §60b, §60c (References)

### Case Studies
- [ ] WSL Leipzig: district heating, 16.5% savings (Part V, 18.1)
- [ ] GWU Eckernförde: heat pump cascade, backup heater issue (Part V, 18.2)
- [ ] DIE EHRENFELDER: gas cascade, legacy digitalization (Part V, 18.3)

### Behavioral
- [ ] Collaboration with domain experts (Part V, 20.1)
- [ ] Translating customer requirements (Part V, 20.2)
- [ ] Communicating results to non-technical stakeholders (Part V, 20.3)
- [ ] STAR responses prepared (Part V, 20.4)

---

*Use this mapping to focus preparation on areas matching the job description priorities.*
