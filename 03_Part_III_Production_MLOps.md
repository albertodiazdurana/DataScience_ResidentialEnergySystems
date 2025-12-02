# Part III: Production Engineering & MLOps

---

## Chapter 12: Data Pipelines for IoT/Energy Systems

Production energy management systems require robust data infrastructure handling continuous sensor streams from thousands of buildings. This chapter covers the architectural patterns and technologies for building scalable data pipelines.

### 12.1 Data Ingestion Patterns

Green Fusion's GreenBox gateway connects heating systems to the cloud platform. Multiple ingestion patterns accommodate diverse equipment and connectivity scenarios.

**MQTT (Message Queuing Telemetry Transport)** is the dominant IoT protocol for sensor data:

```python
import paho.mqtt.client as mqtt
import json
from datetime import datetime

class SensorDataIngester:
    """MQTT client for ingesting sensor data from GreenBox devices."""
    
    def __init__(self, broker_host, broker_port, topic_prefix):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.topic_prefix = topic_prefix
        self.broker_host = broker_host
        self.broker_port = broker_port
        
    def _on_connect(self, client, userdata, flags, rc):
        # Subscribe to all building sensors
        client.subscribe(f"{self.topic_prefix}/+/sensors/#")
        
    def _on_message(self, client, userdata, msg):
        """Process incoming sensor message."""
        try:
            payload = json.loads(msg.payload.decode())
            
            # Extract building_id and sensor_id from topic
            # Topic format: greenbox/{building_id}/sensors/{sensor_type}
            parts = msg.topic.split('/')
            building_id = parts[1]
            sensor_type = parts[3]
            
            record = {
                'timestamp': datetime.utcnow().isoformat(),
                'building_id': building_id,
                'sensor_type': sensor_type,
                'value': payload['value'],
                'unit': payload.get('unit'),
                'quality': payload.get('quality', 'good')
            }
            
            self._write_to_buffer(record)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def _write_to_buffer(self, record):
        """Buffer records for batch writing to database."""
        # Implementation depends on chosen buffering strategy
        pass
    
    def start(self):
        self.client.connect(self.broker_host, self.broker_port, 60)
        self.client.loop_forever()
```

**Message structure** considerations:

```python
# Recommended sensor message schema
sensor_message = {
    "timestamp": "2025-01-15T14:30:00Z",  # ISO 8601 UTC
    "device_id": "greenbox-abc123",
    "readings": [
        {
            "sensor_id": "vorlauf_temp_hk1",
            "value": 52.3,
            "unit": "degC",
            "quality": "good"  # good, uncertain, bad
        },
        {
            "sensor_id": "ruecklauf_temp_hk1", 
            "value": 38.7,
            "unit": "degC",
            "quality": "good"
        }
    ],
    "metadata": {
        "firmware_version": "2.1.4",
        "signal_strength": -67
    }
}
```

**REST API ingestion** for systems with HTTP connectivity:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class SensorReading(BaseModel):
    sensor_id: str
    value: float
    unit: str
    quality: str = "good"
    
class DevicePayload(BaseModel):
    device_id: str
    timestamp: datetime
    readings: List[SensorReading]

@app.post("/api/v1/ingest")
async def ingest_readings(payload: DevicePayload):
    """Ingest sensor readings from device."""
    try:
        # Validate device registration
        if not await device_registry.exists(payload.device_id):
            raise HTTPException(status_code=404, detail="Device not registered")
        
        # Write to time-series database
        await tsdb.write_batch(
            device_id=payload.device_id,
            timestamp=payload.timestamp,
            readings=payload.readings
        )
        
        return {"status": "accepted", "readings_count": len(payload.readings)}
        
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail="Ingestion failed")
```

**Cloud-to-cloud API integration** (e.g., Viessmann partnership):

```python
import httpx
from typing import AsyncGenerator

