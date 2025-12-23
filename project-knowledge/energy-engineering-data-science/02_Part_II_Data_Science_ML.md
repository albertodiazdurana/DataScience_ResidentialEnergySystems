# Part II: Data Science & Machine Learning for Energy Systems

---

## Chapter 6: Time Series Fundamentals for Energy Data

Energy systems generate continuous streams of temporal data from sensors, meters, and controllers. This chapter establishes the foundational concepts and techniques for working with energy time series.

### 6.1 Characteristics of Energy Time Series

Energy data exhibits distinct statistical properties that inform modeling choices.

**Seasonality** manifests at multiple scales:
- Daily: heat demand peaks morning/evening, PV production peaks midday
- Weekly: occupancy patterns differ weekdays vs. weekends
- Annual: heating demand follows outdoor temperature cycles

**Trend** components reflect:
- Long-term efficiency degradation (fouling, wear)
- Building occupancy changes
- Climate change effects (warming winters)

**Autocorrelation** is typically strong in energy data. Today's consumption correlates highly with yesterday's and last week's same day. The autocorrelation function (ACF) quantifies this:

$$\rho_k = \frac{Cov(y_t, y_{t-k})}{Var(y_t)}$$

For hourly heating data, expect significant autocorrelation at lags 1 (previous hour), 24 (same hour yesterday), and 168 (same hour last week).

**Non-stationarity** arises from:
- Seasonal mean shifts (winter vs. summer consumption)
- Variance changes (higher variability in heating season)
- Structural breaks (system modifications, control parameter changes)

Stationarity testing (Augmented Dickey-Fuller, KPSS tests) should precede model selection. Differencing or seasonal decomposition may be required.

### 6.2 Resampling and Interpolation

Raw sensor data arrives at varying frequencies and may contain gaps. Preprocessing establishes consistent temporal resolution.

**Resampling** converts between frequencies:

```python
import pandas as pd

# Upsample 15-minute data to 5-minute with interpolation
df_5min = df.resample('5T').interpolate(method='linear')

# Downsample to hourly with appropriate aggregation
df_hourly = df.resample('1H').agg({
    'temperature_vorlauf': 'mean',
    'energy_kwh': 'sum',  # Energy sums, not averages
    'power_kw': 'mean'
})
```

**Aggregation methods** must respect physical quantities:
- Temperatures: mean or time-weighted mean
- Energy (kWh): sum
- Power (kW): mean
- Flow rates: mean
- Counts (cycles, starts): sum

**Interpolation strategies** for missing data:

Linear interpolation suits slowly-varying quantities (outdoor temperature). For quantities with daily patterns, time-of-day aware methods perform better:

```python
def interpolate_with_daily_pattern(series, max_gap_hours=4):
    """
    Interpolate missing values using same-hour values from adjacent days.
    Only interpolate gaps shorter than max_gap_hours.
    """
    interpolated = series.copy()
    mask = series.isna()
    
    for idx in series[mask].index:
        # Find same hour from previous and next day
        prev_day = idx - pd.Timedelta(days=1)
        next_day = idx + pd.Timedelta(days=1)
        
        values = []
        if prev_day in series.index and pd.notna(series[prev_day]):
            values.append(series[prev_day])
        if next_day in series.index and pd.notna(series[next_day]):
            values.append(series[next_day])
        
        if values:
            interpolated[idx] = np.mean(values)
    
    return interpolated
```

**Gap handling policies:**
- Short gaps (<4 hours): interpolate
- Medium gaps (4-24 hours): flag and interpolate with reduced confidence
- Long gaps (>24 hours): exclude from training, handle explicitly in inference

### 6.3 Feature Engineering for Energy Time Series

Raw timestamps transform into predictive features capturing temporal patterns.

**Calendar features:**

