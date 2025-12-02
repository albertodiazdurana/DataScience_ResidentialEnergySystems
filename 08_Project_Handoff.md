# Project Handoff: Data Science for Residential Energy Systems

## Document Purpose
This handoff provides complete context for the Claude project, summarizing the research, analysis, and materials created during the initial preparation session. Use this as the authoritative reference for project context.

---

## 1. Project Origin

### Objective
Prepare for a Senior Data Scientist interview at **Green Fusion GmbH**, a Berlin-based cleantech startup specializing in AI-powered heating optimization for residential buildings in the German housing sector (Wohnungswirtschaft).

### Interview Focus Areas
- Domain expertise in heating systems and energy optimization
- Data science and ML for time series, forecasting, anomaly detection, control systems
- Production engineering and MLOps
- Cross-functional collaboration with energy engineers and stakeholders

---

## 2. Target Company: Green Fusion GmbH

### Company Profile
- **Founded**: 2021 by Paul Hock, Simon Wagenknecht, Nina Germanus
- **Location**: Berlin (Hohen Neuendorf), Germany
- **Funding**: €12M Series A (January 2025), led by HV Capital and XAnge
- **Market Position**: Market leader in heating monitoring and optimization per GdW (German housing industry association)
- **Scale**: 100+ housing company customers, 800,000+ apartments served, targeting 3,000 optimized buildings by end of 2025

### Core Product
- **Energiespar-Pilot / Energiespar-Autopilot**: Cloud-based AI platform for real-time heating system optimization
- **GreenBox**: Hardware gateway installed in building basements, connecting heating systems to cloud platform
- **Capabilities**: Monitoring, analysis, remote control, automated optimization
- **Results**: Average 16% heating cost/energy reduction

### Technology Approach
- Hardware-agnostic (works with any heating system manufacturer)
- Supports: gas boilers, oil boilers, district heating (Fernwärme), heat pumps, CHP (BHKW), hybrid systems, sector coupling (PV + heat pump + storage)
- Data sources: Anlegefühler (clamp-on sensors), meter integration (M-Bus, pulse), controller interfaces, cloud-to-cloud APIs (e.g., Viessmann partnership via API)
- Real-time and predictive optimization using weather data

### Strategic Partnerships
- **Viessmann Climate Solutions**: API-based integration for Viessmann heating systems
- **aedifion**: Partnership for commercial building optimization (extending beyond residential)

### Expansion Plans
- European expansion: France, Benelux, Austria, Italy (pilot projects)
- New unit focused on renewable energy systems integration (heat pumps, PV, batteries, EV charging)

---

## 3. Job Description

### Position: Senior Data Scientist (m/f/d) - Energy Tech Start Up

**Location**: Berlin, Germany

**Team**: Energy Optimization Team

**Role Summary**: Develop production-ready algorithms that optimize heating system operations, requiring both data science expertise and understanding of heating systems/control technology.

### Tasks
1. Clean and analyze data to identify patterns and trends, uncovering insights that drive solutions
2. Apply statistical techniques to interpret data, ensuring reliability and accuracy of findings
3. Build data models to predict heating system behavior and patterns using advanced analytics and machine learning
4. Develop production-ready algorithms and data pipelines to optimize energy system components, reduce CO₂ emissions, and enhance energy efficiency
5. Responsible for full development cycle of product features — from understanding customer requirements to final deployment — collaborating with energy engineers, frontend/backend developers, product and customer success managers
6. Analyze experimental data to refine and improve energy optimization algorithms
7. Present findings in a clear, concise, and understandable way
8. Support the team in creating data models for predicting energy time series data (heat demand, solar production, electricity consumption) and optimizing energy systems using ML techniques including supervised, unsupervised, and reinforcement learning

### Requirements
1. Familiar with full product lifecycles — feasibility studies, requirement engineering, production-ready tool development, code reviews, feature deployments, ongoing maintenance
2. Strong skills in statistics, data modeling, data analysis, and machine learning
3. Educational background in electrical engineering, mechanical engineering, physics, computer science, data science, or mathematics — with solid foundation in energy technologies
4. Expertise in developing prediction models and working with energy time series data
5. Proficient in Python, SQL, GraphQL, and REST; confident with Pandas, SciPy, Scikit-Learn
6. MLOps experience is a plus
7. Hands-on experience with Git and collaborative coding practices
8. Familiar with testing frameworks and quality assurance processes
9. Code is clean, well-structured, maintainable, and easy for others to understand
10. Comfortable collaborating and communicating with energy engineers, developers, and customer success managers
11. Strong understanding of customer needs and ability to translate them into technical solutions

---

## 4. Source Materials Used

### 4.1 Green Fusion Case Studies

