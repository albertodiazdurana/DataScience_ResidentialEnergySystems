# Green Fusion Technical Gaps Study Guide
## Advanced Concepts for Energy Optimization

**Purpose:** Bridge your retail forecasting experience to energy optimization domain  
**Level:** Advanced (assumes data science and energy engineering background)

---

## 1. Reinforcement Learning for Heating Control

### 1.1 Why RL for Heating Systems?

Traditional control (PID, rule-based) has fundamental limitations:
- **Reactive only:** Responds to current error, no anticipation
- **No learning:** Same parameters regardless of building behavior
- **Single objective:** Typically just temperature tracking

RL addresses these by learning optimal control policies through interaction:

```
Agent (Controller) ←→ Environment (Building + Heating System)
     ↓                        ↓
   Action                   State
(supply temp,            (indoor temp,
 on/off)                 outdoor temp,
                         occupancy)
     ↓                        ↓
                    Reward
              (comfort - λ·energy)
```

### 1.2 RL Formulation for Heating Control

**State space S:**
```python
state = [
    T_indoor,           # Current indoor temperature
    T_outdoor,          # Current outdoor temperature
    T_supply,           # Current supply water temperature
    humidity,           # Indoor humidity
    occupancy,          # Binary or count
    hour_of_day,        # Cyclic encoding (sin/cos)
    day_of_week,        # Cyclic encoding
    weather_forecast,   # Next N hours outdoor temp
    electricity_price,  # Current and forecasted
]
```

**Action space A:**
```python
# Continuous actions
action = [
    T_supply_setpoint,  # Target supply water temperature [100-180°F]
    heating_mode,       # On/off or modulation level [0-1]
]

# Or discrete actions
actions = {
    0: "maintain",
    1: "increase_5_degrees",
    2: "decrease_5_degrees",
    3: "boost_mode",
    4: "night_setback",
}
```

**Reward function (critical design choice):**
```python
def reward(state, action, next_state):
    # Comfort component
    T_target = 21.0  # °C
    comfort_penalty = -alpha * (next_state.T_indoor - T_target)**2
    
    # Energy component
    energy_cost = -beta * get_energy_consumption(action)
    
    # Constraint violations
    if next_state.T_indoor < 19.0 or next_state.T_indoor > 23.0:
        constraint_penalty = -gamma * 100  # Hard penalty
    else:
        constraint_penalty = 0
    
    return comfort_penalty + energy_cost + constraint_penalty
```

### 1.3 Key RL Algorithms for HVAC

**Model-Free Approaches (most common in research):**

| Algorithm | Strengths | Weaknesses | Best For |
|-----------|-----------|------------|----------|
| **DQN** | Handles discrete actions well | Continuous actions need discretization | Simple on/off control |
| **DDPG** | Continuous actions natively | Sensitive to hyperparameters | Fine-grained setpoint control |
| **SAC** | Entropy regularization prevents collapse | More complex | Robust exploration |
| **TD3** | Twin critics reduce overestimation | Delayed updates add complexity | Stable continuous control |
| **PPO** | Sample efficient, stable training | Slightly worse asymptotic performance | Production deployment |

**Model-Based Approaches:**
- Learn a transition model: `P(s'|s,a)`
- Plan using the learned model
- More sample efficient but model errors compound

### 1.4 The Sim-to-Real Challenge

**Why simulation is necessary:**
- Can't explore randomly on real buildings (comfort violations)
- Need millions of interactions for training
- Safety constraints during learning

**Simulation tools:**
- **EnergyPlus:** DOE building simulation (most common)
- **TRNSYS:** Transient systems simulation
- **Modelica/Dymola:** Equation-based modeling
- **Sinergym:** RL-specific wrapper for EnergyPlus

**Transfer learning challenge:**
```
Simulation Model → Trained Policy → Real Building
                                         ↓
                          Domain gap causes performance drop
```

**Solutions:**
1. **Domain randomization:** Vary simulation parameters during training
2. **System identification:** Calibrate simulator to real building
3. **Offline RL:** Learn from historical real data without exploration
4. **Hybrid:** Pre-train in simulation, fine-tune on real building with constraints

### 1.5 RL vs MPC for Heating

| Aspect | RL | MPC |
|--------|-----|-----|
| Model requirement | Learned implicitly | Explicit physics model |
| Computational cost at inference | Low (forward pass) | High (optimization each step) |
| Handling constraints | Soft (via reward) | Hard (optimization constraints) |
| Adaptability | Can learn from experience | Requires model updates |
| Interpretability | Black box | Explainable optimization |
| Sample efficiency | Poor (needs lots of data) | Good (uses physics) |

**Green Fusion likely uses:** Hybrid approach—MPC for baseline control with RL for parameter tuning or residual policy.

### 1.6 Pseudo-Code: Simple Q-Learning for Heating