```python
def create_calendar_features(df):
    """Generate calendar-based features from DatetimeIndex."""
    df = df.copy()
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    df['month'] = df.index.month
    df['is_weekend'] = df.index.dayofweek >= 5
    df['is_business_hour'] = df['hour'].between(8, 18)
    
    # German public holidays matter for occupancy
    # Use 'holidays' library for accurate holiday detection
    
    return df
```

**Cyclical encoding** prevents discontinuities (hour 23 should be close to hour 0):

```python
def cyclical_encode(df, col, max_val):
    """Encode cyclical feature using sine/cosine transformation."""
    df[f'{col}_sin'] = np.sin(2 * np.pi * df[col] / max_val)
    df[f'{col}_cos'] = np.cos(2 * np.pi * df[col] / max_val)
    return df

df = cyclical_encode(df, 'hour', 24)
df = cyclical_encode(df, 'day_of_week', 7)
df = cyclical_encode(df, 'month', 12)
```

**Lag features** capture autocorrelation:

```python
def create_lag_features(df, column, lags):
    """Create lagged versions of a column."""
    for lag in lags:
        df[f'{column}_lag_{lag}h'] = df[column].shift(lag)
    return df

# Typical lags for hourly heating data
lags = [1, 2, 3, 6, 12, 24, 48, 168]  # hours
df = create_lag_features(df, 'heat_demand_kw', lags)
```

**Rolling statistics** smooth noise and capture trends:

```python
def create_rolling_features(df, column, windows):
    """Create rolling mean and std features."""
    for window in windows:
        df[f'{column}_rolling_mean_{window}h'] = (
            df[column].rolling(window=window, min_periods=1).mean()
        )
        df[f'{column}_rolling_std_{window}h'] = (
            df[column].rolling(window=window, min_periods=1).std()
        )
    return df

windows = [6, 24, 168]  # 6h, 1d, 1w
df = create_rolling_features(df, 'outdoor_temp', windows)
```

**Fourier terms** capture complex seasonality:

```python
def fourier_features(index, period, n_terms):
    """Generate Fourier series features for seasonality."""
    t = np.arange(len(index))
    features = {}
    for k in range(1, n_terms + 1):
        features[f'sin_{period}_{k}'] = np.sin(2 * np.pi * k * t / period)
        features[f'cos_{period}_{k}'] = np.cos(2 * np.pi * k * t / period)
    return pd.DataFrame(features, index=index)

# Daily seasonality with 4 harmonics (for hourly data, period=24)
fourier_daily = fourier_features(df.index, period=24, n_terms=4)
```

---

## Chapter 7: Forecasting Heat Demand & Energy Production

Accurate forecasting enables proactive control strategies, from next-hour adjustments to day-ahead planning for dynamic pricing optimization.

### 7.1 Classical Time Series Methods

**ARIMA (AutoRegressive Integrated Moving Average)** models capture linear dependencies:

$$y_t = c + \sum_{i=1}^{p} \phi_i y_{t-i} + \sum_{j=1}^{q} \theta_j \varepsilon_{t-j} + \varepsilon_t$$

Where p is the autoregressive order, q is the moving average order, and d (in ARIMA(p,d,q)) is the differencing order for stationarity.

**SARIMA** extends ARIMA with seasonal components:

$$SARIMA(p,d,q)(P,D,Q)_s$$

For hourly heating data with daily seasonality, s=24. Typical starting points: SARIMA(1,0,1)(1,1,1)₂₄.

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(
    train_data['heat_demand'],
    order=(1, 0, 1),
    seasonal_order=(1, 1, 1, 24),
    exog=train_data[['outdoor_temp', 'is_weekend']]
)
results = model.fit(disp=False)
forecast = results.forecast(steps=24, exog=test_exog)
```

**Exponential Smoothing (ETS)** provides robust baseline forecasts:

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(
    train_data['heat_demand'],
    seasonal_periods=24,
    trend='add',
    seasonal='add',
    damped_trend=True
)
results = model.fit()
forecast = results.forecast(24)
```

### 7.2 Machine Learning Approaches

