"""
Heating Curve Configuration Module

This module provides default configurations, building presets, and noise models
for heating curve simulation and analysis.

Building Presets:
    BUILDING_PRESETS: Pre-configured heating curves for common building types

Noise Models:
    NOISE_MODELS: Configurations for data quality scenarios (Model 1/2/3)

Defaults:
    DEFAULT_CONFIG: Default heating curve parameters
    WINTER_PRESETS: Notable winter seasons for simulation

References:
    - DIN EN 12831: Heating systems in buildings - Method for calculation of
      the design heat load
    - VDI 2067: Economic efficiency of building installations
    - DIN 4701: Rules for calculation of heat requirements of buildings
    - EnEV/GEG: Energieeinsparverordnung / Gebäudeenergiegesetz
    - VDI 6030: Designing free heating surfaces - Fundamentals
    - DVGW W 551: Drinking water heating and piping systems (Legionella)
"""

from typing import Dict, Any


# =============================================================================
# Building Type Presets
# =============================================================================
# Different building types require different heating curve slopes based on
# insulation quality, heat distribution system, and heat source.
#
# References:
#   - Slope values: VDI 6030 Blatt 1, manufacturer default settings
#   - Temperature limits: DIN EN 12831, heat pump manufacturer specs
#   - KfW standards: Kreditanstalt für Wiederaufbau efficiency classes

BUILDING_PRESETS: Dict[str, Dict[str, Any]] = {
    "Heat Pump + Floor Heating": {
        # Ref: Heat pump max Vorlauf 55°C per manufacturer specs (Viessmann, Vaillant)
        # Ref: Floor heating design temp 35°C Vorlauf per DIN EN 1264
        # Ref: Slope 0.3 typical for low-energy buildings per VDI 6030
        "slope": 0.3,
        "t_vorlauf_max": 55,
        "t_vorlauf_min": 25,
        "description": "Modern, well-insulated building with floor heating. "
                       "Low-temperature system optimized for heat pump efficiency.",
        "typical_buildings": ["KfW 40/55 standard", "Passive house", "New construction"],
    },
    "Radiators + Good Insulation": {
        # Ref: Condensing boiler optimal return <55°C per DIN 4702-8
        # Ref: Renovated buildings per EnEV 2014/GEG requirements
        # Ref: Slope 1.0 standard for medium-temperature systems
        "slope": 1.0,
        "t_vorlauf_max": 65,
        "t_vorlauf_min": 25,
        "description": "Renovated building with improved insulation and modern radiators. "
                       "Medium-temperature system suitable for condensing boilers.",
        "typical_buildings": ["Renovated 1960s-1990s", "KfW 70-100 standard"],
    },
    "Radiators + Poor Insulation": {
        # Ref: Slope 1.4 is common factory default (Viessmann, Buderus, Vaillant controllers)
        # Ref: 75°C max per traditional radiator design DIN 4703
        "slope": 1.4,
        "t_vorlauf_max": 75,
        "t_vorlauf_min": 25,
        "description": "Older building with original insulation and radiators. "
                       "Common factory default setting for heating controllers.",
        "typical_buildings": ["Unrenovated 1950s-1980s", "Post-war buildings"],
    },
    "Historic Building": {
        # Ref: High-temperature systems up to 90°C per older DIN 4701
        # Ref: Slope 1.6 for buildings with high transmission losses
        "slope": 1.6,
        "t_vorlauf_max": 80,
        "t_vorlauf_min": 25,
        "description": "Unrenovated historic building with high heat loss. "
                       "Requires high flow temperatures to maintain comfort.",
        "typical_buildings": ["Pre-1940s", "Listed buildings", "Altbau"],
    },
}


# =============================================================================
# Noise Model Configurations
# =============================================================================
# Three noise models simulating different data quality scenarios.
# These are used to test algorithm robustness.

NOISE_MODELS: Dict[str, Dict[str, Any]] = {
    "Model 1": {
        "name": "Clean Data",
        "description": "Low-noise scenario for algorithm validation. "
                       "Simulates high-quality sensor installation.",
        "gaussian_sigma": 1.5,
        "dhw_spike_probability": 0.0,
        "dhw_spike_magnitude": 0,
        "missing_rate": 0.0,
        "outlier_rate": 0.0,
        "stuck_sensor_rate": 0.0,
    },
    "Model 2": {
        "name": "Moderate Noise",
        "description": "Typical sensor quality found in most buildings. "
                       "Some DHW interference and occasional outliers.",
        "gaussian_sigma": 3.5,
        "dhw_spike_probability": 0.02,
        "dhw_spike_magnitude": 12,
        "missing_rate": 0.0,
        "outlier_rate": 0.005,
        "stuck_sensor_rate": 0.0,
    },
    "Model 3": {
        "name": "Noisy/Realistic",
        "description": "Challenging data quality with significant noise, "
                       "missing values, and outliers. Tests algorithm limits.",
        "gaussian_sigma": 5.0,
        "dhw_spike_probability": 0.03,
        "dhw_spike_magnitude": 15,
        "missing_rate": 0.05,
        "outlier_rate": 0.015,
        "stuck_sensor_rate": 0.01,
    },
}