class ViessmannAPIClient:
    """Client for Viessmann Cloud API integration."""
    
    def __init__(self, client_id: str, client_secret: str):
        self.base_url = "https://api.viessmann.com/iot/v1"
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = None
        
    async def _authenticate(self):
        """Obtain OAuth2 access token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://iam.viessmann.com/idp/v2/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )
            self._token = response.json()["access_token"]
    
    async def get_device_data(self, installation_id: str, 
                               gateway_serial: str) -> dict:
        """Fetch current device data from Viessmann API."""
        if not self._token:
            await self._authenticate()
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/equipment/installations/{installation_id}"
                f"/gateways/{gateway_serial}/devices/0/features",
                headers={"Authorization": f"Bearer {self._token}"}
            )
            return response.json()
    
    async def poll_installations(self, 
                                  installation_ids: List[str]
                                  ) -> AsyncGenerator[dict, None]:
        """Poll multiple installations for updated data."""
        for installation_id in installation_ids:
            try:
                data = await self.get_device_data(installation_id)
                yield {
                    "installation_id": installation_id,
                    "timestamp": datetime.utcnow(),
                    "data": data
                }
            except Exception as e:
                logger.warning(f"Failed to poll {installation_id}: {e}")
```

### 12.2 Time-Series Database Storage

Energy data requires specialized storage optimized for time-indexed writes and range queries.

**InfluxDB** example:

```python
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBStorage:
    """Time-series storage using InfluxDB."""
    
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.bucket = bucket
        self.org = org
        
    def write_sensor_reading(self, building_id: str, sensor_id: str,
                             value: float, timestamp: datetime):
        """Write single sensor reading."""
        point = (
            Point("sensor_reading")
            .tag("building_id", building_id)
            .tag("sensor_id", sensor_id)
            .field("value", value)
            .time(timestamp)
        )
        self.write_api.write(bucket=self.bucket, record=point)
    
    def query_sensor_data(self, building_id: str, sensor_id: str,
                          start: datetime, end: datetime) -> pd.DataFrame:
        """Query sensor data for time range."""
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: {start.isoformat()}Z, stop: {end.isoformat()}Z)
            |> filter(fn: (r) => r["building_id"] == "{building_id}")
            |> filter(fn: (r) => r["sensor_id"] == "{sensor_id}")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        result = self.query_api.query_data_frame(query, org=self.org)
        return result
```

**TimescaleDB** (PostgreSQL extension) for SQL-native time-series:

```sql
-- Create hypertable for sensor data
CREATE TABLE sensor_readings (
    time        TIMESTAMPTZ NOT NULL,
    building_id TEXT NOT NULL,
    sensor_id   TEXT NOT NULL,
    value       DOUBLE PRECISION,
    quality     TEXT DEFAULT 'good'
);

SELECT create_hypertable('sensor_readings', 'time');

-- Create index for common query patterns
CREATE INDEX idx_sensor_readings_building_sensor 
ON sensor_readings (building_id, sensor_id, time DESC);

-- Continuous aggregate for hourly rollups
CREATE MATERIALIZED VIEW sensor_readings_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    building_id,
    sensor_id,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value,
    COUNT(*) AS reading_count
FROM sensor_readings
GROUP BY bucket, building_id, sensor_id;

-- Retention policy: raw data for 90 days, hourly for 2 years
SELECT add_retention_policy('sensor_readings', INTERVAL '90 days');
```

### 12.3 ETL Patterns for Sensor Data

**Stream processing** for real-time transformations:

```python
from typing import Dict, Any
import asyncio
from dataclasses import dataclass

@dataclass
class TransformedReading:
    building_id: str
    timestamp: datetime
    vorlauf_temp: float
    ruecklauf_temp: float
    spreizung: float  # Calculated field
    outdoor_temp: float
    heat_power_kw: float

class SensorDataTransformer:
    """Transform raw sensor readings into analytics-ready format."""
    
    def __init__(self, building_config: Dict[str, Any]):
        self.config = building_config
        self._buffer: Dict[str, Dict] = {}  # Buffer partial readings
        
    async def process_reading(self, raw: dict) -> Optional[TransformedReading]:
        """Process incoming reading, emit when complete set available."""
        building_id = raw['building_id']
        sensor_type = raw['sensor_type']
        
        # Initialize buffer for building if needed
        if building_id not in self._buffer:
            self._buffer[building_id] = {
                'timestamp': raw['timestamp'],
                'readings': {}
            }
        
        # Store reading in buffer
        self._buffer[building_id]['readings'][sensor_type] = raw['value']
        
        # Check if we have all required sensors
        required = {'vorlauf_temp', 'ruecklauf_temp', 'outdoor_temp', 'flow_rate'}
        available = set(self._buffer[building_id]['readings'].keys())
        
        if required.issubset(available):
            readings = self._buffer[building_id]['readings']
            
            # Calculate derived fields
            spreizung = readings['vorlauf_temp'] - readings['ruecklauf_temp']
            
            # Heat power: Q = m_dot * c_p * delta_T
            # flow_rate in L/min, c_p = 4.18 kJ/(kg·K), convert to kW
            flow_kg_s = readings['flow_rate'] / 60  # L/min to kg/s (assuming water)
            heat_power_kw = flow_kg_s * 4.18 * spreizung
            
            result = TransformedReading(
                building_id=building_id,
                timestamp=self._buffer[building_id]['timestamp'],
                vorlauf_temp=readings['vorlauf_temp'],
                ruecklauf_temp=readings['ruecklauf_temp'],
                spreizung=spreizung,
                outdoor_temp=readings['outdoor_temp'],
                heat_power_kw=heat_power_kw
            )
            
            # Clear buffer
            del self._buffer[building_id]
            
            return result
        
        return None
```

**Batch processing** for historical analysis:

```python
import pandas as pd
from pathlib import Path

class BatchETLPipeline:
    """Batch ETL for historical sensor data processing."""
    
    def __init__(self, source_db, target_db, config):
        self.source = source_db
        self.target = target_db
        self.config = config
        
    def extract(self, building_id: str, start: datetime, 
                end: datetime) -> pd.DataFrame:
        """Extract raw sensor data for building."""
        query = """
        SELECT time, sensor_id, value, quality
        FROM sensor_readings
        WHERE building_id = %s
          AND time BETWEEN %s AND %s
        ORDER BY time
        """
        return pd.read_sql(query, self.source, 
                          params=[building_id, start, end])
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform raw readings into feature matrix."""
        # Pivot sensors to columns
        df_pivot = df.pivot(index='time', columns='sensor_id', values='value')
        
        # Resample to consistent frequency
        df_resampled = df_pivot.resample('15T').mean()
        
        # Handle missing values
        df_clean = self._handle_missing(df_resampled)
        
        # Calculate derived features
        df_features = self._calculate_features(df_clean)
        
        # Add quality flags
        df_features['data_quality'] = self._assess_quality(df_resampled)
        
        return df_features
    
    def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values with appropriate strategies."""
        df = df.copy()
        
        # Forward fill for short gaps (< 1 hour)
        df = df.fillna(method='ffill', limit=4)
        
        # Interpolate remaining short gaps
        df = df.interpolate(method='time', limit=8)
        
        return df
    
    def _calculate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived features."""
        df = df.copy()
        
        if 'vorlauf_temp' in df.columns and 'ruecklauf_temp' in df.columns:
            df['spreizung'] = df['vorlauf_temp'] - df['ruecklauf_temp']
        
        if 'outdoor_temp' in df.columns:
            df['heating_degree_hours'] = (18 - df['outdoor_temp']).clip(lower=0)
        
        return df
    
    def load(self, df: pd.DataFrame, building_id: str):
        """Load transformed data to analytics database."""
        df['building_id'] = building_id
        df.to_sql('building_features', self.target, 
                  if_exists='append', index=True)
    
    def run(self, building_id: str, start: datetime, end: datetime):
        """Execute full ETL pipeline."""
        raw_data = self.extract(building_id, start, end)
        transformed = self.transform(raw_data)
        self.load(transformed, building_id)
