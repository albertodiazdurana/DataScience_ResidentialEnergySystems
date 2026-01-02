"""
Heating Curve Simulation Module

This module provides functions to simulate heating curve (Heizkennlinie) data
for residential buildings. It includes weather data fetching, heating curve
calculation, night setback logic, and noise model application.

Functions:
    fetch_weather_data: Fetch historical weather data from Open-Meteo API
    interpolate_to_15min: Convert hourly data to 15-minute resolution
    calculate_vorlauf: Calculate flow temperature using heating curve formula
    is_night_hour: Check if hour falls within night setback period
    get_room_target: Get target room temperature based on time of day
    apply_noise: Apply noise model to ideal temperature data
    generate_simulation: Generate complete simulation dataset
"""

import pandas as pd
import numpy as np
import requests
from typing import Optional


def fetch_weather_data(
    latitude: float = 52.52,
    longitude: float = 13.41,
    start_date: str = "2023-11-01",
    end_date: str = "2024-03-31"
) -> pd.DataFrame:
    """
    Fetch historical hourly temperature data from Open-Meteo API.

    Parameters
    ----------
    latitude : float
        Location latitude (default: Berlin 52.52)
    longitude : float
        Location longitude (default: Berlin 13.41)
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and t_outdoor column (°C)

    Raises
    ------
    requests.HTTPError
        If API request fails
    """
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
        "timezone": "Europe/Berlin"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame({
        "datetime": pd.to_datetime(data["hourly"]["time"]),
        "t_outdoor": data["hourly"]["temperature_2m"]
    })

    df = df.set_index("datetime")

    return df


def interpolate_to_15min(df: pd.DataFrame, method: str = "linear") -> pd.DataFrame:
    """
    Interpolate hourly data to 15-minute resolution.

    Adds datetime feature columns for time-based logic.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with datetime index and temperature column
    method : str
        Interpolation method ('linear', 'cubic', 'quadratic')

    Returns
    -------
    pd.DataFrame
        DataFrame with 15-minute resolution and datetime features
    """
    # Create 15-minute index
    new_index = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="15min"
    )

    # Reindex and interpolate
    df_15min = df.reindex(new_index)
    df_15min = df_15min.interpolate(method=method)
    df_15min.index.name = "datetime"

    # Add datetime features
    df_15min["hour"] = df_15min.index.hour
    df_15min["day_of_week"] = df_15min.index.dayofweek
    df_15min["month"] = df_15min.index.month
    df_15min["is_weekend"] = df_15min["day_of_week"].isin([5, 6])

    return df_15min


def calculate_vorlauf(
    t_outdoor: float,
    t_room: float,
    slope: float,
    t_base: float = 20.0,
    t_min: float = 25.0,
    t_max: float = 75.0,
    summer_cutoff: float = 15.0
) -> float:
    """
    Calculate Vorlauftemperatur (flow temperature) based on Heizkennlinie.

    Formula: T_vorlauf = T_base + slope * (T_room - T_outdoor)

    Parameters
    ----------
    t_outdoor : float
        Outdoor temperature (°C)
    t_room : float
        Target room temperature (°C)
    slope : float
        Heating curve slope (Neigung/Steilheit), typically 0.3-1.6
    t_base : float
        Base flow temperature (°C), default 20
    t_min : float
        Minimum flow temperature (°C), default 25
    t_max : float
        Maximum flow temperature (°C), default 75
    summer_cutoff : float
        Outdoor temp above which heating is off (°C), default 15

    Returns
    -------
    float
        Flow temperature (°C), or NaN if heating is off (summer mode)
    """
    # Summer mode: heating off
    if t_outdoor > summer_cutoff:
        return np.nan

    # Heating curve formula
    t_vorlauf = t_base + slope * (t_room - t_outdoor)

    # Clamp to operating limits
    t_vorlauf = np.clip(t_vorlauf, t_min, t_max)

    return t_vorlauf