```python
class HeatingRLAgent:
    def __init__(self, state_dim, action_dim, lr=0.001):
        self.q_network = build_mlp(state_dim, action_dim)
        self.target_network = build_mlp(state_dim, action_dim)
        self.optimizer = Adam(lr=lr)
        self.replay_buffer = ReplayBuffer(capacity=100000)
        self.gamma = 0.99  # Discount factor
        
    def select_action(self, state, epsilon):
        """Epsilon-greedy action selection"""
        if random.random() < epsilon:
            return random.choice(self.action_space)
        else:
            q_values = self.q_network(state)
            return np.argmax(q_values)
    
    def train_step(self, batch_size=64):
        """One step of Q-learning update"""
        states, actions, rewards, next_states, dones = (
            self.replay_buffer.sample(batch_size)
        )
        
        # Compute target Q-values
        with torch.no_grad():
            next_q = self.target_network(next_states)
            max_next_q = next_q.max(dim=1)[0]
            targets = rewards + self.gamma * max_next_q * (1 - dones)
        
        # Current Q-values
        current_q = self.q_network(states)
        current_q_actions = current_q.gather(1, actions.unsqueeze(1))
        
        # Loss and update
        loss = F.mse_loss(current_q_actions.squeeze(), targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
    
    def update_target_network(self):
        """Soft update of target network"""
        for target_param, param in zip(
            self.target_network.parameters(),
            self.q_network.parameters()
        ):
            target_param.data.copy_(
                0.99 * target_param.data + 0.01 * param.data
            )
```

### 1.7 How to Discuss RL in Interview

**Your honest position:**
> "I haven't implemented RL in production, but I understand the framework well. In my retail forecasting project, I worked with sequential decision problems where current predictions inform future ones—that's conceptually similar to RL's temporal credit assignment. The key difference is that RL learns a policy through environment interaction rather than supervised labels."

**Bridge from your experience:**
- Your autoregressive forecasting = sequential decision making
- Your multi-step forecast = planning horizon concept
- Your ablation testing = reward function design intuition
- Your LSTM temporal modeling = value function approximation

---

## 2. Unsupervised Learning for Building Energy

### 2.1 Applications in Heating Systems