# =============================================================================
# Default Configuration
# =============================================================================
#
# References:
#   - Room temperature 20°C: DIN EN 12831, standard design indoor temp
#   - Night setback 4K: VDI 2067, typical energy-saving measure
#   - Summer cutoff 15°C: Common controller default (Heizgrenztemperatur)
#   - Min Vorlauf 25°C: Prevents condensation in return pipes

DEFAULT_CONFIG: Dict[str, Any] = {
    # Heating curve parameters
    "slope": 1.4,  # Ref: Common factory default per manufacturer settings
    "t_base": 20.0,  # Ref: DIN EN 12831 standard indoor design temperature
    "t_room_day": 20.0,  # Ref: DIN EN 12831 comfort temperature
    "t_room_night": 16.0,  # Ref: 4K night setback per VDI 2067 recommendations

    # Operating limits
    "t_vorlauf_min": 25.0,  # Ref: Prevents condensation, ensures circulation
    "t_vorlauf_max": 75.0,  # Ref: Traditional radiator design per DIN 4703
    "t_outdoor_summer_cutoff": 15.0,  # Ref: Heizgrenztemperatur, common default

    # Night setback schedule (22:00-06:00)
    # Ref: Typical residential schedule per EnEV/GEG usage profiles
    "night_start_hour": 22,
    "night_end_hour": 6,

    # Location (Berlin default)
    "location": {
        "name": "Berlin",
        "latitude": 52.52,
        "longitude": 13.41,
    },

    # Default period
    "period": {
        "start_date": "2023-11-01",
        "end_date": "2024-03-31",
    },
}


# =============================================================================
# Location Presets
# =============================================================================
# German cities for weather data fetching.
# Heating curve parameters are based on German norms (DIN, VDI, EnEV/GEG).

LOCATION_PRESETS: Dict[str, Dict[str, Any]] = {
    "Berlin": {
        "latitude": 52.52,
        "longitude": 13.41,
        "description": "Capital, continental climate",
    },
    "Munich": {
        "latitude": 48.14,
        "longitude": 11.58,
        "description": "Bavaria, colder winters (alpine influence)",
    },
    "Hamburg": {
        "latitude": 53.55,
        "longitude": 9.99,
        "description": "North, maritime climate",
    },
    "Frankfurt": {
        "latitude": 50.11,
        "longitude": 8.68,
        "description": "Central, moderate climate",
    },
    "Cologne": {
        "latitude": 50.94,
        "longitude": 6.96,
        "description": "West, mild winters (Rhine valley)",
    },
    "Stuttgart": {
        "latitude": 48.78,
        "longitude": 9.18,
        "description": "Southwest, moderate continental",
    },
    "Dresden": {
        "latitude": 51.05,
        "longitude": 13.74,
        "description": "East, continental climate",
    },
    "Freiburg": {
        "latitude": 47.99,
        "longitude": 7.85,
        "description": "Southwest, warmest German city",
    },
}


# =============================================================================
# Winter Presets
# =============================================================================
# Notable winter seasons for comparing mild vs cold conditions.

WINTER_PRESETS: Dict[str, Dict[str, str]] = {
    "2023-2024 (Mild)": {
        "start_date": "2023-11-01",
        "end_date": "2024-03-31",
        "description": "Mild winter, Berlin mean 4.9°C, only 25 freezing days",
    },
    "2022-2023": {
        "start_date": "2022-11-01",
        "end_date": "2023-03-31",
        "description": "Moderate winter",
    },
    "2021-2022": {
        "start_date": "2021-11-01",
        "end_date": "2022-03-31",
        "description": "Moderate winter",
    },
    "2010-2011 (Cold)": {
        "start_date": "2010-11-01",
        "end_date": "2011-03-31",
        "description": "Cold winter, good for testing upper temperature limits",
    },
}