**Case Study 1: dhu Hamburg (KfW 70 Neubau)**
- Building type: New construction, KfW 70 energy standard
- Heating: District heating (Fernwärme), Hamburger Energiewerke
- Configuration: 18 apartments, separate controllers for heating circuit and DHW
- Challenge: Integrating separate regulators for holistic optimization
- Interventions: Optimized Vorlauf/Rücklauf temperatures, hysteresis, storage setpoint, combined heating and DHW optimization
- Result: ~8% energy savings (approx. 5,000 kWh absolute)
- Source: KEDi (Kompetenzzentrum Energieeffizienz durch Digitalisierung)

**Case Study 2: GWU Eckernförde (Wärmepumpenkaskade)**
- Building: 1972 construction, renovated 2022-23, 16 units, 1,072 m²
- Heating: Two Stiebel Eltron heat pumps with PV integration
- Challenge: Higher than expected electricity consumption; needed to optimize complex hydraulic system
- Interventions: Comprehensive data collection via GreenBox, identified Durchlauferhitzer running excessively, reduced Vorlauf temperature, implemented night setback, optimized heating curve
- Result: 20% reduction in DHW electricity, 15% total system savings expected
- Key insight: "Hybridanlagen können ohne aktive Steuerung nicht effizient betrieben werden"

**Case Study 3: DIE EHRENFELDER (Gaskesselkaskade)**
- Building: 1984/1987 construction, >7,000 m² net floor area
- Heating: Gas boiler cascade with DHW storage, no digital interfaces
- Challenge: No existing digitalization, boilers on factory settings, all running simultaneously even in summer
- Interventions: Installed sensors and gateway, optimized cascade sequencing, reduced DHW storage temp, adjusted heating curve, implemented night setback, improved condensing operation
- Result: Substantial DHW savings, rolling out to 23 additional buildings (gas, pellet, hybrid)

**Case Study 4: WSL Wohnen & Service Leipzig**
- Building: 1950s construction, 27 units, 1,062 m²
- Heating: 30-year-old district heating (90 kW, Samson Trovis controller)
- Challenge: Legacy system with no digital connectivity, high consumption
- Context: Part of EU SPARCS research project
- Interventions: Installed GreenBox, integrated via Vodafone API, dynamic heating curve control, automated summer/winter switching
- Result: 16.5% consumption reduction after 3 months
- Measurement period: April-July 2023

### 4.2 Green Fusion Blog Posts

**"Von Gasheizung bis Wärmepumpe: Heizungsoptimierung im Überblick"**
- Comprehensive overview of optimization approach across heating types
- Digitalization process: sensors (Anlegefühler), meters, controller interfaces, APIs
- Digital twin concept and monitoring capabilities
- Optimization parameters: Heizkennlinie, hysteresis, Taktverhalten, night setback, summer mode, DHW

**"Sektorkopplung: Das Was, Wie und Warum"**
- Sector coupling: integrating electricity, heat, and mobility
- Heat pump COP: 3-5 (3-4x energy output vs. electrical input)
- Temporal mismatch: peak demand (morning/evening) vs. PV production (midday)
- Self-consumption optimization strategies
- Dynamic electricity pricing integration

**"Effiziente Steuerung von hybriden Heizungsanlagen"**
- OSTLAND Wohnungsgenossenschaft case
- Heat pump + gas peak load boiler hybrids (~66% heat pump share)
- Importance of active control for hybrid efficiency
- Early fault detection via monitoring

**"Energieeffizienz jetzt auch für gemischte Portfolios"**
- Partnership with aedifion for commercial buildings
- 22% average savings in commercial buildings
- TÜV certification per §71a GEG

**"5 %, 16 % oder 42 %? Wie groß ist das Potenzial zur Kostenreduzierung?"**
- Savings depend on baseline state
- KfW-70 new build: 8% (already efficient)
- Typical existing building: 18%
- Poorly configured old building: up to 42%
- Average across all systems: 16%
- Energy savings vs. cost savings (includes emission fees, maintenance reduction)

**"Was die Daten über unsere Heizsysteme verraten"**
- Analysis of 800 digitalized heating systems
- Key findings:
  - Average Vorlauf at 4°C outdoor: 64.4°C (too high)
  - 17% of buildings heat-pump-ready without renovation (Vorlauf < 55°C at -5°C)
  - 70% of systems without night setback
  - 20% with DHW storage temp > 65°C (unnecessary)
  - 10% with legionella risk (circulation < 50°C)
  - Only 17.5% urgently need hydraulic balancing; 43% don't need it at all

