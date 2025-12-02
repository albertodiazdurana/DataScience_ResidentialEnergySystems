# TravelTide Segmentation → Green Fusion Energy Optimization
## Bridging Your Unsupervised Learning Experience

**Source Project:** [TravelTide Customer Segmentation](https://github.com/albertodiazdurana/TravelTide_Customer_Segmentation)  
**Target Domain:** Green Fusion Heating Optimization

---

## 1. Project Overview: TravelTide

Your TravelTide project delivered:
- **Customer Segmentation:** 3 behavioral clusters from 5,765 users using Hierarchical clustering (Ward)
- **Individual Assignment:** Propensity-based perk allocation to 5 reward types
- **Confidence Ratings:** HIGH/MEDIUM/LOW for phased implementation
- **65 Engineered Features:** From booking patterns, spending, engagement, risk indicators

**Key Technical Achievements:**
- K-selection validated through 4 metrics (Silhouette, Davies-Bouldin, Calinski-Harabasz, Inertia)
- Hierarchical vs K-Means comparison (Hierarchical won: DB 0.88 vs 1.65)
- PCA analysis: 56.4% variance explained in PC1-2
- Propensity scoring revealed within-cluster diversity (79.7% cluster had 5 different perk preferences)

---

## 2. Direct Domain Translation

### Entity Mapping

| TravelTide | Green Fusion |
|------------|--------------|
| Customer | Building |
| Booking behavior | Heating consumption pattern |
| Customer Lifetime Value (CLV) | Energy efficiency potential / Savings |
| Perk preference | Optimal heating strategy |
| Session engagement | Sensor data quality/frequency |
| Travel frequency | Heating demand variability |

### Cluster Persona → Building Archetype

| TravelTide Persona | Green Fusion Equivalent |
|--------------------|------------------------|
| **Premium Paula** (79.7%, high CLV) | **Stable Stefan** - Large multi-family buildings, consistent consumption, high savings potential |
| **Dining David** (5.0%, experiential) | **Variable Viktor** - Buildings with complex usage patterns, occupancy-driven demand |
| **Flexible Fiona** (15.3%, budget) | **Efficient Emma** - Well-insulated buildings, low baseline consumption, optimization-sensitive |

---

## 3. Technical Skills Transfer

### 3.1 Feature Engineering (65 Features → Building Features)

**Your TravelTide Features:**
```
Booking patterns (12 features)
Spending behavior (10 features)
Engagement metrics (8 features)
Risk indicators (7 features)
Travel preferences (8 features)
RFM segmentation (4 features)
Behavioral scores (5 features)
Discount patterns (6 features)
Perk propensities (5 features)
```

**Green Fusion Equivalent Features:**

| TravelTide Category | Energy Domain | Example Features |
|---------------------|---------------|------------------|
| **Booking patterns** | Heating patterns | Daily consumption profile, peak demand hours, weekend/weekday ratio |
| **Spending behavior** | Energy expenditure | kWh per degree-day, cost per m², seasonal spending |
| **Engagement metrics** | Sensor quality | Data completeness, reading frequency, sensor uptime |
| **Risk indicators** | Anomaly indicators | Consumption volatility, equipment age, maintenance history |
| **Travel preferences** | Thermal preferences | Setpoint choices, comfort band width, response to weather |
| **RFM segmentation** | Building RFM | Recency (last optimization), Frequency (adjustments), Monetary (savings achieved) |
| **Perk propensities** | Strategy propensities | Night setback effectiveness, outdoor reset responsiveness, load shift potential |

### 3.2 Clustering Methodology

**Your Approach (directly transferable):**

| Step | TravelTide | Green Fusion Application |
|------|-----------|-------------------------|
| K-selection | Tested K=2-10 with 4 metrics | Test building cluster counts with same metrics |
| Method comparison | Hierarchical vs K-Means | Same comparison for building portfolios |
| Validation | Silhouette 0.3806, DB 0.8844 | Same metrics for building clusters |
| Linkage | Ward (minimizes within-cluster variance) | Ward ideal for buildings with continuous features |
| Dimensionality | PCA (56.4% in PC1-2) | PCA for high-dimensional sensor data |

**Pseudo-code from your project (applicable to buildings):**

```python
# Your TravelTide approach → Building segmentation
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score

def segment_buildings(building_features, k_range=range(2, 11)):
    """
    Segment buildings using your validated methodology
    """
    # Normalize features (your approach)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(building_features)
    
    # K-selection with multiple metrics (your 4-metric validation)
    results = []
    for k in k_range:
        model = AgglomerativeClustering(
            n_clusters=k,
            linkage='ward'  # Your choice
        )
        labels = model.fit_predict(features_scaled)
        
        results.append({
            'k': k,
            'silhouette': silhouette_score(features_scaled, labels),
            'davies_bouldin': davies_bouldin_score(features_scaled, labels),
        })
    
    return pd.DataFrame(results)
```

### 3.3 Propensity Scoring → Strategy Assignment

**Your critical insight:** Cluster membership alone misses individual variation. Premium Paula (79.7%) had diverse perk preferences:
- 28% → Free Hotel Night
- 26% → Free Hotel Meal  
- 24% → Free Bag
- 14% → Exclusive Discount
- 8% → No Cancel Fee

**Green Fusion application:** Building clusters also have internal diversity. A "High Consumption" cluster may include:
- Buildings responsive to night setback (40%)
- Buildings responsive to outdoor reset optimization (30%)
- Buildings needing equipment replacement (20%)
- Buildings with occupancy-based potential (10%)

**Your propensity approach transfers directly:**

```python
def calculate_strategy_propensities(building_features):
    """
    Calculate propensity for each optimization strategy
    (mirrors your perk propensity calculation)
    """
    propensities = pd.DataFrame()
    
    # Night setback propensity
    # High if: consistent occupancy patterns, good thermal mass
    propensities['night_setback'] = (
        building_features['occupancy_predictability'] * 0.4 +
        building_features['thermal_mass_indicator'] * 0.3 +
        building_features['current_night_consumption'] * 0.3
    )
    
    # Outdoor reset propensity  
    # High if: weather-correlated consumption, adjustable heating curve
    propensities['outdoor_reset'] = (
        building_features['weather_correlation'] * 0.5 +
        building_features['heating_curve_suboptimal'] * 0.3 +
        building_features['has_adjustable_controls'] * 0.2
    )
    
    # Load shifting propensity (for heat pumps)
    # High if: thermal storage capacity, variable tariff
    propensities['load_shift'] = (
        building_features['thermal_storage_capacity'] * 0.4 +
        building_features['has_variable_tariff'] * 0.3 +
        building_features['consumption_flexibility'] * 0.3
    )
    
    # Normalize to [0, 1]
    propensities = propensities.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    return propensities


def assign_optimal_strategy(propensities):
    """
    Assign each building to optimal strategy with confidence
    (mirrors your perk assignment logic)
    """
    assignments = pd.DataFrame()
    
    # Primary assignment
    assignments['assigned_strategy'] = propensities.idxmax(axis=1)
    assignments['strategy_propensity'] = propensities.max(axis=1)
    
    # Second best (for fallback)
    assignments['second_strategy'] = propensities.apply(
        lambda row: row.nlargest(2).index[1], axis=1
    )
    assignments['second_propensity'] = propensities.apply(
        lambda row: row.nlargest(2).values[1], axis=1
    )
    
    # Confidence delta (your approach)
    assignments['confidence_delta'] = (
        assignments['strategy_propensity'] - assignments['second_propensity']
    )
    
    # Confidence level (your thresholds)
    assignments['confidence_level'] = pd.cut(
        assignments['confidence_delta'],
        bins=[-np.inf, 0.1, 0.25, np.inf],
        labels=['LOW', 'MEDIUM', 'HIGH']
    )
    
    return assignments
```

### 3.4 Confidence Ratings for Phased Rollout

**Your approach:**
- HIGH confidence: 63.5% → Immediate launch
- MEDIUM confidence: 33.8% → Reliable, proceed with monitoring
- LOW confidence: 2.8% → Require A/B testing

**Green Fusion application:**

| Confidence | Buildings | Action |
|------------|-----------|--------|
| HIGH | Clear strategy fit | Deploy optimization immediately |
| MEDIUM | Good fit, some uncertainty | Deploy with closer monitoring |
| LOW | Ambiguous response patterns | Pilot test before full deployment |

**Interview talking point:**
> "In my segmentation project, I developed confidence ratings based on the gap between first and second choice propensities. This enabled a phased implementation—63.5% of users could be targeted immediately with high confidence, while 2.8% required A/B testing. The same logic applies to building optimization: deploy proven strategies first, pilot uncertain cases."

---

## 4. Analytical Techniques Mapping

### 4.1 Your Validated Metrics

| Metric | Your Use | Green Fusion Use |
|--------|----------|------------------|
| **Silhouette Score** | Cluster cohesion (0.3806 at K=3) | Building cluster quality |
| **Davies-Bouldin Index** | Cluster separation (0.8844) | Cluster distinctiveness |
| **Calinski-Harabasz** | Cluster density ratio | Building group compactness |
| **Inertia** | Within-cluster variance | Consumption pattern similarity |

### 4.2 PCA Analysis

**Your finding:** 56.4% variance in PC1-2, 81.9% in PC1-5

**Green Fusion application:**
- High-dimensional sensor data (temperature, humidity, flow rates, etc.)
- PCA reduces to interpretable components
- PC1 might represent "overall consumption level"
- PC2 might represent "temporal pattern type"

```python
# Your PCA approach for building features
from sklearn.decomposition import PCA

def analyze_building_dimensions(features_scaled):
    """
    Dimensionality analysis for building features
    (your PCA methodology)
    """
    pca = PCA()
    pca.fit(features_scaled)
    
    # Variance explained (your 56.4% benchmark)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    
    # How many components for 80% variance?
    n_components_80 = np.argmax(cumulative_variance >= 0.80) + 1
    
    # Component loadings for interpretation
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(len(pca.components_))],
        index=feature_names
    )
    
    return {
        'variance_explained': cumulative_variance,
        'n_components_80pct': n_components_80,
        'loadings': loadings
    }
```

### 4.3 Hierarchical Clustering (Your Winning Method)

**Why you chose Hierarchical over K-Means:**
- Better DB score (0.88 vs 1.65)
- Deterministic (no random initialization)
- Dendrogram provides interpretability

**Green Fusion relevance:**
- Building portfolios benefit from hierarchical structure
- Can cut dendrogram at different levels for different granularity
- Reproducible results critical for production systems

---

## 5. Feature Engineering Parallels

### 5.1 RFM Segmentation → Building RFM

**Your customer RFM:**
- **Recency:** Days since last booking
- **Frequency:** Bookings per period
- **Monetary:** Total spend / CLV

**Building RFM:**
- **Recency:** Days since last optimization adjustment
- **Frequency:** How often building responds to control changes
- **Monetary:** Energy savings achieved / Savings potential

```python
def calculate_building_rfm(building_history):
    """
    RFM for buildings (adapted from your customer RFM)
    """
    rfm = pd.DataFrame()
    
    # Recency: Days since last optimization
    rfm['recency'] = (
        pd.Timestamp.now() - building_history.groupby('building_id')['last_adjustment'].max()
    ).dt.days
    
    # Frequency: Adjustments per quarter
    rfm['frequency'] = building_history.groupby('building_id')['adjustments'].sum() / 4
    
    # Monetary: Savings achieved (€)
    rfm['monetary'] = building_history.groupby('building_id')['savings_eur'].sum()
    
    # Score each dimension (1-5)
    for col in ['recency', 'frequency', 'monetary']:
        # Recency: lower is better (invert)
        if col == 'recency':
            rfm[f'{col}_score'] = pd.qcut(rfm[col], 5, labels=[5,4,3,2,1])
        else:
            rfm[f'{col}_score'] = pd.qcut(rfm[col], 5, labels=[1,2,3,4,5])
    
    rfm['rfm_score'] = (
        rfm['recency_score'].astype(int) * 100 +
        rfm['frequency_score'].astype(int) * 10 +
        rfm['monetary_score'].astype(int)
    )
    
    return rfm
```

### 5.2 Behavioral Scores → Building Behavioral Scores

**Your behavioral scores:**
- Loyalty indicators
- Engagement patterns
- Risk indicators

**Building behavioral scores:**

```python
def calculate_building_behavioral_scores(building_data):
    """
    Behavioral scoring for buildings
    (adapted from your customer behavioral scores)
    """
    scores = pd.DataFrame()
    
    # Stability score (like loyalty)
    # Consistent consumption patterns = stable building
    scores['stability'] = 1 - building_data.groupby('building_id')['consumption'].transform('std') / \
                              building_data.groupby('building_id')['consumption'].transform('mean')
    
    # Responsiveness score (like engagement)
    # How well building responds to control changes
    scores['responsiveness'] = building_data.groupby('building_id').apply(
        lambda x: correlation(x['setpoint_change'], x['consumption_change'])
    )
    
    # Anomaly risk score
    # Buildings with frequent anomalies = higher risk
    scores['anomaly_risk'] = building_data.groupby('building_id')['is_anomaly'].mean()
    
    # Weather sensitivity score
    # How correlated is consumption with outdoor temperature
    scores['weather_sensitivity'] = building_data.groupby('building_id').apply(
        lambda x: correlation(x['outdoor_temp'], x['consumption'])
    )
    
    return scores
```

### 5.3 Outlier Handling (Your IQR Method)

**Your approach:** IQR-based outlier removal for data quality

**Building application:**

```python
def remove_sensor_outliers(df, columns, iqr_multiplier=1.5):
    """
    IQR outlier removal (your validated approach)
    """
    df_clean = df.copy()
    
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - iqr_multiplier * IQR
        upper_bound = Q3 + iqr_multiplier * IQR
        
        outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
        df_clean.loc[outliers, col] = np.nan  # Or median imputation
        
        print(f"{col}: {outliers.sum()} outliers removed ({outliers.mean()*100:.1f}%)")
    
    return df_clean
```

---

## 6. Business Value Translation

### 6.1 Your CLV Analysis → Building Value Analysis

**Your finding:** Premium Paula = $22.9M CLV (98% of total)
**Your recommendation:** 70-75% budget allocation to Premium Paula

**Green Fusion equivalent:**
- Identify high-value buildings (largest savings potential)
- Prioritize optimization efforts on highest-impact buildings
- Calculate ROI per building segment

```python
def calculate_building_value_segments(buildings_df):
    """
    Building value analysis (mirrors your CLV analysis)
    """
    # Savings potential = Building value
    buildings_df['savings_potential'] = estimate_savings_potential(buildings_df)
    
    # Segment by value
    buildings_df['value_segment'] = pd.qcut(
        buildings_df['savings_potential'],
        q=[0, 0.5, 0.85, 1.0],
        labels=['Low Value', 'Medium Value', 'High Value']
    )
    
    # Value concentration analysis
    value_summary = buildings_df.groupby('value_segment').agg({
        'building_id': 'count',
        'savings_potential': ['sum', 'mean']
    })
    
    # Your insight: top segment often contains majority of value
    # "High Value" buildings might be 15% of count but 60% of savings
    
    return value_summary
```

### 6.2 Phased Implementation Strategy

**Your approach:**
1. HIGH confidence (63.5%) → Immediate launch
2. MEDIUM confidence (33.8%) → Standard rollout
3. LOW confidence (2.8%) → A/B testing

**Green Fusion rollout:**

| Phase | Buildings | Strategy |
|-------|-----------|----------|
| 1 | HIGH confidence, High value | Immediate optimization deployment |
| 2 | HIGH confidence, Medium value | Scheduled rollout |
| 3 | MEDIUM confidence | Deploy with enhanced monitoring |
| 4 | LOW confidence | Pilot program with manual validation |

---

## 7. Interview Talking Points

### Connecting Segmentation to Energy Optimization

**Question:** "Tell us about your experience with unsupervised learning."

**Answer:**
> "I completed a customer segmentation project for TravelTide where I segmented 5,765 users into behavioral clusters for a rewards program. The key insight wasn't just the clustering—I found that 79.7% of users fell into one cluster, but individual preferences within that cluster were highly diverse. This led me to develop propensity scoring that captured within-cluster variation.
>
> For building optimization, the same principle applies: buildings might cluster by consumption level, but optimal strategies vary within clusters. One high-consumption building might respond best to night setback, another to heating curve optimization. My propensity-based assignment approach handles this diversity."

### Technical Depth

**Question:** "How did you validate your clustering approach?"

**Answer:**
> "I used a 4-metric validation framework: Silhouette Score for cohesion, Davies-Bouldin Index for separation, Calinski-Harabasz for density ratio, and Inertia for within-cluster variance. I tested K=2 through K=10 and found K=3 optimal across metrics.
>
> I also compared Hierarchical clustering with Ward linkage against K-Means. Hierarchical won decisively—Davies-Bouldin of 0.88 versus 1.65. The deterministic nature of Hierarchical clustering was also important for reproducibility, which matters for production systems like building optimization."

### Confidence and Risk Management

**Question:** "How would you handle uncertainty in model recommendations?"

**Answer:**
> "In my TravelTide project, I implemented confidence ratings based on the gap between first and second choice propensities. If a customer strongly preferred one perk over others, they got HIGH confidence. If preferences were close, they got MEDIUM or LOW.
>
> 63.5% of users had HIGH confidence, enabling immediate targeting. The 2.8% with LOW confidence were flagged for A/B testing rather than assuming the model was correct. This risk-managed approach would translate directly to building optimization—deploy high-confidence strategies immediately, pilot uncertain cases."

---

## 8. Skills Summary: TravelTide → Green Fusion

| Your Demonstrated Skill | Evidence from TravelTide | Green Fusion Application |
|------------------------|-------------------------|-------------------------|
| **Feature Engineering** | 65 features from raw data | Building behavioral features |
| **Clustering** | Hierarchical (Ward), K=3 validated | Building portfolio segmentation |
| **Method Comparison** | Hierarchical vs K-Means with metrics | Algorithm selection for building data |
| **Dimensionality Reduction** | PCA (56.4% variance PC1-2) | High-dimensional sensor data |
| **Propensity Modeling** | Individual perk assignment | Individual strategy assignment |
| **Confidence Scoring** | HIGH/MEDIUM/LOW ratings | Phased deployment decisions |
| **Business Translation** | CLV analysis, segment priorities | Savings potential prioritization |
| **Data Quality** | IQR outliers, cohort filtering | Sensor data validation |
| **Reproducibility** | Deterministic methods, documentation | Production-ready pipelines |

---

## 9. Key Differentiators to Emphasize

1. **Within-cluster diversity insight:** Your discovery that 79.7% in one cluster still had 5 different preferences—this translates to buildings needing individualized strategies despite cluster membership.

2. **Multi-metric validation:** Not relying on single metric (Silhouette alone)—used 4 complementary metrics for robust K-selection.

3. **Method comparison rigor:** Didn't assume K-Means—tested against Hierarchical and chose based on evidence.

4. **Confidence-based rollout:** Practical implementation strategy, not just analytical results.

5. **Feature engineering depth:** 65 features with business logic, not just statistical transformations.

---

## 10. Combined Project Narrative

For the Green Fusion interview, you can now present **two complementary projects:**

| Project | ML Type | Key Technique | Green Fusion Relevance |
|---------|---------|---------------|----------------------|
| **Favorita Forecasting** | Supervised (Time Series) | LSTM/XGBoost, Temporal validation | Heat demand prediction |
| **TravelTide Segmentation** | Unsupervised (Clustering) | Hierarchical clustering, Propensity scoring | Building segmentation, Strategy assignment |

**Combined narrative:**
> "I've worked on both supervised and unsupervised problems. My demand forecasting project taught me temporal data handling, feature engineering for sequences, and production deployment. My segmentation project taught me clustering validation, within-group diversity analysis, and confidence-based recommendations. Together, these cover the full spectrum Green Fusion needs: predicting heating demand (supervised) and segmenting buildings for strategy assignment (unsupervised)."

---

*Mapping document prepared: December 2025*
