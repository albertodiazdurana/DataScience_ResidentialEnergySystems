# Part IV: Technical Stack Deep Dive

---

## Chapter 16: Python for Energy Data Science

This chapter provides a deep dive into the Python libraries essential for energy data science, with emphasis on patterns and techniques specific to heating system optimization.

### 16.1 Pandas: Time-Indexed DataFrames

Energy data is inherently temporal. Pandas provides powerful abstractions for time series manipulation.

**DatetimeIndex fundamentals:**

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create time-indexed DataFrame from sensor data
def load_sensor_data(filepath: str) -> pd.DataFrame:
    """Load sensor data with proper datetime indexing."""
    df = pd.read_csv(filepath, parse_dates=['timestamp'])
    
    # Set timezone-aware index
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df = df.set_index('timestamp')
    
    # Convert to local timezone for analysis
    df.index = df.index.tz_convert('Europe/Berlin')
    
    # Sort and remove duplicates
    df = df.sort_index()
    df = df[~df.index.duplicated(keep='first')]
    
    return df

# Example data structure for heating system
df = pd.DataFrame({
    'vorlauf_temp': [52.3, 52.1, 51.8, 52.5, 53.1],
    'ruecklauf_temp': [38.7, 38.5, 38.2, 38.9, 39.2],
    'outdoor_temp': [5.2, 5.0, 4.8, 4.5, 4.3],
    'flow_rate_lpm': [12.5, 12.3, 12.1, 12.8, 13.0],
    'heat_power_kw': [11.2, 10.9, 10.5, 11.5, 12.1]
}, index=pd.date_range('2025-01-15 08:00', periods=5, freq='15T', tz='Europe/Berlin'))
```

**Resampling operations:**

```python
def resample_sensor_data(df: pd.DataFrame, freq: str = '1H') -> pd.DataFrame:
    """
    Resample sensor data to specified frequency with appropriate aggregations.
    
    Parameters
    ----------
    df : pd.DataFrame
        Sensor data with DatetimeIndex
    freq : str
        Target frequency ('15T', '1H', '1D', etc.)
    
    Returns
    -------
    pd.DataFrame
        Resampled data with appropriate aggregations per column type
    """
    # Define aggregation rules by physical quantity type
    agg_rules = {
        # Temperatures: mean value
        'vorlauf_temp': 'mean',
        'ruecklauf_temp': 'mean',
        'outdoor_temp': 'mean',
        
        # Flow rates: mean
        'flow_rate_lpm': 'mean',
        
        # Power: mean (instantaneous measurement)
        'heat_power_kw': 'mean',
        
        # Energy: sum (cumulative quantity)
        'energy_kwh': 'sum',
        
        # Counts: sum
        'burner_starts': 'sum',
        
        # Status flags: mode or last value
        'heating_mode': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[-1]
    }
    
    # Filter to columns present in DataFrame
    active_rules = {k: v for k, v in agg_rules.items() if k in df.columns}
    
    return df.resample(freq).agg(active_rules)


def calculate_energy_from_power(df: pd.DataFrame, 
                                 power_col: str = 'heat_power_kw') -> pd.Series:
    """
    Calculate cumulative energy from power measurements.
    
    Integrates power over time using trapezoidal rule.
    """
    # Get time differences in hours
    time_diff_hours = df.index.to_series().diff().dt.total_seconds() / 3600
    
    # Trapezoidal integration
    avg_power = (df[power_col] + df[power_col].shift(1)) / 2
    energy_kwh = avg_power * time_diff_hours
    
    return energy_kwh.cumsum()
```

**Window functions for feature engineering:**

```python
def create_rolling_features(df: pd.DataFrame, 
                            columns: list,
                            windows: list = [6, 24, 168]) -> pd.DataFrame:
    """
    Create rolling window features for specified columns.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input data with DatetimeIndex
    columns : list
        Columns to create rolling features for
    windows : list
        Window sizes in hours (default: 6h, 24h, 1 week)
    
    Returns
    -------
    pd.DataFrame
        Original data with added rolling features
    """
    df = df.copy()
    
    for col in columns:
        if col not in df.columns:
            continue
            
        for window in windows:
            window_str = f'{window}H'
            
            # Rolling mean
            df[f'{col}_rolling_mean_{window}h'] = (
                df[col].rolling(window=window_str, min_periods=1).mean()
            )
            
            # Rolling standard deviation
            df[f'{col}_rolling_std_{window}h'] = (
                df[col].rolling(window=window_str, min_periods=1).std()
            )
            
            # Rolling min/max
            df[f'{col}_rolling_min_{window}h'] = (
                df[col].rolling(window=window_str, min_periods=1).min()
            )
            df[f'{col}_rolling_max_{window}h'] = (
                df[col].rolling(window=window_str, min_periods=1).max()
            )
    
    return df