**"Hydraulischer Abgleich: Pflicht, Sinn und Verfahren"**
- EnSimiMaV expired September 2024; GEG now governs
- Verfahren A (simplified): unreliable, uses tabulated assumptions
- Verfahren B (detailed): room-by-room heat load calculation per DIN EN 12831, mandatory for new/modernized systems since 2023
- Green Fusion approach: digitalize first, analyze data, then target balancing where data indicates need
- Less than 25% of companies met EnSimiMaV deadlines (per VDIV)

**"Fernwärme - So reduzieren sie Anschluss- und Verbrauchskosten"**
- Cost structure: Grundpreis (based on Anschlussleistung) + Arbeitspreis (per kWh)
- Return temperature penalties (typically max 50-60°C)
- Optimization strategies: reduce actual peak load, avoid simultaneous heating/DHW peaks (peak shifting), maintain return temp compliance
- Typical savings: ~15%

### 4.3 External Sources (Web Search)

**Funding and Company News:**
- EU-Startups (January 2025): €12M Series A details
- Startbase (January 2025): Growth plans, 300% target
- TechFundingNews (January 2025): European expansion
- Reason-Why Berlin: Product details

**Partnerships:**
- Viessmann Climate Solutions (July 2024): Strategic partnership announcement, API integration

**Investor Information:**
- Vireo Ventures: Technology advantage description
- Brandenburg Kapital: Seed funding context

---

## 5. Study Guide Created

### Structure
A comprehensive 7-part study guide (~22,000 words) was created covering all aspects of the job description.

### Files Generated

| File | Content | Word Count |
|------|---------|------------|
| `00_TOC.md` | Table of Contents for all 20 chapters | ~300 |
| `01_Part_I_Domain_Fundamentals.md` | Chapters 1-5: Thermodynamics, heating system types, control variables, hydraulic balancing, sector coupling | ~4,800 |
| `02_Part_II_Data_Science_ML.md` | Chapters 6-11: Time series fundamentals, forecasting, anomaly detection, control algorithms, supervised/unsupervised learning | ~6,200 |
| `03_Part_III_Production_MLOps.md` | Chapters 12-15: Data pipelines, production code quality, MLOps, deployment patterns | ~4,200 |
| `04_Part_IV_Technical_Stack.md` | Chapters 16-17: Python (Pandas, NumPy, SciPy, Scikit-learn), SQL, GraphQL, REST APIs | ~3,800 |
| `05_Part_V_Interview_Scenarios.md` | Chapters 18-20: Case study walkthroughs, system design questions, behavioral/cross-functional collaboration | ~4,500 |
| `06_References.md` | German regulations, academic sources, library documentation, German-English glossary | ~1,500 |
| `07_Job_Description_Mapping.md` | Maps each job requirement/task to specific study guide sections | ~1,200 |

### Chapter Overview

**Part I: Domain Fundamentals**
1. Thermodynamic Principles (heat transfer, thermal mass, degree-days)
2. Heating System Types (gas, oil, Fernwärme, heat pumps, CHP, hybrids)
3. Key Control Variables (Heizkennlinie, Vorlauf/Rücklauf, hysteresis, setpoints)
4. Hydraulic Balancing (Verfahren A vs B, data-driven assessment)
5. Sector Coupling (PV + heat pump orchestration, dynamic pricing)

**Part II: Data Science & ML**
6. Time Series Fundamentals (seasonality, resampling, feature engineering)
7. Forecasting (ARIMA, gradient boosting, LSTM, weather integration)
8. Anomaly Detection (statistical, ML-based, domain-specific)
9. Control & Optimization (rule-based, MPC, reinforcement learning)
10. Supervised Learning (regression, classification, interpretability)
11. Unsupervised Learning (clustering, dimensionality reduction, regimes)

**Part III: Production Engineering & MLOps**
12. Data Pipelines (MQTT, REST, cloud-to-cloud, TimescaleDB/InfluxDB)
13. Production Code (type hints, SOLID, testing strategies)
14. MLOps (MLflow, model registry, CI/CD, drift monitoring)
15. Deployment (batch vs real-time, edge, A/B testing, gradual rollout)

**Part IV: Technical Stack**
16. Python (Pandas time series, NumPy/SciPy optimization, Scikit-learn pipelines)
17. Data Access (SQL window functions, GraphQL schemas, REST API design)

**Part V: Interview Scenarios**
18. Case Study Walkthroughs (WSL Leipzig, GWU Eckernförde, DIE EHRENFELDER)
19. System Design (3000-building platform, anomaly detection, multi-tenant)
20. Behavioral & Collaboration (energy engineers, requirements, communication)

---

## 6. Key Technical Concepts

### Domain Metrics (Memorize)