def is_night_hour(hour: int, night_start: int = 22, night_end: int = 6) -> bool:
    """
    Determine if given hour falls within night setback period.

    Handles crossing midnight (e.g., 22:00 - 06:00).

    Parameters
    ----------
    hour : int
        Hour of day (0-23)
    night_start : int
        Hour when night mode starts (default 22)
    night_end : int
        Hour when night mode ends (default 6)

    Returns
    -------
    bool
        True if hour is within night period
    """
    # Handle crossing midnight
    if night_start > night_end:
        return hour >= night_start or hour < night_end
    else:
        return night_start <= hour < night_end


def get_room_target(
    hour: int,
    t_room_day: float = 20.0,
    t_room_night: float = 16.0,
    night_start: int = 22,
    night_end: int = 6
) -> float:
    """
    Get target room temperature based on time of day.

    Parameters
    ----------
    hour : int
        Hour of day (0-23)
    t_room_day : float
        Target room temperature during day (°C)
    t_room_night : float
        Target room temperature during night (°C)
    night_start : int
        Hour when night mode starts
    night_end : int
        Hour when night mode ends

    Returns
    -------
    float
        Target room temperature (°C)
    """
    if is_night_hour(hour, night_start, night_end):
        return t_room_night
    else:
        return t_room_day