Tree-based ensemble methods handle non-linear relationships and mixed feature types effectively.

**Gradient Boosting (XGBoost, LightGBM):**

```python
import lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit

# Prepare features (lagged values, calendar, weather)
feature_cols = [c for c in df.columns if c != 'heat_demand_kw']
X = df[feature_cols]
y = df['heat_demand_kw']

# Time series cross-validation
tscv = TimeSeriesSplit(n_splits=5)

params = {
    'objective': 'regression',
    'metric': 'rmse',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1
}

scores = []
for train_idx, val_idx in tscv.split(X):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
    
    train_set = lgb.Dataset(X_train, y_train)
    val_set = lgb.Dataset(X_val, y_val, reference=train_set)
    
    model = lgb.train(
        params,
        train_set,
        num_boost_round=1000,
        valid_sets=[val_set],
        callbacks=[lgb.early_stopping(50)]
    )
    
    pred = model.predict(X_val)
    rmse = np.sqrt(np.mean((pred - y_val) ** 2))
    scores.append(rmse)

print(f"CV RMSE: {np.mean(scores):.3f} +/- {np.std(scores):.3f}")
```

**Feature importance** guides model interpretation:

```python
importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importance(importance_type='gain')
}).sort_values('importance', ascending=False)

# Typical top features for heat demand:
# 1. outdoor_temp (dominant)
# 2. heat_demand_lag_1h
# 3. heat_demand_lag_24h
# 4. hour_sin, hour_cos
# 5. outdoor_temp_rolling_mean_24h
```

### 7.3 Deep Learning for Sequence Modeling

**LSTM (Long Short-Term Memory)** networks capture long-range temporal dependencies:

```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def create_sequences(data, seq_length, forecast_horizon):
    """Create sequences for LSTM training."""
    X, y = [], []
    for i in range(len(data) - seq_length - forecast_horizon + 1):
        X.append(data[i:(i + seq_length)])
        y.append(data[(i + seq_length):(i + seq_length + forecast_horizon), 0])
    return np.array(X), np.array(y)

seq_length = 168  # 1 week of hourly data
forecast_horizon = 24  # Predict next 24 hours

X, y = create_sequences(scaled_data, seq_length, forecast_horizon)

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(seq_length, n_features)),
    Dropout(0.2),
    LSTM(32, return_sequences=False),
    Dropout(0.2),
    Dense(forecast_horizon)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=50, batch_size=32, 
          validation_data=(X_val, y_val))
```

**Transformer architectures** increasingly outperform LSTMs for longer sequences, with attention mechanisms capturing relevant historical patterns regardless of temporal distance.

### 7.4 Weather Data Integration

Outdoor temperature is the dominant predictor for heat demand. Integration considerations:

**Data sources:**
- Historical: Deutscher Wetterdienst (DWD) open data
- Forecasts: Commercial APIs (OpenWeatherMap, Tomorrow.io) or DWD MOSMIX

**Feature engineering from weather:**

```python
weather_features = [
    'temp_outdoor',           # Current temperature
    'temp_outdoor_lag_24h',   # Same time yesterday
    'temp_outdoor_forecast_24h',  # Forecast for next 24h
    'temp_outdoor_rolling_mean_72h',  # 3-day average
    'heating_degree_hours',   # max(0, 18 - temp_outdoor)
    'wind_speed',             # Affects heat loss
    'solar_radiation',        # Passive solar gains
]
```

**Forecast uncertainty:** Weather forecasts degrade with horizon. Day-ahead temperature forecasts typically have RMSE of 1-2°C; week-ahead increases to 3-5°C. Ensemble forecasts or probabilistic predictions quantify this uncertainty for robust optimization.

---

## Chapter 8: Anomaly Detection in Heating Systems

Anomaly detection identifies equipment faults, control errors, and efficiency degradation. Green Fusion's platform uses this for automated alerting and proactive maintenance.

### 8.1 Statistical Methods

**Z-score detection** for normally distributed metrics:

```python
def detect_zscore_anomalies(series, threshold=3.0):
    """Flag values more than threshold standard deviations from mean."""
    z_scores = (series - series.mean()) / series.std()
    return np.abs(z_scores) > threshold
```

**Interquartile Range (IQR)** is robust to outliers:

```python
def detect_iqr_anomalies(series, k=1.5):
    """Flag values outside [Q1 - k*IQR, Q3 + k*IQR]."""
    Q1, Q3 = series.quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower = Q1 - k * IQR
    upper = Q3 + k * IQR
    return (series < lower) | (series > upper)
```

**Grubbs' test** for single outliers in small samples:

$$G = \frac{\max|x_i - \bar{x}|}{s}$$

Compare against critical values from Student's t-distribution.

### 8.2 Machine Learning Methods

**Isolation Forest** efficiently detects anomalies in multivariate data:

```python
from sklearn.ensemble import IsolationForest

features = ['vorlauf_temp', 'ruecklauf_temp', 'outdoor_temp', 
            'flow_rate', 'heat_power']

iso_forest = IsolationForest(
    n_estimators=100,
    contamination=0.01,  # Expected anomaly rate
    random_state=42
)

df['anomaly_score'] = iso_forest.fit_predict(df[features])
df['is_anomaly'] = df['anomaly_score'] == -1
```

**One-Class SVM** learns a boundary around normal operating regions:

```python
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

oc_svm = OneClassSVM(kernel='rbf', nu=0.01, gamma='auto')
df['anomaly_score'] = oc_svm.fit_predict(X_scaled)
```

**Autoencoders** learn compressed representations; high reconstruction error indicates anomalies:

```python
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

input_dim = len(features)
encoding_dim = 4

input_layer = Input(shape=(input_dim,))
encoded = Dense(8, activation='relu')(input_layer)
encoded = Dense(encoding_dim, activation='relu')(encoded)
decoded = Dense(8, activation='relu')(encoded)
decoded = Dense(input_dim, activation='linear')(decoded)

autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer='adam', loss='mse')

# Train on normal data only
autoencoder.fit(X_train_normal, X_train_normal, 
                epochs=50, batch_size=32, validation_split=0.1)

# Anomaly score = reconstruction error
reconstructed = autoencoder.predict(X_test)
mse = np.mean((X_test - reconstructed) ** 2, axis=1)
threshold = np.percentile(mse, 99)
anomalies = mse > threshold
```

### 8.3 Domain-Specific Anomaly Types

**Legionella risk** (circulation temperature < 50°C):

```python
def detect_legionella_risk(df, temp_col='zirkulation_temp', 
                           threshold=50.0, duration_hours=1):
    """
    Flag periods where circulation temperature falls below safe threshold.
    Requires sustained low temperature, not momentary dips.
    """
    below_threshold = df[temp_col] < threshold
    
    # Require consecutive hours below threshold
    rolling_count = below_threshold.rolling(duration_hours).sum()
    return rolling_count >= duration_hours
```

Green Fusion data showed 10% of systems with this risk condition.

**Excessive cycling (Taktverhalten):**

```python
def detect_excessive_cycling(df, power_col='burner_power', 
                             window_hours=1, max_cycles=6):
    """
    Detect excessive on/off cycling indicating control issues.
    """
    # Detect state changes (on->off or off->on)
    is_on = df[power_col] > 0
    state_changes = is_on.astype(int).diff().abs()
    
    # Count cycles per window
    cycles_per_window = state_changes.rolling(
        window=f'{window_hours}H'
    ).sum() / 2  # Each cycle = 2 state changes
    
    return cycles_per_window > max_cycles
```

**Return temperature violations** (Fernwärme penalty risk):