| Metric | Value | Context |
|--------|-------|---------|
| Average Vorlauf at 4°C outdoor | 64.4°C | Too high; indicates optimization potential |
| Systems without night setback | 70% | Quick win opportunity |
| Average savings from optimization | 16% | Green Fusion benchmark |
| Heat pump COP range | 3-5 | 3-5x electrical input |
| Condensing threshold (gas) | Return < 55°C | Required for Brennwertnutzung |
| Heat-pump-ready buildings | 17% | Without renovation |
| Legionella risk threshold | Circulation < 50°C | 10% of systems |
| Hydraulic balancing urgent | 17.5% | Data-driven assessment |

### German Terms (Essential)

| German | English | Technical Context |
|--------|---------|-------------------|
| Heizkennlinie | Heating curve | Flow temp = f(outdoor temp) |
| Vorlauftemperatur | Flow temperature | Supply to heating circuits |
| Rücklauftemperatur | Return temperature | Back to heat source |
| Spreizung | Temperature spread | Vorlauf - Rücklauf |
| Anschlussleistung | Connection power | Fernwärme capacity charge |
| Brennwertnutzung | Condensing operation | Latent heat recovery |
| Hydraulischer Abgleich | Hydraulic balancing | Flow rate optimization |
| Nachtabsenkung | Night setback | Reduced heating at night |
| Fernwärme | District heating | Centralized heat network |
| Wärmepumpe | Heat pump | COP-based heating |

### Regulatory Context

| Regulation | Relevance |
|------------|-----------|
| GEG §60b | Mandatory heating inspection and optimization |
| GEG §60c | Hydraulic balancing requirements for new/modernized |
| GEG §71a | General heating system requirements; TÜV certification |
| DIN EN 12831 | Heat load calculation standard (Verfahren B) |
| EnSimiMaV | Expired Sept 2024; historical context |

---

## 7. Interview Preparation Priorities

### High Priority (Core Role)
1. **Heating curve optimization** - Explain Heizkennlinie, slope/shift adjustments
2. **Time series forecasting** - Heat demand prediction, weather integration
3. **Production ML pipelines** - Scikit-learn, testing, deployment
4. **Case study analysis** - Walk through WSL Leipzig or GWU Eckernförde

### Medium Priority (Differentiators)
5. **Control algorithms** - MPC basics, RL for HVAC conceptually
6. **System design** - Platform architecture for building portfolio
7. **Anomaly detection** - Statistical + ML approaches, domain-specific

### Supporting (Demonstrate Breadth)
8. **MLOps practices** - MLflow, monitoring, CI/CD
9. **Cross-functional collaboration** - Engineer communication, requirements
10. **German regulatory context** - GEG awareness

---

## 8. Recommended Project Usage

### Conversation Starters

**Concept Review:**
- "Explain [Heizkennlinie/COP/hydraulic balancing] as I would in an interview"
- "What's the relationship between return temperature and condensing operation?"

**Technical Practice:**
- "Write Python code to [detect anomalies in heating data / optimize heating curve / calculate COP]"
- "How would I design a forecasting pipeline for heat demand?"

**Interview Prep:**
- "Quiz me on [Part I domain concepts / ML techniques / system design]"
- "How should I answer: 'Describe a time you worked with domain experts'?"
- "What questions should I ask the interviewer about Green Fusion's tech stack?"

**Case Study Practice:**
- "Walk me through the WSL Leipzig optimization as if I'm presenting to a customer"
- "What would you look for first when diagnosing high consumption in a heat pump system?"

---

## 9. Files to Upload to Project

### Required (Core Reference)
1. This handoff document (`08_Project_Handoff.md`)
2. `07_Job_Description_Mapping.md`
3. `00_TOC.md`
4. `06_References.md`

### Recommended (Full Study Guide)
5. `01_Part_I_Domain_Fundamentals.md`
6. `02_Part_II_Data_Science_ML.md`
7. `03_Part_III_Production_MLOps.md`
8. `04_Part_IV_Technical_Stack.md`
9. `05_Part_V_Interview_Scenarios.md`

---

## 10. Session Summary

### What Was Accomplished
1. Researched Green Fusion GmbH via web search (funding, partnerships, product details)
2. Analyzed job description and mapped to data science competencies
3. Reviewed 4 detailed case studies provided by user
4. Reviewed 8 technical blog posts from Green Fusion website
5. Created comprehensive 20-chapter study guide (~22,000 words)
6. Created job description to study guide mapping
7. Prepared project setup instructions
8. Created this handoff document

### Quality Standards Applied
- All temperatures in Celsius
- German technical terms retained with English explanations
- Python code examples throughout
- Domain-specific numerical examples (actual Green Fusion metrics)
- Production-quality code patterns (type hints, docstrings, testing)
- Interview-focused structure with behavioral preparation

---

*Document created: January 2025*
*For: Senior Data Scientist Interview Preparation - Green Fusion GmbH*
