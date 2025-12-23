# References

---

## German Regulations and Standards

### Gebäudeenergiegesetz (GEG)
- **§60b GEG**: Heizungsprüfung und Heizungsoptimierung - Mandatory heating system inspection and optimization requirements
- **§60c GEG**: Hydraulischer Abgleich - Requirements for hydraulic balancing in new and modernized systems
- **§71a GEG**: Anforderungen an Heizungsanlagen - General heating system requirements
- Full text available at: https://www.geg-info.de/geg_2024/

### EnSimiMaV (Energiesicherungsmaßnahmenverordnung)
- Short-term energy security measures (expired September 2024)
- Historical context for hydraulic balancing requirements
- Superseded by GEG second amendment

### DIN Standards
- **DIN EN 12831**: Heating systems in buildings - Method for calculation of the design heat load
- **DIN EN 15232**: Energy performance of buildings - Impact of Building Automation, Controls and Building Management
- **DIN V 18599**: Energy assessment of buildings

---

## Technical References

### Thermodynamics and Heat Transfer
- Incropera, F.P., DeWitt, D.P., Bergman, T.L., Lavine, A.S. (2006). *Fundamentals of Heat and Mass Transfer*. 6th Edition. Wiley.
- Recknagel, Sprenger, Schramek (2018). *Taschenbuch für Heizung und Klimatechnik*. 79th Edition. DIV Deutscher Industrieverlag. [German HVAC standard reference]

### Heat Pump Technology
- Staffell, I., et al. (2012). "A review of domestic heat pumps." *Energy & Environmental Science*, 5(11), 9291-9306.
- Fischer, D., Madani, H. (2017). "On heat pumps in smart grids: A review." *Renewable and Sustainable Energy Reviews*, 70, 342-357.

### Building Energy Modeling
- Coakley, D., Raftery, P., Keane, M. (2014). "A review of methods to match building energy simulation models to measured data." *Renewable and Sustainable Energy Reviews*, 37, 123-141.
- Li, X., Wen, J. (2014). "Review of building energy modeling for control and operation." *Renewable and Sustainable Energy Reviews*, 37, 517-537.

---

## Data Science and Machine Learning

### Time Series Analysis
- Hyndman, R.J., Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*. 3rd Edition. OTexts. Available online: https://otexts.com/fpp3/
- Box, G.E.P., Jenkins, G.M., Reinsel, G.C., Ljung, G.M. (2015). *Time Series Analysis: Forecasting and Control*. 5th Edition. Wiley.

### Machine Learning for Energy Systems
- Amasyali, K., El-Gohary, N.M. (2018). "A review of data-driven building energy consumption prediction studies." *Renewable and Sustainable Energy Reviews*, 81, 1192-1205.
- Zhao, H.X., Magoulès, F. (2012). "A review on the prediction of building energy consumption." *Renewable and Sustainable Energy Reviews*, 16(6), 3586-3592.

### Reinforcement Learning for HVAC
- Wang, Z., Hong, T. (2020). "Reinforcement learning for building controls: The opportunities and challenges." *Applied Energy*, 269, 115036.
- Zhang, Z., Lam, K.P. (2018). "Practical implementation and evaluation of deep reinforcement learning control for a radiant heating system." *Proceedings of the 5th Conference on Systems for Built Environments*.

### Anomaly Detection
- Chandola, V., Banerjee, A., Kumar, V. (2009). "Anomaly detection: A survey." *ACM Computing Surveys*, 41(3), 1-58.
- Himeur, Y., et al. (2021). "Artificial intelligence based anomaly detection of energy consumption in buildings: A review, current trends and new perspectives." *Applied Energy*, 287, 116601.

---

## MLOps and Production Systems

### MLOps Practices
- Kreuzberger, D., Kühl, N., Hirschl, S. (2023). "Machine Learning Operations (MLOps): Overview, Definition, and Architecture." *IEEE Access*, 11, 31866-31879.
- Sculley, D., et al. (2015). "Hidden technical debt in machine learning systems." *Advances in Neural Information Processing Systems*, 28.

### Time-Series Databases
- TimescaleDB Documentation: https://docs.timescale.com/
- InfluxDB Documentation: https://docs.influxdata.com/