```python
def detect_return_temp_violations(df, temp_col='ruecklauf_temp',
                                  limit=60.0, tolerance=2.0):
    """
    Flag periods where return temperature exceeds contractual limit.
    Include tolerance band for early warning.
    """
    violation = df[temp_col] > limit
    warning = df[temp_col] > (limit - tolerance)
    
    return pd.DataFrame({
        'violation': violation,
        'warning': warning & ~violation
    })
```

**Simultaneous heating and cooling** (control fault in hybrid systems):

```python
def detect_simultaneous_heating_cooling(df):
    """Detect when both heating and cooling are active."""
    heating_active = df['heat_demand_kw'] > 0.5
    cooling_active = df['cooling_demand_kw'] > 0.5
    return heating_active & cooling_active
```

---

## Chapter 9: Control & Optimization Algorithms

This chapter covers the algorithmic approaches for optimizing heating system operation, from simple rules to advanced model predictive control and reinforcement learning.

### 9.1 Rule-Based Control

Traditional heating control relies on deterministic rules:

```python
def rule_based_heating_curve(outdoor_temp, params):
    """
    Calculate flow temperature setpoint from heating curve.
    
    Parameters:
    - outdoor_temp: Current outdoor temperature (°C)
    - params: dict with 'base_temp', 'slope', 'min_flow', 'max_flow'
    """
    flow_temp = params['base_temp'] - params['slope'] * outdoor_temp
    return np.clip(flow_temp, params['min_flow'], params['max_flow'])

def rule_based_night_setback(hour, base_setpoint, setback_reduction=3.0):
    """Apply night setback between 22:00 and 06:00."""
    if 22 <= hour or hour < 6:
        return base_setpoint - setback_reduction
    return base_setpoint
```

Limitations: Rules cannot adapt to changing conditions, forecast information, or multi-objective trade-offs.

### 9.2 Model Predictive Control (MPC)

MPC optimizes control actions over a prediction horizon using a system model.

**Problem formulation:**

$$\min_{u_0, ..., u_{N-1}} \sum_{k=0}^{N-1} \left[ (T_k - T_{setpoint})^2 + \lambda \cdot E_k^2 \right]$$

Subject to:
- System dynamics: $T_{k+1} = f(T_k, u_k, T_{outdoor,k})$
- Comfort constraints: $T_{min} \leq T_k \leq T_{max}$
- Equipment constraints: $0 \leq u_k \leq u_{max}$

Where $T_k$ is indoor temperature, $u_k$ is control action (heating power), $E_k$ is energy consumption, and $\lambda$ balances comfort vs. energy.

**Implementation sketch:**

```python
from scipy.optimize import minimize

def mpc_controller(current_state, weather_forecast, price_forecast,
                   horizon=24, dt=1.0):
    """
    Model Predictive Control for heating system.
    
    Parameters:
    - current_state: dict with 'T_indoor', 'T_storage', etc.
    - weather_forecast: array of outdoor temps for horizon
    - price_forecast: array of electricity prices for horizon
    - horizon: prediction horizon in hours
    - dt: time step in hours
    """
    
    def objective(u):
        """Cost function: energy cost + comfort penalty."""
        T = simulate_building(current_state, u, weather_forecast, dt)
        
        energy_cost = np.sum(u * price_forecast * dt)
        comfort_penalty = np.sum(np.maximum(0, 20 - T) ** 2) * 100
        
        return energy_cost + comfort_penalty
    
    def simulate_building(state, u, T_out, dt):
        """Simple RC building model."""
        T = np.zeros(len(u))
        T[0] = state['T_indoor']
        
        # Thermal parameters (would be identified from data)
        C = 1e7  # Thermal capacitance (J/K)
        UA = 500  # Heat loss coefficient (W/K)
        
        for k in range(len(u) - 1):
            Q_loss = UA * (T[k] - T_out[k])
            Q_heat = u[k] * 1000  # kW to W
            dT = (Q_heat - Q_loss) * dt * 3600 / C
            T[k+1] = T[k] + dT
        
        return T
    
    # Constraints
    bounds = [(0, 50)] * horizon  # 0-50 kW heating power
    
    # Initial guess: constant power
    u0 = np.ones(horizon) * 10
    
    result = minimize(objective, u0, method='SLSQP', bounds=bounds)
    
    return result.x[0]  # Return first control action
```

