"""
Heating Curve Application Package

This package provides modules for heating curve simulation and analysis:
- simulation: Generate heating curve data from weather data
- analysis: Extract parameters from sensor data
- config: Configuration presets and defaults

To run the Streamlit app:
    streamlit run app/streamlit_app.py
"""

from .simulation import (
    fetch_weather_data,
    interpolate_to_15min,
    calculate_vorlauf,
    generate_simulation,
)

from .analysis import (
    detect_temperature_limits,
    detect_day_night_modes,
    extract_parameters,
)

from .config import (
    BUILDING_PRESETS,
    NOISE_MODELS,
    DEFAULT_CONFIG,
    get_building_preset,
    get_noise_config,
)

__all__ = [
    # Simulation
    "fetch_weather_data",
    "interpolate_to_15min",
    "calculate_vorlauf",
    "generate_simulation",
    # Analysis
    "detect_temperature_limits",
    "detect_day_night_modes",
    "extract_parameters",
    # Config
    "BUILDING_PRESETS",
    "NOISE_MODELS",
    "DEFAULT_CONFIG",
    "get_building_preset",
    "get_noise_config",
]