def apply_noise(
    df: pd.DataFrame,
    gaussian_sigma: float = 1.5,
    dhw_spike_probability: float = 0.0,
    dhw_spike_magnitude: float = 12.0,
    missing_rate: float = 0.0,
    outlier_rate: float = 0.0,
    stuck_sensor_rate: float = 0.0,
    vorlauf_col: str = "t_vorlauf_ideal",
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Apply noise to ideal Vorlauf data to simulate sensor imperfections.

    Noise types:
    - Gaussian: Random measurement noise
    - DHW spikes: Domestic hot water interference (temporary +magnitude)
    - Missing: Sensor dropouts (NaN values)
    - Outliers: Extreme erroneous readings (±20°C)
    - Stuck sensor: Repeated previous value

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with t_vorlauf_ideal column
    gaussian_sigma : float
        Standard deviation of Gaussian noise (°C)
    dhw_spike_probability : float
        Probability of DHW spike per reading (0-1)
    dhw_spike_magnitude : float
        Magnitude of DHW spike (°C)
    missing_rate : float
        Probability of missing value per reading (0-1)
    outlier_rate : float
        Probability of outlier per reading (0-1)
    stuck_sensor_rate : float
        Probability of stuck sensor per reading (0-1)
    vorlauf_col : str
        Name of column containing ideal Vorlauf values
    random_seed : int
        Random seed for reproducibility

    Returns
    -------
    pd.DataFrame
        DataFrame with added t_vorlauf_noisy column
    """
    np.random.seed(random_seed)
    df = df.copy()

    # Start with ideal values
    noisy = df[vorlauf_col].copy()
    n = len(noisy)

    # 1. Gaussian noise
    if gaussian_sigma > 0:
        noise = np.random.normal(0, gaussian_sigma, n)
        noisy = noisy + noise

    # 2. DHW spikes (domestic hot water interference)
    if dhw_spike_probability > 0:
        spike_mask = np.random.random(n) < dhw_spike_probability
        noisy[spike_mask] = noisy[spike_mask] + dhw_spike_magnitude

    # 3. Outliers (random extreme values)
    if outlier_rate > 0:
        outlier_mask = np.random.random(n) < outlier_rate
        outlier_direction = np.random.choice([-1, 1], size=n)
        noisy[outlier_mask] = noisy[outlier_mask] + outlier_direction[outlier_mask] * 20

    # 4. Missing values
    if missing_rate > 0:
        missing_mask = np.random.random(n) < missing_rate
        noisy[missing_mask] = np.nan

    # 5. Stuck sensor values (repeat previous value)
    if stuck_sensor_rate > 0:
        stuck_mask = np.random.random(n) < stuck_sensor_rate
        for i in range(1, n):
            if stuck_mask[i] and not np.isnan(noisy.iloc[i-1]):
                noisy.iloc[i] = noisy.iloc[i-1]

    # Clamp to reasonable range (sensor limits)
    noisy = noisy.clip(lower=0, upper=100)

    df["t_vorlauf_noisy"] = noisy

    return df


def generate_simulation(
    config: dict,
    weather_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Generate complete heating curve simulation dataset.

    This is the main entry point for simulation. It combines weather data,
    heating curve calculation, night setback, and noise application.

    Parameters
    ----------
    config : dict
        Configuration dictionary with keys:
        - slope: Heating curve slope
        - t_base: Base temperature
        - t_room_day: Day room target
        - t_room_night: Night room target
        - t_vorlauf_min: Minimum flow temperature
        - t_vorlauf_max: Maximum flow temperature
        - t_outdoor_summer_cutoff: Summer cutoff temperature
        - night_start_hour: Night mode start
        - night_end_hour: Night mode end
        - noise_model: dict with noise parameters (optional)
        - location: dict with latitude/longitude (optional)
        - period: dict with start_date/end_date (optional)
    weather_df : pd.DataFrame, optional
        Pre-fetched weather data. If None, fetches from API.

    Returns
    -------
    pd.DataFrame
        Complete simulation dataset with columns:
        - t_outdoor: Outdoor temperature
        - hour, day_of_week, month, is_weekend: Datetime features
        - t_room_target: Target room temperature
        - t_vorlauf_ideal: Ideal flow temperature
        - is_night: Night mode indicator
        - t_vorlauf_noisy: Flow temperature with noise (if noise_model provided)
    """
    # Get location and period from config or use defaults
    location = config.get("location", {"latitude": 52.52, "longitude": 13.41})
    period = config.get("period", {"start_date": "2023-11-01", "end_date": "2024-03-31"})

    # Fetch or use provided weather data
    if weather_df is None:
        df = fetch_weather_data(
            latitude=location.get("latitude", 52.52),
            longitude=location.get("longitude", 13.41),
            start_date=period.get("start_date", "2023-11-01"),
            end_date=period.get("end_date", "2024-03-31")
        )
        df = interpolate_to_15min(df)
    else:
        df = weather_df.copy()

    # Get room target for each timestamp
    df["t_room_target"] = df["hour"].apply(
        lambda h: get_room_target(
            h,
            t_room_day=config.get("t_room_day", 20.0),
            t_room_night=config.get("t_room_night", 16.0),
            night_start=config.get("night_start_hour", 22),
            night_end=config.get("night_end_hour", 6)
        )
    )

    # Calculate ideal Vorlauf
    df["t_vorlauf_ideal"] = df.apply(
        lambda row: calculate_vorlauf(
            t_outdoor=row["t_outdoor"],
            t_room=row["t_room_target"],
            slope=config.get("slope", 1.4),
            t_base=config.get("t_base", 20.0),
            t_min=config.get("t_vorlauf_min", 25.0),
            t_max=config.get("t_vorlauf_max", 75.0),
            summer_cutoff=config.get("t_outdoor_summer_cutoff", 15.0)
        ),
        axis=1
    )

    # Add night mode indicator
    df["is_night"] = df["hour"].apply(
        lambda h: is_night_hour(
            h,
            night_start=config.get("night_start_hour", 22),
            night_end=config.get("night_end_hour", 6)
        )
    )

    # Apply noise if noise model is provided
    noise_model = config.get("noise_model")
    if noise_model:
        df = apply_noise(
            df,
            gaussian_sigma=noise_model.get("gaussian_sigma", 1.5),
            dhw_spike_probability=noise_model.get("dhw_spike_probability", 0.0),
            dhw_spike_magnitude=noise_model.get("dhw_spike_magnitude", 12.0),
            missing_rate=noise_model.get("missing_rate", 0.0),
            outlier_rate=noise_model.get("outlier_rate", 0.0),
            stuck_sensor_rate=noise_model.get("stuck_sensor_rate", 0.0),
            vorlauf_col="t_vorlauf_ideal",
            random_seed=noise_model.get("random_seed", 42)
        )

    return df