### 9.3 Reinforcement Learning for HVAC

RL learns optimal control policies through interaction with the environment (or simulator).

**State space** for heating control:

```python
state = {
    'T_indoor': 21.5,           # Indoor temperature (°C)
    'T_outdoor': 5.0,           # Outdoor temperature (°C)
    'T_storage': 55.0,          # Storage tank temperature (°C)
    'hour': 14,                 # Hour of day
    'day_of_week': 2,           # Day of week
    'electricity_price': 0.25,  # Current price (€/kWh)
    'T_outdoor_forecast_6h': 3.0,  # Weather forecast
    'solar_radiation': 150,     # W/m²
}
```

**Action space:**

```python
# Discrete actions
actions = {
    0: 'heating_off',
    1: 'heating_low',      # 30% capacity
    2: 'heating_medium',   # 60% capacity
    3: 'heating_high',     # 100% capacity
}

# Or continuous: heating power in kW
action = 15.5  # kW
```

**Reward function:**

```python
def reward_function(state, action, next_state, params):
    """
    Multi-objective reward balancing comfort, cost, and emissions.
    """
    # Comfort: penalize deviation from setpoint
    T_setpoint = 21.0
    comfort_penalty = -params['w_comfort'] * (next_state['T_indoor'] - T_setpoint) ** 2
    
    # Energy cost
    energy_kwh = action * params['dt']  # action = power in kW
    energy_cost = -params['w_cost'] * energy_kwh * state['electricity_price']
    
    # Emissions (if using carbon intensity signal)
    emissions = -params['w_emissions'] * energy_kwh * state['carbon_intensity']
    
    # Hard constraint: severe penalty for comfort violations
    if next_state['T_indoor'] < 18.0:
        constraint_penalty = -1000
    else:
        constraint_penalty = 0
    
    return comfort_penalty + energy_cost + emissions + constraint_penalty
```

**Training considerations:**
- Simulation environment required (real buildings too slow/risky for exploration)
- Building thermal models (RC networks, data-driven) serve as simulators
- Safe RL techniques constrain exploration to acceptable operating regions
- Transfer learning from simulation to real buildings requires domain adaptation

### 9.4 Multi-Objective Optimization

Heating optimization involves inherent trade-offs:
- Comfort vs. energy cost
- Cost vs. emissions (not always aligned)
- Peak reduction vs. total consumption

**Pareto optimization** finds the set of non-dominated solutions:

```python
from scipy.optimize import minimize

def multi_objective_optimization(params):
    """
    Find Pareto-optimal heating schedules.
    """
    def cost_objective(u):
        return np.sum(u * electricity_prices)
    
    def comfort_objective(u):
        T = simulate_temperatures(u)
        return np.sum((T - T_setpoint) ** 2)
    
    # ε-constraint method: minimize cost subject to comfort constraint
    pareto_front = []
    for comfort_limit in np.linspace(0, 100, 20):
        constraints = {'type': 'ineq', 
                       'fun': lambda u: comfort_limit - comfort_objective(u)}
        
        result = minimize(cost_objective, u0, constraints=constraints)
        if result.success:
            pareto_front.append({
                'cost': cost_objective(result.x),
                'comfort': comfort_objective(result.x),
                'schedule': result.x
            })
    
    return pareto_front
```

### 9.5 Peak Shaving and Load Shifting

**Peak shaving** reduces maximum power demand, critical for Fernwärme Anschlussleistung costs:

```python
def peak_shaving_schedule(base_demand, storage_capacity, 
                          max_charge_rate, max_discharge_rate):
    """
    Optimize storage operation to minimize peak demand.
    """
    n_periods = len(base_demand)
    
    # Decision variables: charge[t], discharge[t], storage_level[t]
    from scipy.optimize import linprog
    
    # Objective: minimize peak (reformulated as linear program)
    # min z subject to: base_demand[t] - discharge[t] + charge[t] <= z for all t
    
    # This requires iterative solution or MILP formulation
    # Simplified heuristic approach:
    
    peak_target = np.percentile(base_demand, 90)
    schedule = np.zeros(n_periods)
    storage = storage_capacity / 2  # Start half full
    
    for t in range(n_periods):
        if base_demand[t] > peak_target and storage > 0:
            # Discharge to shave peak
            discharge = min(base_demand[t] - peak_target, 
                          max_discharge_rate, storage)
            schedule[t] = -discharge
            storage -= discharge
        elif base_demand[t] < peak_target * 0.7 and storage < storage_capacity:
            # Charge during low demand
            charge = min(peak_target * 0.7 - base_demand[t],
                        max_charge_rate, storage_capacity - storage)
            schedule[t] = charge
            storage += charge
    
    return schedule
```

---

## Chapter 10: Supervised Learning Applications

Supervised learning addresses prediction and classification tasks where labeled training data is available.

### 10.1 Regression: Energy Consumption Prediction

**Problem:** Predict daily/hourly energy consumption from building and weather features.

**Feature engineering:**

```python
features = [
    # Weather
    'heating_degree_hours',
    'outdoor_temp_mean',
    'outdoor_temp_min',
    'wind_speed_mean',
    'solar_radiation_sum',
    
    # Calendar
    'is_weekend',
    'is_holiday',
    'month',
    
    # Building characteristics (static)
    'building_area_m2',
    'building_year',
    'insulation_level',  # encoded categorical
    
    # Lagged consumption
    'consumption_lag_1d',
    'consumption_lag_7d',
    'consumption_rolling_7d_mean',
]
```

**Model comparison:**

```python
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

models = {
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.1),
    'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=10),
    'GradientBoosting': GradientBoostingRegressor(n_estimators=100, max_depth=5),
}

tscv = TimeSeriesSplit(n_splits=5)

results = {}
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=tscv, 
                            scoring='neg_root_mean_squared_error')
    results[name] = {
        'rmse_mean': -scores.mean(),
        'rmse_std': scores.std()
    }
```

**COP estimation** for heat pumps requires modeling efficiency as function of operating conditions:

```python
def estimate_cop(T_source, T_sink, model_params):
    """
    Estimate heat pump COP from source and sink temperatures.
    
    Empirical model: COP = a - b * (T_sink - T_source)
    """
    delta_T = T_sink - T_source
    cop = model_params['a'] - model_params['b'] * delta_T
    return np.clip(cop, 1.0, 7.0)  # Physical bounds
```

### 10.2 Classification: Fault Detection

**Problem:** Classify operating states as normal or faulty.

**Label generation** often requires domain expertise or rule-based initial labeling:

```python
def label_faults(df):
    """Generate fault labels from operational data."""
    labels = pd.Series('normal', index=df.index)
    
    # Fault: pump failure (no flow despite demand)
    pump_fault = (df['heat_demand'] > 1) & (df['flow_rate'] < 0.1)
    labels[pump_fault] = 'pump_fault'
    
    # Fault: sensor drift (physically impossible values)
    sensor_fault = (df['vorlauf_temp'] < df['ruecklauf_temp'] - 2)
    labels[sensor_fault] = 'sensor_fault'
    
    # Fault: control error (heating in summer with high outdoor temp)
    control_fault = (df['outdoor_temp'] > 22) & (df['heat_demand'] > 5)
    labels[control_fault] = 'control_fault'
    
    return labels
```

**Imbalanced classification** (faults are rare) requires appropriate techniques:

```python
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, confusion_matrix

# Address class imbalance
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

clf = RandomForestClassifier(n_estimators=100, class_weight='balanced')
clf.fit(X_resampled, y_resampled)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
```

### 10.3 Feature Importance and Interpretability