def create_lag_features(df: pd.DataFrame,
                        column: str,
                        lags: list = [1, 24, 168]) -> pd.DataFrame:
    """
    Create lagged features for autoregressive modeling.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input data with DatetimeIndex (assumed hourly)
    column : str
        Column to create lags for
    lags : list
        Lag values in hours
    
    Returns
    -------
    pd.DataFrame
        Original data with added lag features
    """
    df = df.copy()
    
    for lag in lags:
        df[f'{column}_lag_{lag}h'] = df[column].shift(lag)
    
    # Difference features (change from previous period)
    df[f'{column}_diff_1h'] = df[column].diff(1)
    df[f'{column}_diff_24h'] = df[column].diff(24)
    
    return df
```

**Handling time zones and daylight saving:**

```python
def handle_dst_transitions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle daylight saving time transitions in sensor data.
    
    DST transitions can cause:
    - Missing hours (spring forward): interpolate
    - Duplicate hours (fall back): average or keep first
    """
    df = df.copy()
    
    # Detect DST transitions
    if df.index.tz is not None:
        # Check for non-monotonic index (duplicates from fall back)
        if not df.index.is_monotonic_increasing:
            # Keep first occurrence of duplicates
            df = df[~df.index.duplicated(keep='first')]
    
    # Reindex to complete hourly sequence
    full_index = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq='1H',
        tz=df.index.tz
    )
    
    df = df.reindex(full_index)
    
    # Interpolate missing hours (spring forward gap)
    df = df.interpolate(method='time', limit=2)
    
    return df
```

### 16.2 NumPy and SciPy for Numerical Computing

**Signal processing for sensor data:**

```python
import numpy as np
from scipy import signal, stats
from scipy.ndimage import uniform_filter1d

def smooth_sensor_data(data: np.ndarray, 
                       method: str = 'savgol',
                       **kwargs) -> np.ndarray:
    """
    Apply smoothing to noisy sensor data.
    
    Parameters
    ----------
    data : np.ndarray
        Raw sensor values
    method : str
        Smoothing method: 'savgol', 'lowpass', 'moving_avg'
    **kwargs
        Method-specific parameters
    
    Returns
    -------
    np.ndarray
        Smoothed data
    """
    if method == 'savgol':
        # Savitzky-Golay filter: preserves peaks and edges
        window_length = kwargs.get('window_length', 11)
        polyorder = kwargs.get('polyorder', 3)
        return signal.savgol_filter(data, window_length, polyorder)
    
    elif method == 'lowpass':
        # Butterworth lowpass filter
        cutoff = kwargs.get('cutoff', 0.1)  # Normalized frequency
        order = kwargs.get('order', 4)
        b, a = signal.butter(order, cutoff, btype='low')
        return signal.filtfilt(b, a, data)
    
    elif method == 'moving_avg':
        # Simple moving average
        window = kwargs.get('window', 5)
        return uniform_filter1d(data, size=window)
    
    else:
        raise ValueError(f"Unknown method: {method}")


def detect_sensor_outliers(data: np.ndarray,
                           method: str = 'iqr',
                           **kwargs) -> np.ndarray:
    """
    Detect outliers in sensor data.
    
    Returns boolean mask where True indicates outlier.
    """
    if method == 'iqr':
        k = kwargs.get('k', 1.5)
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        lower = q1 - k * iqr
        upper = q3 + k * iqr
        return (data < lower) | (data > upper)
    
    elif method == 'zscore':
        threshold = kwargs.get('threshold', 3.0)
        z = np.abs(stats.zscore(data, nan_policy='omit'))
        return z > threshold
    
    elif method == 'mad':
        # Median Absolute Deviation (robust to outliers)
        threshold = kwargs.get('threshold', 3.5)
        median = np.nanmedian(data)
        mad = np.nanmedian(np.abs(data - median))
        modified_z = 0.6745 * (data - median) / mad
        return np.abs(modified_z) > threshold
    
    else:
        raise ValueError(f"Unknown method: {method}")
```

**Optimization with SciPy:**

```python
from scipy.optimize import minimize, differential_evolution, curve_fit

def optimize_heating_curve_params(outdoor_temps: np.ndarray,
                                   measured_demand: np.ndarray,
                                   comfort_temps: np.ndarray) -> dict:
    """
    Optimize heating curve parameters to match observed demand.
    
    Finds base_temp and slope that minimize prediction error
    while maintaining comfort constraints.
    """
    def heating_curve(outdoor, base, slope):
        """Predicted heat demand from heating curve."""
        flow_temp = base + slope * (20 - outdoor)
        # Simplified demand model: proportional to flow-outdoor delta
        return flow_temp - outdoor
    
    def objective(params):
        """Sum of squared errors."""
        base, slope = params
        predicted = heating_curve(outdoor_temps, base, slope)
        return np.sum((predicted - measured_demand) ** 2)
    
    def comfort_constraint(params):
        """Ensure minimum indoor temperature achieved."""
        base, slope = params
        predicted_flow = base + slope * (20 - outdoor_temps)
        # Simplified: flow temp must exceed outdoor by margin
        min_margin = 20  # Minimum flow-outdoor delta
        return np.min(predicted_flow - outdoor_temps) - min_margin
    
    # Initial guess
    x0 = [40.0, 1.5]
    
    # Bounds: base_temp [30, 50], slope [0.5, 3.0]
    bounds = [(30, 50), (0.5, 3.0)]
    
    # Constraints
    constraints = {'type': 'ineq', 'fun': comfort_constraint}
    
    result = minimize(
        objective,
        x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    
    return {
        'base_temp': result.x[0],
        'slope': result.x[1],
        'converged': result.success,
        'residual': result.fun
    }


def fit_building_thermal_model(outdoor_temps: np.ndarray,
                                indoor_temps: np.ndarray,
                                heat_power: np.ndarray,
                                dt_hours: float = 1.0) -> dict:
    """
    Fit simple RC thermal model to building data.
    
    Model: C * dT/dt = Q_heat - UA * (T_indoor - T_outdoor)
    
    Returns estimated thermal capacitance C and heat loss coefficient UA.
    """
    def model(t, C, UA):
        """Simulate indoor temperature evolution."""
        T_sim = np.zeros_like(indoor_temps)
        T_sim[0] = indoor_temps[0]
        
        for i in range(1, len(t)):
            Q_loss = UA * (T_sim[i-1] - outdoor_temps[i-1])
            Q_heat_watts = heat_power[i-1] * 1000  # kW to W
            dT = (Q_heat_watts - Q_loss) * dt_hours * 3600 / C
            T_sim[i] = T_sim[i-1] + dT
        
        return T_sim
    
    # Time array
    t = np.arange(len(indoor_temps))
    
    # Initial guesses: C = 10 MJ/K, UA = 500 W/K
    p0 = [1e7, 500]
    bounds = ([1e5, 50], [1e9, 5000])
    
    try:
        popt, pcov = curve_fit(
            lambda t, C, UA: model(t, C, UA),
            t,
            indoor_temps,
            p0=p0,
            bounds=bounds,
            maxfev=5000
        )
        
        # Calculate time constant
        tau_hours = popt[0] / popt[1] / 3600
        
        return {
            'C_joules_per_kelvin': popt[0],
            'UA_watts_per_kelvin': popt[1],
            'tau_hours': tau_hours,
            'fit_uncertainty': np.sqrt(np.diag(pcov))
        }
    
    except RuntimeError as e:
        return {'error': str(e)}
```

### 16.3 Scikit-learn: Pipelines and Model Selection

**Building ML pipelines for energy prediction:**

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV

def create_heating_demand_pipeline() -> Pipeline:
    """
    Create preprocessing and modeling pipeline for heat demand prediction.
    """
    # Define feature groups
    numeric_features = [
        'outdoor_temp', 'outdoor_temp_lag_24h', 'outdoor_temp_rolling_mean_24h',
        'wind_speed', 'solar_radiation',
        'heat_demand_lag_1h', 'heat_demand_lag_24h', 'heat_demand_lag_168h'
    ]
    
    categorical_features = [
        'heating_mode', 'day_of_week'
    ]
    
    cyclical_features = [
        'hour_sin', 'hour_cos', 'month_sin', 'month_cos'
    ]
    
    # Preprocessing for numeric features
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Preprocessing for categorical features
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # Cyclical features: already encoded, just scale
    cyclical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('scaler', StandardScaler())
    ])
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features),
            ('cyc', cyclical_transformer, cyclical_features)
        ],
        remainder='drop'
    )
    
    # Full pipeline with model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', GradientBoostingRegressor(random_state=42))
    ])
    
    return pipeline


def tune_pipeline_hyperparameters(pipeline: Pipeline,
                                   X: pd.DataFrame,
                                   y: pd.Series,
                                   n_splits: int = 5) -> dict:
    """
    Tune pipeline hyperparameters using time series cross-validation.
    """
    # Parameter grid
    param_grid = {
        'regressor__n_estimators': [100, 200, 300],
        'regressor__max_depth': [3, 5, 7],
        'regressor__learning_rate': [0.01, 0.05, 0.1],
        'regressor__min_samples_leaf': [5, 10, 20]
    }
    
    # Time series cross-validation
    tscv = TimeSeriesSplit(n_splits=n_splits)
    
    # Grid search
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=tscv,
        scoring='neg_root_mean_squared_error',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X, y)
    
    return {
        'best_params': grid_search.best_params_,
        'best_score': -grid_search.best_score_,  # Convert back to positive RMSE
        'cv_results': pd.DataFrame(grid_search.cv_results_)
    }
```

**Custom transformers for domain-specific features:**

```python
from sklearn.base import BaseEstimator, TransformerMixin

class HeatingDegreeHoursTransformer(BaseEstimator, TransformerMixin):
    """
    Calculate heating degree hours from outdoor temperature.
    
    HDH = max(0, base_temp - outdoor_temp)
    """
    def __init__(self, base_temp: float = 18.0, 
                 outdoor_temp_col: str = 'outdoor_temp'):
        self.base_temp = base_temp
        self.outdoor_temp_col = outdoor_temp_col
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        X['heating_degree_hours'] = np.maximum(
            0, self.base_temp - X[self.outdoor_temp_col]
        )
        return X


class TemperatureSpreizungTransformer(BaseEstimator, TransformerMixin):
    """
    Calculate temperature spread (Spreizung) between flow and return.
    """
    def __init__(self, vorlauf_col: str = 'vorlauf_temp',
                 ruecklauf_col: str = 'ruecklauf_temp'):
        self.vorlauf_col = vorlauf_col
        self.ruecklauf_col = ruecklauf_col
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        if self.vorlauf_col in X.columns and self.ruecklauf_col in X.columns:
            X['spreizung'] = X[self.vorlauf_col] - X[self.ruecklauf_col]
        return X


class CyclicalTimeEncoder(BaseEstimator, TransformerMixin):
    """
    Encode cyclical time features using sine/cosine transformation.
    """
    def __init__(self, datetime_col: str = 'timestamp'):
        self.datetime_col = datetime_col
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        
        if self.datetime_col in X.columns:
            dt = pd.to_datetime(X[self.datetime_col])
        elif isinstance(X.index, pd.DatetimeIndex):
            dt = X.index
        else:
            raise ValueError("No datetime column or index found")
        
        # Hour of day (period = 24)
        X['hour_sin'] = np.sin(2 * np.pi * dt.hour / 24)
        X['hour_cos'] = np.cos(2 * np.pi * dt.hour / 24)
        
        # Day of week (period = 7)
        X['dow_sin'] = np.sin(2 * np.pi * dt.dayofweek / 7)
        X['dow_cos'] = np.cos(2 * np.pi * dt.dayofweek / 7)
        
        # Month of year (period = 12)
        X['month_sin'] = np.sin(2 * np.pi * dt.month / 12)
        X['month_cos'] = np.cos(2 * np.pi * dt.month / 12)
        
        return X
```

**Cross-validation for time series:**

```python
from sklearn.model_selection import BaseCrossValidator

class BlockingTimeSeriesSplit(BaseCrossValidator):
    """
    Time series cross-validation with gap between train and test.
    
    Prevents data leakage from temporal autocorrelation.
    """
    def __init__(self, n_splits: int = 5, gap: int = 24):
        """
        Parameters
        ----------
        n_splits : int
            Number of splits
        gap : int
            Number of samples to skip between train and test
        """
        self.n_splits = n_splits
        self.gap = gap
    
    def get_n_splits(self, X=None, y=None, groups=None):
        return self.n_splits
    
    def split(self, X, y=None, groups=None):
        n_samples = len(X)
        
        # Calculate fold size
        fold_size = n_samples // (self.n_splits + 1)
        
        for i in range(self.n_splits):
            train_end = fold_size * (i + 1)
            test_start = train_end + self.gap
            test_end = test_start + fold_size
            
            if test_end > n_samples:
                test_end = n_samples
            
            train_indices = np.arange(0, train_end)
            test_indices = np.arange(test_start, test_end)
            
            yield train_indices, test_indices
```

---

## Chapter 17: Data Access Patterns

This chapter covers the data access technologies and patterns used in energy management systems.

### 17.1 SQL for Time Series Analysis

**Window functions for temporal analysis:**

```sql
-- Calculate rolling averages and detect anomalies
WITH hourly_stats AS (
    SELECT 
        building_id,
        date_trunc('hour', timestamp) AS hour,
        AVG(vorlauf_temp) AS avg_vorlauf,
        AVG(ruecklauf_temp) AS avg_ruecklauf,
        AVG(outdoor_temp) AS avg_outdoor,
        SUM(energy_kwh) AS total_energy
    FROM sensor_readings
    WHERE timestamp >= NOW() - INTERVAL '30 days'
    GROUP BY building_id, date_trunc('hour', timestamp)
),
with_rolling AS (
    SELECT
        *,
        -- 24-hour rolling average
        AVG(avg_vorlauf) OVER (
            PARTITION BY building_id
            ORDER BY hour
            ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
        ) AS vorlauf_rolling_24h,
        
        -- Standard deviation for anomaly detection
        STDDEV(avg_vorlauf) OVER (
            PARTITION BY building_id
            ORDER BY hour
            ROWS BETWEEN 167 PRECEDING AND CURRENT ROW  -- 1 week
        ) AS vorlauf_stddev_7d,
        
        -- Lag for comparison
        LAG(avg_vorlauf, 24) OVER (
            PARTITION BY building_id
            ORDER BY hour
        ) AS vorlauf_24h_ago
    FROM hourly_stats
)
SELECT
    building_id,
    hour,
    avg_vorlauf,
    vorlauf_rolling_24h,
    avg_vorlauf - vorlauf_rolling_24h AS deviation,
    CASE 
        WHEN ABS(avg_vorlauf - vorlauf_rolling_24h) > 2 * vorlauf_stddev_7d 
        THEN TRUE 
        ELSE FALSE 
    END AS is_anomaly
FROM with_rolling
WHERE hour >= NOW() - INTERVAL '7 days'
ORDER BY building_id, hour;
```

**Heating degree day calculations:**

```sql
-- Calculate daily and monthly heating degree days
WITH daily_temps AS (
    SELECT 
        building_id,
        DATE(timestamp) AS date,
        AVG(outdoor_temp) AS avg_temp
    FROM sensor_readings
    WHERE timestamp >= DATE_TRUNC('year', NOW())
    GROUP BY building_id, DATE(timestamp)
),
daily_hdd AS (
    SELECT
        building_id,
        date,
        avg_temp,
        GREATEST(0, 18.0 - avg_temp) AS hdd  -- Base temp 18°C
    FROM daily_temps
)
SELECT
    building_id,
    DATE_TRUNC('month', date) AS month,
    SUM(hdd) AS monthly_hdd,
    AVG(avg_temp) AS avg_monthly_temp,
    COUNT(*) AS days_in_month
FROM daily_hdd
GROUP BY building_id, DATE_TRUNC('month', date)
ORDER BY building_id, month;
```

**Energy consumption analysis:**

```sql
-- Compare consumption to previous period and weather-normalized baseline
WITH current_period AS (
    SELECT
        building_id,
        SUM(energy_kwh) AS energy_current,
        AVG(outdoor_temp) AS avg_temp_current,
        SUM(GREATEST(0, 18 - outdoor_temp)) AS hdd_current
    FROM hourly_consumption
    WHERE timestamp BETWEEN '2025-01-01' AND '2025-01-31'
    GROUP BY building_id
),
previous_period AS (
    SELECT
        building_id,
        SUM(energy_kwh) AS energy_previous,
        AVG(outdoor_temp) AS avg_temp_previous,
        SUM(GREATEST(0, 18 - outdoor_temp)) AS hdd_previous
    FROM hourly_consumption
    WHERE timestamp BETWEEN '2024-01-01' AND '2024-01-31'
    GROUP BY building_id
)
SELECT
    c.building_id,
    c.energy_current,
    p.energy_previous,
    
    -- Absolute change
    c.energy_current - p.energy_previous AS energy_change,
    
    -- Percentage change
    ROUND(100.0 * (c.energy_current - p.energy_previous) / 
          NULLIF(p.energy_previous, 0), 1) AS pct_change,
    
    -- Weather-normalized comparison (energy per HDD)
    c.energy_current / NULLIF(c.hdd_current, 0) AS energy_per_hdd_current,
    p.energy_previous / NULLIF(p.hdd_previous, 0) AS energy_per_hdd_previous,
    
    -- Weather-normalized change
    ROUND(100.0 * (
        (c.energy_current / NULLIF(c.hdd_current, 0)) - 
        (p.energy_previous / NULLIF(p.hdd_previous, 0))
    ) / NULLIF(p.energy_previous / NULLIF(p.hdd_previous, 0), 0), 1) 
        AS weather_normalized_pct_change

FROM current_period c
JOIN previous_period p ON c.building_id = p.building_id
ORDER BY weather_normalized_pct_change DESC;
```

**Detecting control parameter changes:**

```sql
-- Identify when heating curve parameters changed
WITH parameter_changes AS (
    SELECT
        building_id,
        timestamp,
        vorlauf_temp,
        outdoor_temp,
        -- Calculate implied heating curve slope
        (vorlauf_temp - LAG(vorlauf_temp) OVER w) / 
        NULLIF(outdoor_temp - LAG(outdoor_temp) OVER w, 0) AS implied_slope,
        
        -- Detect sudden jumps in flow temperature
        vorlauf_temp - LAG(vorlauf_temp) OVER w AS vorlauf_change
    FROM sensor_readings
    WHERE outdoor_temp BETWEEN -5 AND 15  -- Heating season, avoid extremes
    WINDOW w AS (PARTITION BY building_id ORDER BY timestamp)
)
SELECT
    building_id,
    timestamp,
    vorlauf_temp,
    outdoor_temp,
    vorlauf_change
FROM parameter_changes
WHERE ABS(vorlauf_change) > 5  -- Significant jump suggests manual intervention
ORDER BY building_id, timestamp;
```

### 17.2 GraphQL for Hierarchical Building Data

Energy systems have natural hierarchies: Portfolio → Building → System → Component → Sensor. GraphQL efficiently queries these nested structures.

**Schema design:**

```graphql
type Query {
    portfolio(id: ID!): Portfolio
    building(id: ID!): Building
    buildings(filter: BuildingFilter, limit: Int, offset: Int): [Building!]!
    sensorData(
        buildingId: ID!
        sensorIds: [String!]
        startTime: DateTime!
        endTime: DateTime!
        resolution: TimeResolution
    ): [TimeSeriesData!]!
}

type Portfolio {
    id: ID!
    name: String!
    buildings: [Building!]!
    totalArea: Float!
    totalEnergyConsumption(period: DateRange!): Float!
    aggregateMetrics: PortfolioMetrics!
}

type Building {
    id: ID!
    address: String!
    yearBuilt: Int!
    areaM2: Float!
    heatingSystem: HeatingSystem!
    sensors: [Sensor!]!
    currentState: BuildingState!
    energyConsumption(period: DateRange!): EnergyConsumption!
    optimizationStatus: OptimizationStatus!
}

type HeatingSystem {
    id: ID!
    type: HeatingSystemType!
    installedYear: Int!
    nominalPowerKw: Float!
    components: [HeatingComponent!]!
    currentOperatingMode: OperatingMode!
}

enum HeatingSystemType {
    GAS_BOILER
    OIL_BOILER
    DISTRICT_HEATING
    HEAT_PUMP
    HYBRID
    CHP
}

type Sensor {
    id: ID!
    type: SensorType!
    unit: String!
    currentValue: Float
    lastUpdated: DateTime!
    qualityStatus: QualityStatus!
}

type TimeSeriesData {
    sensorId: String!
    dataPoints: [DataPoint!]!
}

type DataPoint {
    timestamp: DateTime!
    value: Float!
    quality: QualityStatus!
}

input BuildingFilter {
    heatingType: HeatingSystemType
    minArea: Float
    maxArea: Float
    hasActiveOptimization: Boolean
}

enum TimeResolution {
    MINUTE_15
    HOURLY
    DAILY
    MONTHLY
}
```

**Python client implementation:**

```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class EnergyDataClient:
    """GraphQL client for energy data queries."""
    
    def __init__(self, endpoint: str, api_key: str):
        transport = RequestsHTTPTransport(
            url=endpoint,
            headers={'Authorization': f'Bearer {api_key}'}
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
    
    def get_building_with_sensors(self, building_id: str) -> dict:
        """Fetch building details with current sensor values."""
        query = gql("""
            query GetBuilding($id: ID!) {
                building(id: $id) {
                    id
                    address
                    areaM2
                    heatingSystem {
                        type
                        nominalPowerKw
                        currentOperatingMode
                    }
                    sensors {
                        id
                        type
                        currentValue
                        unit
                        lastUpdated
                    }
                    currentState {
                        indoorTemp
                        outdoorTemp
                        heatingActive
                    }
                    optimizationStatus {
                        enabled
                        lastOptimization
                        predictedSavingsPercent
                    }
                }
            }
        """)
        
        result = self.client.execute(query, variable_values={'id': building_id})
        return result['building']
    
    def get_sensor_timeseries(self, building_id: str, 
                              sensor_ids: list,
                              start: datetime,
                              end: datetime,
                              resolution: str = 'HOURLY') -> pd.DataFrame:
        """Fetch time series data for specified sensors."""
        query = gql("""
            query GetSensorData(
                $buildingId: ID!
                $sensorIds: [String!]
                $startTime: DateTime!
                $endTime: DateTime!
                $resolution: TimeResolution
            ) {
                sensorData(
                    buildingId: $buildingId
                    sensorIds: $sensorIds
                    startTime: $startTime
                    endTime: $endTime
                    resolution: $resolution
                ) {
                    sensorId
                    dataPoints {
                        timestamp
                        value
                        quality
                    }
                }
            }
        """)
        
        result = self.client.execute(query, variable_values={
            'buildingId': building_id,
            'sensorIds': sensor_ids,
            'startTime': start.isoformat(),
            'endTime': end.isoformat(),
            'resolution': resolution
        })
        
        # Convert to DataFrame
        dfs = []
        for sensor_data in result['sensorData']:
            sensor_id = sensor_data['sensorId']
            df = pd.DataFrame(sensor_data['dataPoints'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.set_index('timestamp')
            df = df.rename(columns={'value': sensor_id})
            dfs.append(df[[sensor_id]])
        
        return pd.concat(dfs, axis=1) if dfs else pd.DataFrame()
    
    def get_portfolio_summary(self, portfolio_id: str,
                              period_start: datetime,
                              period_end: datetime) -> dict:
        """Fetch portfolio-level aggregated metrics."""
        query = gql("""
            query GetPortfolio($id: ID!, $start: DateTime!, $end: DateTime!) {
                portfolio(id: $id) {
                    name
                    totalArea
                    buildings {
                        id
                        address
                        heatingSystem {
                            type
                        }
                        energyConsumption(period: {start: $start, end: $end}) {
                            totalKwh
                            costEur
                            co2Kg
                        }
                        optimizationStatus {
                            enabled
                            predictedSavingsPercent
                        }
                    }
                    aggregateMetrics {
                        totalBuildings
                        optimizedBuildings
                        avgSavingsPercent
                    }
                }
            }
        """)
        
        return self.client.execute(query, variable_values={
            'id': portfolio_id,
            'start': period_start.isoformat(),
            'end': period_end.isoformat()
        })['portfolio']
```

### 17.3 REST API Design

**API design for heating optimization service:**

```python
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

app = FastAPI(
    title="Green Fusion Energy Optimization API",
    version="1.0.0",
    description="API for heating system optimization and monitoring"
)

security = HTTPBearer()

# --- Models ---

class HeatingSystemType(str, Enum):
    GAS = "gas"
    DISTRICT = "district_heating"
    HEAT_PUMP = "heat_pump"
    HYBRID = "hybrid"

class BuildingCreate(BaseModel):
    address: str
    area_m2: float = Field(..., gt=0)
    year_built: int = Field(..., ge=1800, le=2025)
    heating_type: HeatingSystemType
    nominal_power_kw: float = Field(..., gt=0)

class BuildingResponse(BaseModel):
    id: str
    address: str
    area_m2: float
    year_built: int
    heating_type: HeatingSystemType
    optimization_enabled: bool
    created_at: datetime

class SensorReading(BaseModel):
    sensor_id: str
    timestamp: datetime
    value: float
    unit: str
    quality: str = "good"

class OptimizationRequest(BaseModel):
    building_id: str
    target_comfort_temp: float = Field(21.0, ge=18.0, le=24.0)
    optimization_horizon_hours: int = Field(24, ge=1, le=168)

class OptimizationResponse(BaseModel):
    building_id: str
    recommended_vorlauf_temp: float
    recommended_setpoint: float
    predicted_savings_percent: float
    valid_from: datetime
    valid_until: datetime
    constraints_applied: List[str]

class TimeSeriesQuery(BaseModel):
    building_id: str
    sensor_ids: List[str]
    start_time: datetime
    end_time: datetime
    resolution_minutes: int = Field(60, ge=1, le=1440)

# --- Endpoints ---

@app.get("/v1/buildings", response_model=List[BuildingResponse])
async def list_buildings(
    heating_type: Optional[HeatingSystemType] = None,
    optimization_enabled: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    List buildings with optional filtering.
    
    - **heating_type**: Filter by heating system type
    - **optimization_enabled**: Filter by optimization status
    - **limit**: Maximum number of results (default: 100)
    - **offset**: Pagination offset
    """
    # Implementation would query database
    pass