```

---

## Chapter 13: Production-Ready Algorithm Development

Production code requires higher quality standards than research prototypes. This chapter covers practices ensuring maintainability, reliability, and collaboration.

### 13.1 Code Quality Standards

**Type hints** improve readability and enable static analysis:

```python
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
import pandas as pd
import numpy as np

def calculate_heating_curve(
    outdoor_temps: np.ndarray,
    base_temp: float = 35.0,
    slope: float = 1.5,
    min_flow: float = 25.0,
    max_flow: float = 75.0
) -> np.ndarray:
    """
    Calculate flow temperature setpoints from heating curve.
    
    Parameters
    ----------
    outdoor_temps : np.ndarray
        Array of outdoor temperatures in °C.
    base_temp : float
        Base flow temperature at 20°C outdoor (default: 35.0°C).
    slope : float
        Heating curve slope (default: 1.5).
    min_flow : float
        Minimum flow temperature (default: 25.0°C).
    max_flow : float
        Maximum flow temperature (default: 75.0°C).
        
    Returns
    -------
    np.ndarray
        Calculated flow temperature setpoints in °C.
        
    Examples
    --------
    >>> temps = np.array([0, 5, 10, 15])
    >>> calculate_heating_curve(temps, base_temp=40, slope=1.2)
    array([64., 58., 52., 46.])
    """
    flow_temps = base_temp + slope * (20.0 - outdoor_temps)
    return np.clip(flow_temps, min_flow, max_flow)