---

## Industry Resources

### Green Fusion Publications
- "Die Dekarbonisierung der Wohnungswirtschaft in Zahlen" - Joint publication with Ampeers Energy analyzing 800 heating systems
- Case studies available at: https://www.green-fusion.de/case-studies/
- Technical blog posts: https://www.green-fusion.de/blog/

### German Housing Industry
- GdW Bundesverband deutscher Wohnungs- und Immobilienunternehmen: https://www.gdw.de/
- KEDi (Kompetenzzentrum Energieeffizienz durch Digitalisierung): https://www.kedi-dena.de/

### Energy Data Sources
- Deutscher Wetterdienst (DWD) Open Data: https://opendata.dwd.de/
- SMARD Strommarktdaten: https://www.smard.de/

---

## Python Libraries Documentation

### Data Processing
- Pandas: https://pandas.pydata.org/docs/
- NumPy: https://numpy.org/doc/
- SciPy: https://docs.scipy.org/doc/scipy/

### Machine Learning
- Scikit-learn: https://scikit-learn.org/stable/documentation.html
- LightGBM: https://lightgbm.readthedocs.io/
- XGBoost: https://xgboost.readthedocs.io/

### Deep Learning
- TensorFlow/Keras: https://www.tensorflow.org/guide
- PyTorch: https://pytorch.org/docs/

### MLOps Tools
- MLflow: https://mlflow.org/docs/latest/index.html
- Weights & Biases: https://docs.wandb.ai/

### API Development
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/

---

## Online Courses and Tutorials

### Energy Systems
- edX: "Sustainable Energy" (MIT) - Fundamentals of energy systems
- Coursera: "Solar Energy" (TU Delft) - Renewable energy integration

### Time Series and Forecasting
- Coursera: "Sequences, Time Series and Prediction" (DeepLearning.AI)
- DataCamp: "Time Series Analysis in Python"

### MLOps
- Coursera: "Machine Learning Engineering for Production (MLOps)" (DeepLearning.AI)
- Full Stack Deep Learning: https://fullstackdeeplearning.com/

---

## Glossary of German Terms

| German Term | English Translation | Technical Context |
|-------------|---------------------|-------------------|
| Anlegefühler | Clamp-on temperature sensor | Non-invasive pipe temperature measurement |
| Anschlussleistung | Connection power | Contracted maximum power for district heating |
| Arbeitspreis | Consumption price | Per-kWh charge in energy contracts |
| Brennwertnutzung | Condensing operation | Recovering latent heat in flue gases |
| Durchlauferhitzer | Instantaneous water heater | Electric backup for DHW |
| Fernwärme | District heating | Centralized heat distribution network |
| Grundpreis | Base price | Fixed charge based on connection capacity |
| Heizkennlinie | Heating curve | Flow temp as function of outdoor temp |
| Heizkreis | Heating circuit | Hydronic distribution loop |
| Hydraulischer Abgleich | Hydraulic balancing | Flow rate optimization across circuits |
| Hysterese | Hysteresis | Temperature band for on/off control |
| Kesselfolgeschaltung | Boiler sequencing | Cascade control for multiple boilers |
| Nachtabsenkung | Night setback | Reduced heating during unoccupied hours |
| Pufferspeicher | Buffer tank | Thermal energy storage |
| Rücklauftemperatur | Return temperature | Water temp returning to heat source |
| Sektorkopplung | Sector coupling | Integration of electricity and heat sectors |
| Sommerbetrieb | Summer mode | DHW-only operation, space heating disabled |
| Speicher-Solltemperatur | Storage setpoint | Target temperature for thermal storage |
| Spreizung | Temperature spread | Difference between flow and return temps |
| Taktverhalten | Cycling behavior | On/off frequency of heating equipment |
| Vorlauftemperatur | Flow temperature | Water temp leaving heat source |
| Wärmemengenzähler | Heat meter | Measures thermal energy delivered |
| Wärmepumpe | Heat pump | Device transferring heat from cold to hot reservoir |

---

*Document prepared for Senior Data Scientist interview at Green Fusion GmbH, Berlin*

*Last updated: January 2025*