@app.get("/v1/buildings/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get details for a specific building."""
    pass

@app.post("/v1/buildings", response_model=BuildingResponse, status_code=201)
async def create_building(
    building: BuildingCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Register a new building in the system."""
    pass

@app.get("/v1/buildings/{building_id}/sensors/current")
async def get_current_sensor_values(
    building_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current values for all sensors in a building."""
    pass

@app.post("/v1/buildings/{building_id}/sensors/data")
async def query_sensor_timeseries(
    building_id: str,
    query: TimeSeriesQuery,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Query historical sensor data.
    
    Returns time series data for specified sensors within the given time range.
    Data is aggregated to the specified resolution.
    """
    # Validate time range
    max_range = timedelta(days=90)
    if query.end_time - query.start_time > max_range:
        raise HTTPException(
            status_code=400,
            detail=f"Time range exceeds maximum of {max_range.days} days"
        )
    
    # Implementation would query time series database
    pass

@app.post("/v1/optimize", response_model=OptimizationResponse)
async def request_optimization(
    request: OptimizationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Request heating optimization for a building.
    
    Returns recommended setpoints and predicted savings.
    """
    pass

@app.get("/v1/buildings/{building_id}/optimization/history")
async def get_optimization_history(
    building_id: str,
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get historical optimization recommendations and outcomes."""
    pass

# --- Error handling ---

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )
```

**API versioning and pagination patterns:**

```python
from fastapi import APIRouter
from typing import Generic, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')

class PaginatedResponse(GenericModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: List[T]
    total: int
    limit: int
    offset: int
    has_more: bool

class PaginationParams(BaseModel):
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)

def paginate(items: List[T], total: int, params: PaginationParams) -> PaginatedResponse[T]:
    """Create paginated response."""
    return PaginatedResponse(
        items=items,
        total=total,
        limit=params.limit,
        offset=params.offset,
        has_more=(params.offset + len(items)) < total
    )

# Versioned routers
v1_router = APIRouter(prefix="/v1", tags=["v1"])
v2_router = APIRouter(prefix="/v2", tags=["v2"])

@v1_router.get("/buildings")
async def list_buildings_v1():
    """V1 endpoint - stable."""
    pass

@v2_router.get("/buildings")
async def list_buildings_v2():
    """V2 endpoint - includes additional fields."""
    pass

app.include_router(v1_router)
app.include_router(v2_router)
```

---

*End of Part IV*