```

**Dataclasses** for structured data:

```python
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class BuildingConfig:
    """Configuration for a building's heating system."""
    building_id: str
    heating_type: str  # 'gas', 'fernwaerme', 'waermepumpe', 'hybrid'
    area_m2: float
    year_built: int
    heating_circuits: int = 1
    has_dhw: bool = True
    
    # Optional optimization parameters
    comfort_temp_min: float = 20.0
    comfort_temp_max: float = 22.0
    night_setback_enabled: bool = True
    night_setback_start: int = 22  # Hour
    night_setback_end: int = 6     # Hour
    night_setback_reduction: float = 3.0  # °C

@dataclass
class OptimizationResult:
    """Result of heating optimization run."""
    building_id: str
    timestamp: datetime
    recommended_vorlauf: float
    recommended_setpoint: float
    predicted_savings_percent: float
    confidence: float
    constraints_violated: List[str] = field(default_factory=list)
```

**SOLID principles** application:

```python
# Single Responsibility: Each class has one job
class HeatingCurveCalculator:
    """Calculates flow temperatures from heating curve parameters."""
    
    def __init__(self, params: HeatingCurveParams):
        self.params = params
    
    def calculate(self, outdoor_temp: float) -> float:
        return self.params.base + self.params.slope * (20 - outdoor_temp)

class ComfortConstraintChecker:
    """Validates temperature constraints for occupant comfort."""
    
    def __init__(self, config: BuildingConfig):
        self.config = config
    
    def check(self, indoor_temp: float) -> Tuple[bool, Optional[str]]:
        if indoor_temp < self.config.comfort_temp_min:
            return False, f"Below minimum: {indoor_temp}°C < {self.config.comfort_temp_min}°C"
        if indoor_temp > self.config.comfort_temp_max:
            return False, f"Above maximum: {indoor_temp}°C > {self.config.comfort_temp_max}°C"
        return True, None


# Open/Closed: Extend via inheritance, not modification
from abc import ABC, abstractmethod

class HeatingSystemOptimizer(ABC):
    """Abstract base for heating system optimizers."""
    
    @abstractmethod
    def optimize(self, state: SystemState) -> OptimizationResult:
        pass

class GasBoilerOptimizer(HeatingSystemOptimizer):
    """Optimizer for gas boiler systems."""
    
    def optimize(self, state: SystemState) -> OptimizationResult:
        # Gas-specific optimization logic
        pass

class HeatPumpOptimizer(HeatingSystemOptimizer):
    """Optimizer for heat pump systems."""
    
    def optimize(self, state: SystemState) -> OptimizationResult:
        # Heat pump-specific optimization (COP-aware)
        pass


# Dependency Injection: Dependencies passed in, not created
class OptimizationService:
    """Service coordinating optimization across buildings."""
    
    def __init__(
        self,
        optimizer_factory: Callable[[str], HeatingSystemOptimizer],
        data_source: DataSource,
        result_store: ResultStore
    ):
        self.optimizer_factory = optimizer_factory
        self.data_source = data_source
        self.result_store = result_store
    
    def run_optimization(self, building_id: str) -> OptimizationResult:
        config = self.data_source.get_building_config(building_id)
        state = self.data_source.get_current_state(building_id)
        
        optimizer = self.optimizer_factory(config.heating_type)
        result = optimizer.optimize(state)
        
        self.result_store.save(result)
        return result
```

### 13.2 Testing Strategies

**Unit tests** for individual functions:

```python
import pytest
import numpy as np
from heating.curves import calculate_heating_curve