Regulated energy domains require explainable models.

**Permutation importance:**

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, 
                                n_repeats=10, random_state=42)

importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance_mean': result.importances_mean,
    'importance_std': result.importances_std
}).sort_values('importance_mean', ascending=False)
```

**SHAP values** provide instance-level explanations:

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test, feature_names=feature_names)

# Single prediction explanation
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

---

## Chapter 11: Unsupervised Learning Applications

Unsupervised methods discover structure in data without labeled examples.

### 11.1 Clustering Building Portfolios

**Problem:** Group buildings by consumption patterns for targeted optimization strategies.

**Feature extraction** for building-level clustering:

```python
def extract_building_features(building_df):
    """Extract features characterizing a building's energy profile."""
    return {
        'annual_consumption_kwh_m2': building_df['consumption'].sum() / building_df['area'].iloc[0],
        'peak_to_mean_ratio': building_df['power'].max() / building_df['power'].mean(),
        'heating_season_share': (building_df[building_df['outdoor_temp'] < 15]['consumption'].sum() / 
                                 building_df['consumption'].sum()),
        'night_share': (building_df[building_df.index.hour.isin(range(22, 6))]['consumption'].sum() /
                       building_df['consumption'].sum()),
        'weekend_share': (building_df[building_df.index.dayofweek >= 5]['consumption'].sum() /
                         building_df['consumption'].sum()),
        'weather_sensitivity': calculate_weather_sensitivity(building_df),
    }
```

**K-Means clustering:**

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(building_features)

# Determine optimal k via elbow method or silhouette score
from sklearn.metrics import silhouette_score

silhouette_scores = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    silhouette_scores.append(silhouette_score(X_scaled, labels))

optimal_k = np.argmax(silhouette_scores) + 2
```

**Cluster interpretation:**

```python
# Analyze cluster characteristics
cluster_profiles = building_features.groupby('cluster').mean()

# Example clusters for housing portfolio:
# Cluster 0: "Efficient new builds" - low consumption, low weather sensitivity
# Cluster 1: "Poorly insulated old stock" - high consumption, high weather sensitivity  
# Cluster 2: "Oversized systems" - high peak-to-mean ratio, moderate consumption
```

### 11.2 Dimensionality Reduction

**PCA** for sensor data compression and visualization:

```python
from sklearn.decomposition import PCA

# Reduce high-dimensional sensor data (50+ sensors) to principal components
pca = PCA(n_components=0.95)  # Retain 95% variance
X_reduced = pca.fit_transform(X_sensors)

print(f"Reduced from {X_sensors.shape[1]} to {X_reduced.shape[1]} dimensions")
print(f"Explained variance ratios: {pca.explained_variance_ratio_[:5]}")
```

**UMAP** for non-linear dimensionality reduction and visualization:

```python
import umap

reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='euclidean')
embedding = reducer.fit_transform(X_scaled)

# Visualize building portfolio in 2D
plt.scatter(embedding[:, 0], embedding[:, 1], c=cluster_labels, cmap='viridis')
```

### 11.3 Identifying Operational Regimes

**Hidden Markov Models** identify distinct operating states:

```python
from hmmlearn import hmm

# Fit HMM to identify heating system operating regimes
model = hmm.GaussianHMM(n_components=4, covariance_type='full', n_iter=100)
model.fit(X_operational)

# Decode most likely state sequence
states = model.predict(X_operational)

# States might correspond to:
# State 0: Off/standby
# State 1: Low-load operation
# State 2: Normal heating
# State 3: Peak demand / recovery mode
```

**Change point detection** identifies regime transitions:

```python
import ruptures as rpt

# Detect changes in operational patterns
algo = rpt.Pelt(model='rbf').fit(signal)
change_points = algo.predict(pen=10)

# Change points may indicate:
# - Control parameter modifications
# - Equipment faults or repairs
# - Seasonal transitions
# - Occupancy changes
```

---

*End of Part II*
