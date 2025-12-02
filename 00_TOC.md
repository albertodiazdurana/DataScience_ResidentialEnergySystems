# Senior Data Scientist Study Guide: Energy Tech & Heating Optimization

## Green Fusion GmbH - Interview Preparation

---

## Table of Contents

### Part I: Domain Fundamentals - Heating Systems & Energy Technology

**Chapter 1: Thermodynamic Principles for Heating Systems**
- Heat transfer modes: conduction, convection, radiation
- Thermal mass and building inertia
- Degree-day calculations and heating load estimation

**Chapter 2: Heating System Types & Control Parameters**
- Gas/oil boilers: condensing technology, Brennwertnutzung
- District heating (Fernwärme): Anschlussleistung, return temperature penalties, Spreizung
- Heat pumps: COP, Carnot efficiency, source types
- CHP (BHKW): electrical/thermal efficiency, Stromkennzahl
- Hybrid and multivalent systems

**Chapter 3: Key Control Variables**
- Heizkennlinie (heating curve): slope, parallel shift, outdoor temperature dependency
- Vorlauf-/Rücklauftemperatur (flow/return temperatures)
- Hysteresis and Taktverhalten (cycling behavior)
- Speicher-Solltemperatur (storage setpoint)
- Night setback and summer mode switching

**Chapter 4: Hydraulic Balancing (Hydraulischer Abgleich)**
- Verfahren A vs. Verfahren B
- Room-by-room heat load calculation (DIN EN 12831)
- Data-driven assessment of balancing necessity

**Chapter 5: Sector Coupling (Sektorkopplung)**
- PV + heat pump + battery orchestration
- Self-consumption maximization
- Dynamic electricity pricing integration
- Temporal mismatch problem

---

### Part II: Data Science & Machine Learning for Energy Systems

**Chapter 6: Time Series Fundamentals for Energy Data**
- Characteristics: seasonality, trend, autocorrelation, non-stationarity
- Resampling, interpolation, handling missing sensor data
- Feature engineering: lag features, rolling statistics, Fourier terms

**Chapter 7: Forecasting Heat Demand & Energy Production**
- Classical methods: ARIMA, SARIMA, exponential smoothing
- ML approaches: gradient boosting, random forests
- Deep learning: LSTM, Transformer-based models
- Weather data integration

**Chapter 8: Anomaly Detection in Heating Systems**
- Statistical methods: z-score, IQR, Grubbs' test
- ML methods: Isolation Forest, One-Class SVM, autoencoders
- Domain-specific anomalies: legionella risk, excessive cycling, return temperature violations

**Chapter 9: Control & Optimization Algorithms**
- Rule-based control vs. model predictive control (MPC)
- Reinforcement learning for HVAC: state/action/reward formulation
- Multi-objective optimization: comfort vs. cost vs. emissions
- Peak shaving and load shifting strategies

**Chapter 10: Supervised Learning Applications**
- Regression: predicting energy consumption, COP estimation
- Classification: fault detection, maintenance prediction
- Feature importance for interpretability

**Chapter 11: Unsupervised Learning Applications**
- Clustering building portfolios by consumption patterns
- Dimensionality reduction for sensor data
- Identifying operational regimes

---

### Part III: Production Engineering & MLOps

**Chapter 12: Data Pipelines for IoT/Energy Systems**
- Ingestion: MQTT, REST APIs, cloud-to-cloud integration
- Storage: time-series databases (InfluxDB, TimescaleDB)
- ETL patterns for sensor data at scale

**Chapter 13: Production-Ready Algorithm Development**
- Code quality: type hints, docstrings, SOLID principles
- Testing: unit tests, integration tests, property-based testing
- Version control workflows: branching strategies, code review

**Chapter 14: MLOps Fundamentals**
- Experiment tracking (MLflow, Weights & Biases)
- Model versioning and registry
- CI/CD for ML pipelines
- Monitoring: data drift, model performance degradation

**Chapter 15: Deployment Patterns**
- Batch inference vs. real-time scoring
- Edge deployment considerations
- A/B testing and gradual rollout

---

### Part IV: Technical Stack Deep Dive

**Chapter 16: Python for Energy Data Science**
- Pandas: time-indexed DataFrames, resampling, window functions
- NumPy/SciPy: signal processing, optimization
- Scikit-learn: pipelines, cross-validation, hyperparameter tuning

**Chapter 17: Data Access Patterns**
- SQL: window functions for time series, aggregations
- GraphQL: schema design for hierarchical data
- REST API design: versioning, pagination, error handling

---

### Part V: Interview Preparation - Applied Scenarios

**Chapter 18: Case Study Walkthroughs**
- District heating optimization (WSL Leipzig)
- Heat pump cascade (GWU Eckernförde)
- Gas boiler cascade (DIE EHRENFELDER)

**Chapter 19: System Design Questions**
- Energy management platform for 3,000 buildings
- Real-time anomaly detection pipeline
- Multi-tenant data architecture

**Chapter 20: Behavioral & Cross-Functional Collaboration**
- Working with energy engineers
- Translating customer requirements to technical specifications
- Communicating ML results to non-technical stakeholders

---

### References

- Academic sources and textbooks
- German regulations (GEG, EnSimiMaV)
- Industry standards and further reading

---

*Document prepared for Senior Data Scientist interview at Green Fusion GmbH, Berlin*