class TestHeatingCurve:
    """Tests for heating curve calculation."""
    
    def test_basic_calculation(self):
        """Test heating curve at standard conditions."""
        outdoor = np.array([0.0])
        result = calculate_heating_curve(outdoor, base_temp=40.0, slope=1.5)
        expected = 40.0 + 1.5 * 20.0  # 70.0
        assert result[0] == pytest.approx(70.0)
    
    def test_respects_max_limit(self):
        """Test that max flow temperature is enforced."""
        outdoor = np.array([-20.0])  # Very cold
        result = calculate_heating_curve(outdoor, max_flow=75.0)
        assert result[0] <= 75.0
    
    def test_respects_min_limit(self):
        """Test that min flow temperature is enforced."""
        outdoor = np.array([25.0])  # Warm, no heating needed
        result = calculate_heating_curve(outdoor, min_flow=25.0)
        assert result[0] >= 25.0
    
    def test_array_input(self):
        """Test with array of outdoor temperatures."""
        outdoor = np.array([-10, 0, 10, 20])
        result = calculate_heating_curve(outdoor, base_temp=35.0, slope=1.0)
        assert len(result) == 4
        assert result[0] > result[1] > result[2] > result[3]
    
    @pytest.mark.parametrize("outdoor,expected", [
        (0.0, 65.0),
        (10.0, 50.0),
        (20.0, 35.0),
    ])
    def test_specific_values(self, outdoor, expected):
        """Test specific outdoor/flow temperature pairs."""
        result = calculate_heating_curve(
            np.array([outdoor]), 
            base_temp=35.0, 
            slope=1.5
        )
        assert result[0] == pytest.approx(expected)
```

**Integration tests** for component interactions:

```python
import pytest
from datetime import datetime, timedelta
from heating.pipeline import OptimizationPipeline
from heating.storage import InMemoryStorage