**1. Building/Zone Clustering:**
Group similar buildings for:
- Transfer learning (train on cluster, deploy to new building)
- Identifying outliers (buildings that don't fit any cluster)
- Tailored heating curves per cluster

**2. Anomaly Detection:**
- Sensor failures (stuck values, drift)
- Equipment malfunctions (inefficient operation)
- Occupancy anomalies (unexpected patterns)
- Energy waste detection

**3. Load Profile Segmentation:**
- Identify typical daily/weekly patterns
- Detect deviations from normal operation
- Inform demand response strategies

### 2.2 Clustering Approaches

**K-Means for Building Profiles:**
```python
def cluster_building_profiles(buildings_df, n_clusters=5):
    """
    Cluster buildings by their thermal characteristics
    
    Features might include:
    - Average heat demand per degree-day
    - Response time to setpoint changes
    - Weekend vs weekday ratio
    - Night setback effectiveness
    """
    # Extract features per building
    features = []
    for building_id in buildings_df['building_id'].unique():
        building_data = buildings_df[buildings_df['building_id'] == building_id]
        
        feature_vector = [
            building_data['heat_demand'].mean(),
            building_data['heat_demand'].std(),
            calc_degree_day_coefficient(building_data),
            calc_thermal_time_constant(building_data),
            calc_weekend_weekday_ratio(building_data),
        ]
        features.append(feature_vector)
    
    features = np.array(features)
    features_scaled = StandardScaler().fit_transform(features)
    
    # Cluster
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(features_scaled)
    
    return labels, kmeans

def calc_thermal_time_constant(df):
    """
    Estimate building thermal inertia from step response
    Time constant = time to reach 63% of final temperature change
    """
    # Find setpoint changes
    setpoint_changes = df[df['setpoint'].diff().abs() > 1]
    
    time_constants = []
    for idx in setpoint_changes.index:
        # Track temperature response after setpoint change
        response = df.loc[idx:idx+pd.Timedelta(hours=6), 'indoor_temp']
        initial = response.iloc[0]
        final = response.iloc[-1]
        target_63pct = initial + 0.63 * (final - initial)
        
        # Find when temperature crosses 63% threshold
        crossing = response[response >= target_63pct].index[0]
        time_constant = (crossing - idx).total_seconds() / 3600  # hours
        time_constants.append(time_constant)
    
    return np.median(time_constants) if time_constants else np.nan
```

### 2.3 Anomaly Detection Methods

**Local Outlier Factor (LOF):**
Density-based approach—anomalies have lower density than neighbors.

```python
def detect_sensor_anomalies(sensor_df, contamination=0.05):
    """
    Detect anomalous sensor readings using LOF
    
    Args:
        sensor_df: DataFrame with columns [timestamp, temperature, humidity, ...]
        contamination: Expected proportion of anomalies
    
    Returns:
        DataFrame with anomaly labels
    """
    # Create feature matrix
    features = sensor_df[['temperature', 'humidity', 'supply_temp']].values
    
    # Add temporal features (hour, day_of_week as cyclic)
    features = np.column_stack([
        features,
        np.sin(2 * np.pi * sensor_df['timestamp'].dt.hour / 24),
        np.cos(2 * np.pi * sensor_df['timestamp'].dt.hour / 24),
    ])
    
    # Scale features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Fit LOF
    lof = LocalOutlierFactor(
        n_neighbors=20,
        contamination=contamination,
        novelty=False
    )
    labels = lof.fit_predict(features_scaled)
    
    # -1 = anomaly, 1 = normal
    sensor_df['is_anomaly'] = labels == -1
    sensor_df['lof_score'] = -lof.negative_outlier_factor_
    
    return sensor_df
```

**Isolation Forest:**
Tree-based approach—anomalies are easier to isolate (shorter path length).

```python
def detect_energy_anomalies_iforest(energy_df, contamination=0.05):
    """
    Detect anomalous energy consumption patterns
    """
    # Create features
    features = create_energy_features(energy_df)
    
    # Fit Isolation Forest
    iforest = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42
    )
    
    labels = iforest.fit_predict(features)
    scores = iforest.decision_function(features)
    
    energy_df['is_anomaly'] = labels == -1
    energy_df['anomaly_score'] = -scores  # Higher = more anomalous
    
    return energy_df

def create_energy_features(df):
    """
    Feature engineering for energy anomaly detection
    """
    features = pd.DataFrame()
    
    # Current consumption normalized by degree-day
    features['consumption_per_dd'] = (
        df['energy'] / df['heating_degree_days'].clip(lower=0.1)
    )
    
    # Deviation from expected based on outdoor temp
    expected = df.groupby(pd.cut(df['outdoor_temp'], bins=10))['energy'].transform('mean')
    features['deviation_from_expected'] = (df['energy'] - expected) / expected.clip(lower=0.1)
    
    # Rate of change
    features['consumption_change'] = df['energy'].pct_change()
    
    # Comparison to same hour previous week
    features['vs_last_week'] = df['energy'] / df['energy'].shift(24*7).clip(lower=0.1)
    
    return features.fillna(0)
```

**Autoencoder for Anomaly Detection:**
Learn compressed representation—high reconstruction error = anomaly.

```python
class EnergyAutoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim=8):
        super().__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, latent_dim),
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_dim),
        )
    
    def forward(self, x):
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return reconstructed
    
    def get_anomaly_score(self, x):
        """Reconstruction error as anomaly score"""
        reconstructed = self.forward(x)
        return F.mse_loss(reconstructed, x, reduction='none').mean(dim=1)


def train_autoencoder_anomaly_detector(train_data, epochs=100):
    """
    Train autoencoder on NORMAL data only
    High reconstruction error on new data = anomaly
    """
    model = EnergyAutoencoder(input_dim=train_data.shape[1])
    optimizer = Adam(model.parameters(), lr=0.001)
    
    train_loader = DataLoader(
        TensorDataset(torch.FloatTensor(train_data)),
        batch_size=64,
        shuffle=True
    )
    
    for epoch in range(epochs):
        total_loss = 0
        for batch in train_loader:
            x = batch[0]
            reconstructed = model(x)
            loss = F.mse_loss(reconstructed, x)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
    
    # Determine threshold from training data
    with torch.no_grad():
        train_scores = model.get_anomaly_score(torch.FloatTensor(train_data))
        threshold = train_scores.mean() + 3 * train_scores.std()
    
    return model, threshold.item()
```

### 2.4 Stuck Sensor Detection

```python
def detect_stuck_sensors(df, window='1H', min_variance=0.01):
    """
    Detect sensors that show no variation (stuck at constant value)
    
    Args:
        df: DataFrame with sensor columns
        window: Rolling window for variance calculation
        min_variance: Threshold below which sensor is considered stuck
    
    Returns:
        Dictionary of sensor: list of stuck periods
    """
    stuck_periods = {}
    
    for col in df.select_dtypes(include=[np.number]).columns:
        # Calculate rolling variance
        rolling_var = df[col].rolling(window).var()
        
        # Find periods where variance is below threshold
        is_stuck = rolling_var < min_variance
        
        # Group consecutive stuck periods
        stuck_groups = (is_stuck != is_stuck.shift()).cumsum()
        stuck_ranges = df[is_stuck].groupby(stuck_groups).agg(
            start=('index', 'first'),
            end=('index', 'last'),
            value=(col, 'mean'),
            duration=('index', lambda x: (x.max() - x.min()).total_seconds() / 3600)
        )
        
        # Filter to significant stuck periods (> 1 hour)
        significant = stuck_ranges[stuck_ranges['duration'] > 1]
        
        if len(significant) > 0:
            stuck_periods[col] = significant.to_dict('records')
    
    return stuck_periods
```

### 2.5 Bridge from Your Experience

**Your retail project has transferable concepts:**

| Your Experience | Unsupervised Energy Application |
|-----------------|--------------------------------|
| Store clustering by sales patterns | Building clustering by thermal behavior |
| Identifying sparse data (0.9% active) | Identifying inactive/stuck sensors |
| Holiday effect detection | Occupancy pattern anomaly detection |
| Family groupings | Building type segmentation |

**How to discuss:**
> "In my retail project, I analyzed store-item combinations and found that only 0.9% contained active sales data. This taught me to distinguish between genuine anomalies and expected sparsity. For heating systems, similar logic applies—a sensor showing zero variation might be stuck, or the heating might genuinely be off during summer."

---

## 3. Model Predictive Control (MPC)

### 3.1 MPC Fundamentals

MPC solves an optimization problem at each timestep:

```
At time t:
    Minimize: J = Σ[k=0 to N] (cost_energy(k) + cost_discomfort(k))
    Subject to:
        x(k+1) = f(x(k), u(k))           # System dynamics
        T_min ≤ T_indoor(k) ≤ T_max      # Comfort constraints
        u_min ≤ u(k) ≤ u_max             # Actuator limits
    
    Apply: u(0) only, then re-solve at t+1
```

### 3.2 Building Thermal Model (RC Model)

Buildings are often modeled as RC (resistor-capacitor) networks:

```
                    R_wall
    T_outdoor ───/\/\/\/───┬─── T_indoor
                           │
                           C (thermal mass)
                           │
                          ═╧═
                           
    Heat input: Q_heating, Q_solar, Q_internal
```

**Mathematical form:**
```
C * dT_indoor/dt = (T_outdoor - T_indoor)/R_wall + Q_heating + Q_solar + Q_internal
```

**Discrete-time state-space:**
```python
def thermal_model(x, u, d, params):
    """
    Simple RC building model
    
    State x: [T_indoor, T_wall]
    Input u: [Q_heating]
    Disturbance d: [T_outdoor, Q_solar, Q_internal]
    
    Returns: next state
    """
    T_indoor, T_wall = x
    Q_heating = u[0]
    T_outdoor, Q_solar, Q_internal = d
    
    C_air = params['C_air']       # Air thermal capacity
    C_wall = params['C_wall']     # Wall thermal capacity
    R_wall = params['R_wall']     # Wall thermal resistance
    R_window = params['R_window'] # Window thermal resistance
    
    # Heat flows
    Q_wall = (T_wall - T_indoor) / R_wall
    Q_window = (T_outdoor - T_indoor) / R_window
    
    # Temperature changes
    dT_indoor = (Q_wall + Q_window + Q_heating + Q_solar + Q_internal) / C_air
    dT_wall = ((T_outdoor - T_wall) / R_wall - Q_wall) / C_wall
    
    # Euler integration
    dt = params['dt']  # timestep in hours
    T_indoor_next = T_indoor + dT_indoor * dt
    T_wall_next = T_wall + dT_wall * dt
    
    return np.array([T_indoor_next, T_wall_next])
```

### 3.3 MPC Implementation

```python
class HeatingMPC:
    def __init__(self, model, horizon=24, dt=1.0):
        """
        Args:
            model: Building thermal model function
            horizon: Prediction horizon (hours)
            dt: Timestep (hours)
        """
        self.model = model
        self.horizon = horizon
        self.dt = dt
        self.n_steps = int(horizon / dt)
        
        # Cost weights
        self.w_energy = 1.0
        self.w_comfort = 10.0
        self.T_target = 21.0
        self.T_min = 19.0
        self.T_max = 23.0
        
    def objective(self, u_sequence, x0, disturbances, energy_prices):
        """
        Cost function to minimize
        
        Args:
            u_sequence: Array of control actions [n_steps]
            x0: Initial state
            disturbances: Predicted disturbances [n_steps, n_disturbances]
            energy_prices: Electricity prices [n_steps]
        
        Returns:
            Total cost
        """
        cost = 0
        x = x0.copy()
        
        for k in range(self.n_steps):
            # Simulate one step
            u = np.array([u_sequence[k]])
            d = disturbances[k]
            x = self.model(x, u, d, self.params)
            
            # Energy cost
            cost += self.w_energy * u_sequence[k] * energy_prices[k]
            
            # Comfort cost (quadratic deviation from target)
            T_indoor = x[0]
            cost += self.w_comfort * (T_indoor - self.T_target)**2
            
            # Constraint violations (soft constraints with high penalty)
            if T_indoor < self.T_min:
                cost += 1000 * (self.T_min - T_indoor)**2
            if T_indoor > self.T_max:
                cost += 1000 * (T_indoor - self.T_max)**2
        
        return cost
    
    def solve(self, x0, weather_forecast, energy_prices):
        """
        Solve MPC optimization problem
        
        Returns:
            Optimal control action for current timestep
        """
        # Initial guess: constant heating
        u0 = np.ones(self.n_steps) * 0.5
        
        # Bounds on control
        bounds = [(0, 1) for _ in range(self.n_steps)]
        
        # Prepare disturbances from weather forecast
        disturbances = self.prepare_disturbances(weather_forecast)
        
        # Optimize
        result = minimize(
            self.objective,
            u0,
            args=(x0, disturbances, energy_prices),
            method='SLSQP',
            bounds=bounds
        )
        
        # Return first action only (receding horizon)
        return result.x[0]
    
    def prepare_disturbances(self, weather_forecast):
        """Convert weather forecast to disturbance array"""
        disturbances = []
        for k in range(self.n_steps):
            T_outdoor = weather_forecast['temperature'][k]
            Q_solar = weather_forecast['solar_radiation'][k] * self.params['solar_gain']
            Q_internal = self.params['internal_gains']  # Could be occupancy-dependent
            disturbances.append([T_outdoor, Q_solar, Q_internal])
        return np.array(disturbances)
```

### 3.4 MPC vs Rule-Based Control

```python
def compare_controllers(building_model, weather_data, n_days=7):
    """
    Compare MPC vs simple rule-based control
    """
    results = {'mpc': [], 'rule_based': []}
    
    for controller_type in ['mpc', 'rule_based']:
        x = np.array([20.0, 18.0])  # Initial state
        total_energy = 0
        total_discomfort = 0
        
        for hour in range(n_days * 24):
            T_outdoor = weather_data['temperature'][hour]
            
            if controller_type == 'mpc':
                # MPC uses forecast
                forecast = weather_data.iloc[hour:hour+24]
                u = mpc_controller.solve(x, forecast, energy_prices[hour:hour+24])
            else:
                # Rule-based: heating curve
                T_indoor = x[0]
                T_setpoint = 21.0
                if T_indoor < T_setpoint - 0.5:
                    u = min(1.0, (T_setpoint - T_indoor) / 2.0)
                elif T_indoor > T_setpoint + 0.5:
                    u = 0.0
                else:
                    u = 0.3
            
            # Simulate
            d = [T_outdoor, weather_data['solar'][hour], 0.5]
            x = building_model(x, [u], d, params)
            
            # Track metrics
            total_energy += u * energy_prices[hour]
            total_discomfort += abs(x[0] - 21.0)
        
        results[controller_type] = {
            'energy_cost': total_energy,
            'discomfort': total_discomfort
        }
    
    return results
```

### 3.5 Key MPC Concepts for Interview

**Prediction horizon:** How far ahead to optimize (typically 6-48 hours for buildings)

**Control horizon:** How many future actions to optimize (can be shorter than prediction)

**Receding horizon:** Only apply first action, then re-solve—handles model uncertainty

**Soft vs hard constraints:**
- Hard: Must never violate (equipment limits)
- Soft: Penalty for violation (comfort bounds)

**Disturbance forecasting:** MPC quality depends on accurate forecasts (weather, occupancy, prices)

---

## 4. Multi-Objective Optimization

### 4.1 The Comfort-Energy Trade-off

In heating systems, objectives conflict:
- **Minimize energy consumption** → Lower temperatures, less heating
- **Maximize comfort** → Stable comfortable temperatures
- **Minimize cost** → Shift heating to cheap electricity periods
- **Minimize emissions** → Use low-carbon energy sources

No single solution optimizes all—need Pareto front.

### 4.2 Pareto Optimality

```
Energy Consumption
       ↑
       │     ×  ×     (dominated solutions)
       │   ×   ×
       │  ●━━━━●━━━●   ← Pareto front
       │ ●           ●
       │●             ●
       └────────────────→ Thermal Discomfort
       
● = Pareto optimal (no solution better in ALL objectives)
× = Dominated (exists a solution better in all objectives)
```

**Solution is Pareto optimal if:** No other solution improves one objective without worsening another.

### 4.3 NSGA-II for Building Optimization

```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize

class HeatingOptimizationProblem(Problem):
    def __init__(self, building_model, weather_forecast):
        # Decision variables: heating setpoints for each hour
        n_hours = 24
        super().__init__(
            n_var=n_hours,          # Number of decision variables
            n_obj=2,                # Number of objectives
            n_constr=n_hours,       # Number of constraints
            xl=np.ones(n_hours) * 16,   # Lower bound (°C)
            xu=np.ones(n_hours) * 24,   # Upper bound (°C)
        )
        self.building_model = building_model
        self.weather = weather_forecast
    
    def _evaluate(self, X, out, *args, **kwargs):
        """
        Evaluate population of solutions
        
        X: Array of shape (pop_size, n_var)
        """
        n_solutions = X.shape[0]
        
        # Objectives
        f1 = np.zeros(n_solutions)  # Energy consumption
        f2 = np.zeros(n_solutions)  # Thermal discomfort
        
        # Constraints (temperature bounds)
        g = np.zeros((n_solutions, self.n_constr))
        
        for i in range(n_solutions):
            setpoints = X[i]
            energy, discomfort, temps = self.simulate(setpoints)
            
            f1[i] = energy
            f2[i] = discomfort
            
            # Constraint: temperature must stay in comfort band
            for j, T in enumerate(temps):
                g[i, j] = max(0, 19 - T) + max(0, T - 23)  # Violation
        
        out["F"] = np.column_stack([f1, f2])
        out["G"] = g
    
    def simulate(self, setpoints):
        """Run building simulation with given setpoints"""
        x = np.array([20.0, 18.0])
        total_energy = 0
        total_discomfort = 0
        temperatures = []
        
        for hour, setpoint in enumerate(setpoints):
            # PI control to track setpoint
            T_indoor = x[0]
            error = setpoint - T_indoor
            u = np.clip(0.5 + 0.2 * error, 0, 1)
            
            # Simulate
            d = [self.weather['T_outdoor'][hour], 
                 self.weather['solar'][hour], 0.5]
            x = self.building_model(x, [u], d, params)
            
            total_energy += u
            total_discomfort += abs(T_indoor - 21.0)
            temperatures.append(x[0])
        
        return total_energy, total_discomfort, temperatures


def run_optimization():
    problem = HeatingOptimizationProblem(building_model, weather_forecast)
    
    algorithm = NSGA2(
        pop_size=100,
        eliminate_duplicates=True
    )
    
    result = minimize(
        problem,
        algorithm,
        ('n_gen', 100),
        seed=42,
        verbose=True
    )
    
    # result.F contains Pareto front objectives
    # result.X contains corresponding decision variables
    return result
```

### 4.4 Weighted Sum Approach (Simpler)

```python
def weighted_optimization(weights, building_sim, weather):
    """
    Single-objective optimization with weighted objectives
    
    Args:
        weights: dict with 'energy', 'comfort', 'cost' weights
    """
    def objective(setpoints):
        energy, discomfort, cost = building_sim(setpoints, weather)
        
        return (
            weights['energy'] * energy +
            weights['comfort'] * discomfort +
            weights['cost'] * cost
        )
    
    # Optimize
    result = minimize(
        objective,
        x0=np.ones(24) * 21,
        bounds=[(16, 24)] * 24,
        method='SLSQP'
    )
    
    return result.x
```

### 4.5 Bridge from Your Experience

Your project touched multi-objective concepts:

| Your Experience | Multi-Objective Parallel |
|-----------------|-------------------------|
| RMSE vs MAE trade-off | Energy vs comfort trade-off |
| Overfitting ratio monitoring | Constraint satisfaction |
| Feature count vs performance | Complexity vs benefit |
| DEC-016: temporal consistency vs data volume | Multiple competing objectives |

**How to discuss:**
> "Multi-objective optimization is about finding the best trade-offs when goals conflict. In my project, I faced this when deciding between model complexity and performance—more features improved training metrics but some degraded test performance. The same logic applies to heating: more heating improves comfort but increases energy use. Pareto fronts help visualize these trade-offs so stakeholders can make informed decisions."

---

## 5. API Technologies (GraphQL, REST)

### 5.1 Why Green Fusion Needs APIs

Green Fusion's architecture likely includes:
- **Green Box hardware** → Sends sensor data to cloud
- **Cloud platform** → Processes data, runs ML models
- **Customer dashboards** → Display metrics, allow configuration
- **Third-party integrations** → Weather services, energy markets

APIs enable this communication.

### 5.2 REST vs GraphQL

| Aspect | REST | GraphQL |
|--------|------|---------|
| Data fetching | Multiple endpoints | Single endpoint, specify exactly what you need |
| Over-fetching | Common (get full objects) | Avoided (request specific fields) |
| Under-fetching | Common (need multiple calls) | Avoided (nested queries) |
| Versioning | URL-based (/api/v1/) | Schema evolution |
| Caching | HTTP caching | More complex |
| Best for | Simple CRUD, caching important | Complex nested data, mobile apps |

### 5.3 GraphQL Example for Building Data

```graphql
# Schema definition
type Building {
  id: ID!
  name: String!
  address: String!
  zones: [Zone!]!
  currentTemperature: Float
  heatingStatus: HeatingStatus!
  energyConsumption(period: TimePeriod!): EnergyData!
}

type Zone {
  id: ID!
  name: String!
  currentTemp: Float!
  setpoint: Float!
  occupancy: Int
}

type EnergyData {
  total: Float!
  breakdown: [EnergyBreakdown!]!
  comparison: ComparisonData
}

type Query {
  building(id: ID!): Building
  buildings(filter: BuildingFilter): [Building!]!
  anomalies(buildingId: ID!, since: DateTime!): [Anomaly!]!
}

type Mutation {
  updateSetpoint(zoneId: ID!, temperature: Float!): Zone!
  scheduleHeating(buildingId: ID!, schedule: ScheduleInput!): Schedule!
}

# Example query
query GetBuildingOverview($id: ID!) {
  building(id: $id) {
    name
    currentTemperature
    heatingStatus {
      mode
      supplyTemperature
    }
    zones {
      name
      currentTemp
      setpoint
    }
    energyConsumption(period: LAST_24H) {
      total
      breakdown {
        hour
        consumption
      }
    }
  }
}
```

### 5.4 Python GraphQL Client

```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class BuildingAPIClient:
    def __init__(self, endpoint, api_key):
        transport = RequestsHTTPTransport(
            url=endpoint,
            headers={'Authorization': f'Bearer {api_key}'}
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
    
    def get_building_data(self, building_id):
        query = gql("""
            query GetBuilding($id: ID!) {
                building(id: $id) {
                    name
                    currentTemperature
                    zones {
                        id
                        name
                        currentTemp
                        setpoint
                    }
                }
            }
        """)
        
        result = self.client.execute(query, variable_values={'id': building_id})
        return result['building']
    
    def update_setpoint(self, zone_id, temperature):
        mutation = gql("""
            mutation UpdateSetpoint($zoneId: ID!, $temp: Float!) {
                updateSetpoint(zoneId: $zoneId, temperature: $temp) {
                    id
                    setpoint
                }
            }
        """)
        
        result = self.client.execute(
            mutation, 
            variable_values={'zoneId': zone_id, 'temp': temperature}
        )
        return result['updateSetpoint']
```

### 5.5 REST Example

```python
import requests

class BuildingRESTClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {api_key}'}
    
    def get_building(self, building_id):
        response = requests.get(
            f'{self.base_url}/buildings/{building_id}',
            headers=self.headers
        )
        return response.json()
    
    def get_building_zones(self, building_id):
        # Separate call needed for zones
        response = requests.get(
            f'{self.base_url}/buildings/{building_id}/zones',
            headers=self.headers
        )
        return response.json()
    
    def update_setpoint(self, zone_id, temperature):
        response = requests.patch(
            f'{self.base_url}/zones/{zone_id}',
            headers=self.headers,
            json={'setpoint': temperature}
        )
        return response.json()
```

---

## 6. Testing Frameworks

### 6.1 Why Testing Matters for ML Systems

ML systems have unique testing challenges:
- **Data drift:** Model performance degrades as data changes
- **Non-determinism:** Random seeds, floating-point precision
- **Complex dependencies:** Feature engineering, preprocessing
- **Silent failures:** Wrong predictions don't crash

### 6.2 Testing Pyramid for ML

```
                    ┌─────────────┐
                    │   E2E       │  ← Full pipeline tests
                   ─┴─────────────┴─
                  ┌─────────────────┐
                  │  Integration    │  ← Component interaction
                 ─┴─────────────────┴─
                ┌───────────────────────┐
                │     Unit Tests        │  ← Individual functions
               ─┴───────────────────────┴─
```

### 6.3 Unit Tests for Data Science

```python
import pytest
import numpy as np
import pandas as pd

class TestFeatureEngineering:
    
    def test_lag_features_correct_shift(self):
        """Lag features should shift values correctly"""
        df = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=5, freq='H'),
            'value': [1, 2, 3, 4, 5]
        })
        df = df.set_index('timestamp')
        
        result = create_lag_features(df, 'value', lags=[1, 2])
        
        assert result['value_lag_1'].iloc[1] == 1
        assert result['value_lag_2'].iloc[2] == 1
        assert pd.isna(result['value_lag_1'].iloc[0])
    
    def test_lag_features_preserves_length(self):
        """Lag features should not change dataframe length"""
        df = pd.DataFrame({'value': range(100)})
        result = create_lag_features(df, 'value', lags=[1, 7, 14])
        
        assert len(result) == len(df)
    
    def test_rolling_mean_window_size(self):
        """Rolling mean should use correct window"""
        df = pd.DataFrame({'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
        result = create_rolling_features(df, 'value', windows=[3])
        
        # First 2 values should be NaN (window=3)
        assert pd.isna(result['value_rolling_mean_3'].iloc[0])
        assert pd.isna(result['value_rolling_mean_3'].iloc[1])
        # Third value should be mean of first 3
        assert result['value_rolling_mean_3'].iloc[2] == 2.0


class TestTemporalSplit:
    
    def test_no_future_leakage(self):
        """Train data should not contain dates after test start"""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100),
            'value': range(100)
        })
        df = df.set_index('date')
        
        test_start = pd.Timestamp('2024-03-01')
        train, test = temporal_train_test_split(df, test_start, gap_days=7)
        
        assert train.index.max() < test_start - pd.Timedelta(days=7)
        assert test.index.min() >= test_start
    
    def test_gap_enforced(self):
        """Gap period should have no data"""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100),
            'value': range(100)
        })
        df = df.set_index('date')
        
        test_start = pd.Timestamp('2024-03-01')
        gap_days = 7
        train, test = temporal_train_test_split(df, test_start, gap_days)
        
        gap_start = test_start - pd.Timedelta(days=gap_days)
        
        # No data in gap period
        assert len(train[train.index >= gap_start]) == 0
        assert len(test[test.index < test_start]) == 0


class TestModelPredictions:
    
    @pytest.fixture
    def trained_model(self):
        """Fixture providing a trained model"""
        # Load or train model
        return load_model('test_model.pkl')
    
    def test_predictions_in_valid_range(self, trained_model):
        """Predictions should be within reasonable bounds"""
        test_features = load_test_features()
        predictions = trained_model.predict(test_features)
        
        # Temperature predictions should be between 15-30°C
        assert np.all(predictions >= 15)
        assert np.all(predictions <= 30)
    
    def test_predictions_deterministic(self, trained_model):
        """Same input should give same output"""
        test_features = load_test_features()
        
        pred1 = trained_model.predict(test_features)
        pred2 = trained_model.predict(test_features)
        
        np.testing.assert_array_almost_equal(pred1, pred2)
    
    def test_model_handles_missing_features(self, trained_model):
        """Model should handle or reject missing features gracefully"""
        test_features = load_test_features()
        test_features_with_nan = test_features.copy()
        test_features_with_nan.iloc[0, 0] = np.nan
        
        # Either predict successfully or raise clear error
        with pytest.raises((ValueError, AssertionError)):
            trained_model.predict(test_features_with_nan)


class TestDataValidation:
    
    def test_no_duplicate_timestamps(self):
        """Time series should have unique timestamps"""
        df = load_sensor_data()
        
        assert df.index.is_unique, "Duplicate timestamps found"
    
    def test_expected_columns_present(self):
        """Required columns should exist"""
        df = load_sensor_data()
        required_columns = ['temperature', 'humidity', 'supply_temp']
        
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_temperature_range(self):
        """Temperatures should be physically plausible"""
        df = load_sensor_data()
        
        assert df['temperature'].min() > -50, "Temperature too low"
        assert df['temperature'].max() < 100, "Temperature too high"
```

### 6.4 Integration Tests

```python
class TestFullPipeline:
    
    def test_end_to_end_prediction(self):
        """Full pipeline from raw data to prediction"""
        # Load raw data
        raw_data = load_raw_data('test_data.csv')
        
        # Preprocessing
        clean_data = preprocess(raw_data)
        
        # Feature engineering
        features = create_features(clean_data)
        
        # Prediction
        model = load_model('production_model.pkl')
        predictions = model.predict(features)
        
        # Validate output
        assert len(predictions) == len(features)
        assert not np.any(np.isnan(predictions))
    
    def test_model_retraining_improves(self):
        """Retraining with new data should not degrade performance"""
        old_model = load_model('production_model.pkl')
        
        # Retrain with new data
        new_model = retrain_model(new_training_data)
        
        # Evaluate both on holdout set
        old_rmse = evaluate_model(old_model, holdout_data)
        new_rmse = evaluate_model(new_model, holdout_data)
        
        # New model should not be significantly worse
        assert new_rmse <= old_rmse * 1.1, "Performance degraded by >10%"
```

---

## 7. Real-Time vs Batch Processing

### 7.1 Heating System Context

| Aspect | Batch | Real-Time |
|--------|-------|-----------|
| Use case | Daily energy reports, model retraining | Setpoint adjustment, anomaly alerts |
| Latency | Minutes to hours | Milliseconds to seconds |
| Data freshness | Historical | Current sensor readings |
| Processing | Large datasets efficiently | Individual events quickly |
| Green Fusion example | Nightly model updates | Immediate heating curve adjustment |

### 7.2 Stream Processing Architecture

```
Sensors → Message Queue → Stream Processor → Actions
  │           (Kafka)        (Flink/Spark)      │
  │                               │             │
  └───────────────────────────────┴─────────────┘
                    ↓
              Time-Series DB
              (InfluxDB/TimescaleDB)
                    ↓
              Batch Processing
              (Daily aggregations)
```

### 7.3 Real-Time Prediction Service

```python
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# Load model at startup
model = load_model('heating_model.pkl')
scaler = load_scaler('scaler.pkl')

class SensorReading(BaseModel):
    building_id: str
    timestamp: str
    indoor_temp: float
    outdoor_temp: float
    humidity: float
    supply_temp: float

class PredictionResponse(BaseModel):
    building_id: str
    predicted_demand: float
    recommended_setpoint: float
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
async def predict_heating_demand(reading: SensorReading):
    # Create feature vector
    features = create_features_realtime(reading)
    features_scaled = scaler.transform(features.reshape(1, -1))
    
    # Predict
    prediction = model.predict(features_scaled)[0]
    
    # Calculate recommended setpoint
    setpoint = calculate_optimal_setpoint(
        current_temp=reading.indoor_temp,
        predicted_demand=prediction,
        outdoor_temp=reading.outdoor_temp
    )
    
    return PredictionResponse(
        building_id=reading.building_id,
        predicted_demand=prediction,
        recommended_setpoint=setpoint,
        confidence=0.85  # Could come from prediction intervals
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_version": "1.2.3"}
```

### 7.4 Bridge from Your Experience

Your Streamlit app is actually real-time prediction:
- User selects store/item → immediate forecast
- Autoregressive updates happen dynamically
- No batch processing needed for inference

**How to discuss:**
> "My deployed Streamlit application performs real-time predictions—users select parameters and get immediate forecasts. The model loads once at startup, then inference is fast. For production heating systems, the same pattern applies: load model, receive sensor data, return prediction/action. The main addition would be proper API design and monitoring."

---

## 8. Interview Discussion Framework

### When Asked About a Gap Topic:

**1. Acknowledge honestly:**
> "I haven't implemented [X] in production, but I understand the concepts well."

**2. Connect to your experience:**
> "In my forecasting project, I faced a similar challenge when [specific example]."

**3. Show learning ability:**
> "The key principles—[name 2-3]—transfer directly. I'd need to learn the specific implementation details for your context."

**4. Ask clarifying question:**
> "How does Green Fusion currently approach [X]? I'm curious whether you use [A] or [B]."

### Example Response for RL Question:

> "I haven't deployed RL in production, but I understand the framework well. In my retail forecasting project, I built autoregressive models where current predictions inform future ones—that's conceptually similar to RL's temporal credit assignment through value functions.
>
> The key differences are that RL learns through environment interaction rather than supervised labels, and handles the exploration-exploitation trade-off. For heating systems, I'd expect challenges around simulation-to-real transfer since you can't safely explore randomly on real buildings.
>
> I'm curious—does Green Fusion use simulation-based training, or do you leverage offline RL from historical data?"

---

## 9. Quick Reference: Key Algorithms

| Domain | Algorithms to Know | Your Talking Point |
|--------|-------------------|-------------------|
| **RL** | DQN, PPO, SAC, TD3 | "My autoregressive forecasting is similar to value estimation" |
| **Unsupervised** | K-Means, LOF, Isolation Forest, Autoencoders | "I identified sparse data patterns (0.9% active combinations)" |
| **MPC** | Quadratic programming, receding horizon | "My multi-step forecasting optimizes across future timesteps" |
| **Multi-objective** | NSGA-II, Pareto fronts, weighted sum | "I balanced model complexity vs performance in feature selection" |
| **APIs** | REST, GraphQL, WebSocket | "My Streamlit app serves real-time predictions" |
| **Testing** | pytest, unit/integration tests | "I validated with ablation studies and documented decisions" |

---

*Study Guide prepared: December 2025*