# =============================================================================
# Parameter Ranges (for Streamlit sliders)
# =============================================================================
#
# References for range limits:
#   - Slope 0.2-2.0: Covers all building types from passive house to Altbau
#   - Room temp 18-24°C: DIN EN 12831 comfort range for residential
#   - Vorlauf max 45-85°C: From floor heating to high-temp radiators
#   - Summer cutoff 12-20°C: Heizgrenztemperatur range per climate zone

PARAMETER_RANGES: Dict[str, Dict[str, Any]] = {
    "slope": {
        "min": 0.2,  # Ref: Passive house / floor heating minimum
        "max": 2.0,  # Ref: Extreme cases, very poor insulation
        "step": 0.1,
        "default": 1.4,  # Ref: Common factory default
        "label": "Heating Curve Slope (K)",
        "help": "Higher values = steeper curve, more temperature change per °C outdoor",
    },
    "t_room_day": {
        "min": 18.0,  # Ref: DIN EN 12831 minimum comfort
        "max": 24.0,  # Ref: Upper comfort limit
        "step": 0.5,
        "default": 20.0,  # Ref: DIN EN 12831 standard
        "label": "Room Target - Day (°C)",
        "help": "Target room temperature during day hours",
    },
    "t_room_night": {
        "min": 14.0,  # Ref: Frost protection minimum
        "max": 20.0,  # Ref: No setback (equals day temp)
        "step": 0.5,
        "default": 16.0,  # Ref: 4K setback per VDI 2067
        "label": "Room Target - Night (°C)",
        "help": "Target room temperature during night setback (22:00-06:00)",
    },
    "t_vorlauf_max": {
        "min": 45.0,  # Ref: Heat pump upper limit
        "max": 85.0,  # Ref: High-temp radiator systems per DIN 4703
        "step": 5.0,
        "default": 75.0,  # Ref: Traditional radiator design
        "label": "Max Flow Temperature (°C)",
        "help": "Maximum Vorlauf temperature (clamping limit)",
    },
    "t_vorlauf_min": {
        "min": 20.0,  # Ref: Absolute minimum for circulation
        "max": 35.0,  # Ref: Floor heating typical operating temp
        "step": 1.0,
        "default": 25.0,  # Ref: Standard minimum to prevent condensation
        "label": "Min Flow Temperature (°C)",
        "help": "Minimum Vorlauf temperature",
    },
    "t_outdoor_summer_cutoff": {
        "min": 12.0,  # Ref: Colder climate zones
        "max": 20.0,  # Ref: Warmer climate zones (e.g., Freiburg)
        "step": 1.0,
        "default": 15.0,  # Ref: Standard Heizgrenztemperatur
        "label": "Summer Cutoff (°C)",
        "help": "Outdoor temperature above which heating is off",
    },
    "night_start_hour": {
        "min": 20,
        "max": 24,
        "step": 1,
        "default": 22,  # Ref: Typical residential schedule
        "label": "Night Start Hour",
        "help": "Hour when night setback begins",
    },
    "night_end_hour": {
        "min": 4,
        "max": 8,
        "step": 1,
        "default": 6,  # Ref: Typical residential schedule
        "label": "Night End Hour",
        "help": "Hour when night setback ends",
    },
}


# =============================================================================
# Helper Functions
# =============================================================================

def get_building_preset(name: str) -> Dict[str, Any]:
    """Get configuration for a building preset, merged with defaults."""
    if name not in BUILDING_PRESETS:
        raise ValueError(f"Unknown preset: {name}. Available: {list(BUILDING_PRESETS.keys())}")

    config = DEFAULT_CONFIG.copy()
    preset = BUILDING_PRESETS[name]
    config["slope"] = preset["slope"]
    config["t_vorlauf_max"] = preset["t_vorlauf_max"]
    config["t_vorlauf_min"] = preset["t_vorlauf_min"]

    return config


def get_noise_config(model_name: str) -> Dict[str, Any]:
    """Get noise configuration for a noise model."""
    if model_name not in NOISE_MODELS:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(NOISE_MODELS.keys())}")

    return NOISE_MODELS[model_name].copy()


def get_winter_period(preset_name: str) -> Dict[str, str]:
    """Get date range for a winter preset."""
    if preset_name not in WINTER_PRESETS:
        raise ValueError(f"Unknown preset: {preset_name}. Available: {list(WINTER_PRESETS.keys())}")

    preset = WINTER_PRESETS[preset_name]
    return {
        "start_date": preset["start_date"],
        "end_date": preset["end_date"],
    }