class TestOptimizationPipeline:
    """Integration tests for optimization pipeline."""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline with test dependencies."""
        storage = InMemoryStorage()
        return OptimizationPipeline(storage=storage)
    
    @pytest.fixture
    def sample_building_data(self):
        """Generate sample building sensor data."""
        timestamps = pd.date_range(
            start='2025-01-01', 
            periods=168,  # 1 week hourly
            freq='H'
        )
        return pd.DataFrame({
            'timestamp': timestamps,
            'vorlauf_temp': np.random.uniform(50, 65, 168),
            'ruecklauf_temp': np.random.uniform(35, 45, 168),
            'outdoor_temp': np.sin(np.linspace(0, 4*np.pi, 168)) * 5 + 5,
        })
    
    def test_full_pipeline_execution(self, pipeline, sample_building_data):
        """Test complete pipeline from data ingestion to result."""
        building_id = "test-building-001"
        
        # Ingest data
        pipeline.ingest(building_id, sample_building_data)
        
        # Run optimization
        result = pipeline.optimize(building_id)
        
        # Verify result structure
        assert result.building_id == building_id
        assert 25.0 <= result.recommended_vorlauf <= 75.0
        assert 0.0 <= result.confidence <= 1.0
    
    def test_handles_missing_data(self, pipeline, sample_building_data):
        """Test pipeline handles missing sensor values."""
        # Introduce gaps
        sample_building_data.loc[10:15, 'vorlauf_temp'] = np.nan
        
        building_id = "test-building-002"
        pipeline.ingest(building_id, sample_building_data)
        
        # Should not raise, should handle gracefully
        result = pipeline.optimize(building_id)
        assert result is not None
```

**Property-based testing** for invariants:

```python
from hypothesis import given, strategies as st
import hypothesis.extra.numpy as hnp

class TestHeatingCurveProperties:
    """Property-based tests for heating curve."""
    
    @given(st.floats(min_value=-30, max_value=40))
    def test_output_within_bounds(self, outdoor_temp):
        """Flow temp always within [min_flow, max_flow]."""
        result = calculate_heating_curve(
            np.array([outdoor_temp]),
            min_flow=25.0,
            max_flow=75.0
        )
        assert 25.0 <= result[0] <= 75.0
    
    @given(
        st.floats(min_value=-20, max_value=20),
        st.floats(min_value=-20, max_value=20)
    )
    def test_monotonically_decreasing(self, temp1, temp2):
        """Colder outdoor temp yields higher flow temp."""
        if temp1 < temp2:
            result = calculate_heating_curve(np.array([temp1, temp2]))
            assert result[0] >= result[1]
```

### 13.3 Version Control Practices

**Branching strategy** (GitFlow variant):

```
main (production)
  └── develop (integration)
        ├── feature/heating-curve-optimizer
        ├── feature/anomaly-detection-v2
        └── bugfix/return-temp-threshold
```

**Commit message conventions:**

```
feat(optimizer): add dynamic heating curve adjustment

Implement adaptive heating curve that adjusts slope based on
observed indoor temperature response. Uses 7-day rolling window
for parameter estimation.

- Add HeatingCurveAdapter class
- Integrate with OptimizationService
- Add unit tests for edge cases

Closes #142
```

**Code review checklist:**

```markdown
## Code Review Checklist

### Correctness
- [ ] Logic correctly implements requirements
- [ ] Edge cases handled (empty data, extreme values)
- [ ] Units consistent (°C not °F, kW not W)

### Quality
- [ ] Type hints present and correct
- [ ] Docstrings for public functions
- [ ] No code duplication
- [ ] Follows project style guide

### Testing
- [ ] Unit tests for new functions
- [ ] Integration tests if components interact
- [ ] Tests cover edge cases

### Performance
- [ ] No obvious O(n²) or worse algorithms
- [ ] Database queries optimized
- [ ] Large data handled in batches

### Security
- [ ] No hardcoded credentials
- [ ] Input validation present
- [ ] SQL injection prevented (parameterized queries)
```

---

## Chapter 14: MLOps Fundamentals

MLOps practices ensure machine learning models are reproducible, deployable, and maintainable in production.

### 14.1 Experiment Tracking

**MLflow** for tracking experiments:

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

def train_consumption_model(X_train, y_train, X_test, y_test, params):
    """Train and log consumption prediction model."""
    
    mlflow.set_experiment("heat_demand_forecasting")
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(params)
        
        # Log dataset info
        mlflow.log_param("train_samples", len(X_train))
        mlflow.log_param("test_samples", len(X_test))
        mlflow.log_param("features", list(X_train.columns))
        
        # Train model
        model = GradientBoostingRegressor(**params)
        model.fit(X_train, y_train)
        
        # Evaluate
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        metrics = {
            "train_rmse": np.sqrt(mean_squared_error(y_train, train_pred)),
            "test_rmse": np.sqrt(mean_squared_error(y_test, test_pred)),
            "train_mae": mean_absolute_error(y_train, train_pred),
            "test_mae": mean_absolute_error(y_test, test_pred),
        }
        mlflow.log_metrics(metrics)
        
        # Log feature importance
        importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        importance.to_csv("feature_importance.csv", index=False)
        mlflow.log_artifact("feature_importance.csv")
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        return model, metrics
```

### 14.2 Model Versioning and Registry

**Model registry workflow:**

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

def promote_model_to_production(model_name: str, run_id: str):
    """Promote a model version to production stage."""
    
    # Register model from run
    model_uri = f"runs:/{run_id}/model"
    mv = mlflow.register_model(model_uri, model_name)
    
    # Transition to staging for validation
    client.transition_model_version_stage(
        name=model_name,
        version=mv.version,
        stage="Staging"
    )
    
    # After validation, promote to production
    # (In practice, this would follow automated tests)
    client.transition_model_version_stage(
        name=model_name,
        version=mv.version,
        stage="Production"
    )
    
    # Archive previous production version
    for mv_old in client.search_model_versions(f"name='{model_name}'"):
        if mv_old.current_stage == "Production" and mv_old.version != mv.version:
            client.transition_model_version_stage(
                name=model_name,
                version=mv_old.version,
                stage="Archived"
            )

def load_production_model(model_name: str):
    """Load the current production model."""
    model_uri = f"models:/{model_name}/Production"
    return mlflow.sklearn.load_model(model_uri)
```

### 14.3 CI/CD for ML Pipelines

**GitHub Actions workflow** for ML:

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          ruff check .
          mypy src/
      
      - name: Run tests
        run: pytest tests/ -v --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  train:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Train model
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}
        run: python scripts/train_model.py
      
      - name: Validate model
        run: python scripts/validate_model.py --min-rmse 5.0
```

### 14.4 Model Monitoring

**Data drift detection:**

```python
from scipy import stats
import pandas as pd

class DataDriftMonitor:
    """Monitor for detecting data distribution drift."""
    
    def __init__(self, reference_data: pd.DataFrame, 
                 significance_level: float = 0.05):
        self.reference = reference_data
        self.alpha = significance_level
        self._compute_reference_stats()
    
    def _compute_reference_stats(self):
        """Compute reference distribution statistics."""
        self.ref_stats = {}
        for col in self.reference.select_dtypes(include=[np.number]).columns:
            self.ref_stats[col] = {
                'mean': self.reference[col].mean(),
                'std': self.reference[col].std(),
                'distribution': self.reference[col].values
            }
    
    def check_drift(self, current_data: pd.DataFrame) -> Dict[str, dict]:
        """Check for drift in current data vs reference."""
        results = {}
        
        for col in self.ref_stats:
            if col not in current_data.columns:
                continue
            
            ref_dist = self.ref_stats[col]['distribution']
            curr_dist = current_data[col].dropna().values
            
            # Kolmogorov-Smirnov test
            ks_stat, ks_pvalue = stats.ks_2samp(ref_dist, curr_dist)
            
            # Population Stability Index
            psi = self._calculate_psi(ref_dist, curr_dist)
            
            results[col] = {
                'ks_statistic': ks_stat,
                'ks_pvalue': ks_pvalue,
                'drift_detected': ks_pvalue < self.alpha,
                'psi': psi,
                'psi_alert': psi > 0.2  # PSI > 0.2 indicates significant drift
            }
        
        return results
    
    def _calculate_psi(self, reference: np.ndarray, 
                       current: np.ndarray, bins: int = 10) -> float:
        """Calculate Population Stability Index."""
        # Create bins from reference distribution
        _, bin_edges = np.histogram(reference, bins=bins)
        
        ref_counts, _ = np.histogram(reference, bins=bin_edges)
        curr_counts, _ = np.histogram(current, bins=bin_edges)
        
        # Convert to proportions, avoid zeros
        ref_pct = (ref_counts + 1) / (len(reference) + bins)
        curr_pct = (curr_counts + 1) / (len(current) + bins)
        
        psi = np.sum((curr_pct - ref_pct) * np.log(curr_pct / ref_pct))
        return psi
```

**Model performance monitoring:**

```python
class ModelPerformanceMonitor:
    """Monitor model predictions against actuals."""
    
    def __init__(self, model_name: str, alert_threshold_rmse: float):
        self.model_name = model_name
        self.threshold = alert_threshold_rmse
        self.predictions_log = []
        
    def log_prediction(self, prediction: float, actual: float, 
                       timestamp: datetime, metadata: dict = None):
        """Log a prediction-actual pair."""
        self.predictions_log.append({
            'timestamp': timestamp,
            'prediction': prediction,
            'actual': actual,
            'error': actual - prediction,
            'metadata': metadata or {}
        })
    
    def compute_metrics(self, window_hours: int = 24) -> dict:
        """Compute metrics over recent window."""
        cutoff = datetime.utcnow() - timedelta(hours=window_hours)
        recent = [p for p in self.predictions_log if p['timestamp'] > cutoff]
        
        if len(recent) < 10:
            return {'status': 'insufficient_data', 'count': len(recent)}
        
        errors = np.array([p['error'] for p in recent])
        
        metrics = {
            'rmse': np.sqrt(np.mean(errors ** 2)),
            'mae': np.mean(np.abs(errors)),
            'bias': np.mean(errors),
            'count': len(recent),
            'window_hours': window_hours
        }
        
        metrics['alert'] = metrics['rmse'] > self.threshold
        
        return metrics
```

---

## Chapter 15: Deployment Patterns

This chapter covers strategies for deploying ML models and optimization algorithms to production.

### 15.1 Batch vs. Real-Time Inference

**Batch inference** for periodic optimization:

```python
from datetime import datetime, timedelta
import schedule
import time

class BatchOptimizationJob:
    """Scheduled batch optimization for building portfolio."""
    
    def __init__(self, building_ids: List[str], 
                 optimizer: HeatingSystemOptimizer,
                 result_store: ResultStore):
        self.building_ids = building_ids
        self.optimizer = optimizer
        self.result_store = result_store
    
    def run(self):
        """Execute optimization for all buildings."""
        results = []
        
        for building_id in self.building_ids:
            try:
                state = self._get_current_state(building_id)
                result = self.optimizer.optimize(state)
                self.result_store.save(result)
                results.append(result)
                
            except Exception as e:
                logger.error(f"Optimization failed for {building_id}: {e}")
        
        logger.info(f"Batch complete: {len(results)}/{len(self.building_ids)} successful")
        return results

# Schedule hourly optimization
job = BatchOptimizationJob(building_ids, optimizer, store)
schedule.every().hour.at(":05").do(job.run)

while True:
    schedule.run_pending()
    time.sleep(60)
```

**Real-time inference** for immediate control:

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

class OptimizationRequest(BaseModel):
    building_id: str
    current_state: dict

class OptimizationResponse(BaseModel):
    building_id: str
    recommended_vorlauf: float
    recommended_setpoint: float
    valid_until: datetime

@app.post("/optimize", response_model=OptimizationResponse)
async def optimize_building(request: OptimizationRequest,
                           background_tasks: BackgroundTasks):
    """Real-time optimization endpoint."""
    
    # Load model
    model = load_production_model("heating_optimizer")
    
    # Prepare features
    features = prepare_features(request.current_state)
    
    # Get recommendation
    recommendation = model.predict(features)
    
    # Log for monitoring (async)
    background_tasks.add_task(
        log_prediction,
        request.building_id,
        recommendation
    )
    
    return OptimizationResponse(
        building_id=request.building_id,
        recommended_vorlauf=recommendation['vorlauf'],
        recommended_setpoint=recommendation['setpoint'],
        valid_until=datetime.utcnow() + timedelta(minutes=15)
    )
```

### 15.2 Edge Deployment Considerations

The GreenBox gateway enables edge computing for latency-sensitive control:

```python
# Lightweight model for edge deployment
import onnxruntime as ort

class EdgeOptimizer:
    """Lightweight optimizer for GreenBox edge deployment."""
    
    def __init__(self, model_path: str):
        # Load ONNX model for efficient inference
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Run inference on edge device."""
        return self.session.run(None, {self.input_name: features})[0]

# Model export for edge
def export_to_onnx(sklearn_model, sample_input, output_path):
    """Export sklearn model to ONNX for edge deployment."""
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType
    
    initial_type = [('features', FloatTensorType([None, sample_input.shape[1]]))]
    onnx_model = convert_sklearn(sklearn_model, initial_types=initial_type)
    
    with open(output_path, 'wb') as f:
        f.write(onnx_model.SerializeToString())
```

### 15.3 A/B Testing and Gradual Rollout

```python
import hashlib
from enum import Enum

class ModelVariant(Enum):
    CONTROL = "control"
    TREATMENT = "treatment"

class ABTestRouter:
    """Route buildings to model variants for A/B testing."""
    
    def __init__(self, treatment_fraction: float = 0.1,
                 experiment_name: str = "default"):
        self.treatment_fraction = treatment_fraction
        self.experiment_name = experiment_name
    
    def get_variant(self, building_id: str) -> ModelVariant:
        """Deterministically assign building to variant."""
        # Hash for consistent assignment
        hash_input = f"{self.experiment_name}:{building_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        
        # Map to [0, 1) range
        fraction = (hash_value % 10000) / 10000
        
        if fraction < self.treatment_fraction:
            return ModelVariant.TREATMENT
        return ModelVariant.CONTROL
    
    def get_model(self, building_id: str):
        """Get appropriate model for building."""
        variant = self.get_variant(building_id)
        
        if variant == ModelVariant.TREATMENT:
            return load_production_model("heating_optimizer_v2")
        return load_production_model("heating_optimizer_v1")
```

**Gradual rollout strategy:**

```python
class GradualRollout:
    """Manage gradual rollout of new model versions."""
    
    def __init__(self, rollout_schedule: List[Tuple[datetime, float]]):
        """
        Initialize with rollout schedule.
        
        Parameters:
        - rollout_schedule: List of (datetime, fraction) tuples
          e.g., [(day1, 0.01), (day3, 0.05), (day7, 0.25), (day14, 1.0)]
        """
        self.schedule = sorted(rollout_schedule, key=lambda x: x[0])
    
    def get_current_fraction(self) -> float:
        """Get current rollout fraction based on schedule."""
        now = datetime.utcnow()
        
        current_fraction = 0.0
        for scheduled_time, fraction in self.schedule:
            if now >= scheduled_time:
                current_fraction = fraction
            else:
                break
        
        return current_fraction
    
    def should_use_new_model(self, building_id: str) -> bool:
        """Determine if building should use new model."""
        fraction = self.get_current_fraction()
        router = ABTestRouter(treatment_fraction=fraction)
        return router.get_variant(building_id) == ModelVariant.TREATMENT
```

---

*End of Part III*
