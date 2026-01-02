"""
Heating Curve Streamlit Application

An interactive web application for simulating and analyzing heating curve
(Heizkennlinie) data for residential buildings.

Features:
- Simulation Tab: Generate heating curve data with configurable parameters
- Analysis Tab: Extract parameters from simulated or uploaded data

Run with: streamlit run app/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Import local modules
from config import (
    BUILDING_PRESETS,
    NOISE_MODELS,
    DEFAULT_CONFIG,
    WINTER_PRESETS,
    LOCATION_PRESETS,
    PARAMETER_RANGES,
    get_building_preset,
    get_noise_config,
)
from simulation import (
    fetch_weather_data,
    interpolate_to_15min,
    generate_simulation,
)
from analysis import (
    extract_parameters,
    detect_temperature_limits,
)


# =============================================================================
# Page Configuration
# =============================================================================

st.set_page_config(
    page_title="Heating Curve Simulator",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("🔥 Heating Curve Simulation & Analysis")
st.markdown("""
An interactive tool for understanding and analyzing heating curves (Heizkennlinie)
in residential buildings. Simulate data with configurable parameters and extract
heating curve parameters from noisy sensor data.
""")


# =============================================================================
# Sidebar - Documentation
# =============================================================================

with st.sidebar:
    st.header("📚 About")
    st.markdown("""
    **Heating Curve (Heizkennlinie)**

    The heating curve defines the relationship between outdoor temperature
    and flow temperature (Vorlauftemperatur):

    ```
    T_vorlauf = T_base + K × (T_room - T_outdoor)
    ```

    Where:
    - **K** = Slope (Neigung)
    - **T_room** = Target room temperature
    - **T_base** = Base temperature (typically 20°C)
    """)

    st.divider()

    st.markdown("""
    **Building Types**

    | Type | Slope | Typical |
    |------|-------|---------|
    | Heat Pump | 0.3 | Modern |
    | Good Insulation | 1.0 | Renovated |
    | Poor Insulation | 1.4 | Older |
    | Historic | 1.6 | Altbau |
    """)

    st.divider()

    st.markdown("""
    **Data Source**

    Weather data from [Open-Meteo](https://open-meteo.com/) API.
    Default: Berlin, 2023-2024 heating season.
    """)

    st.divider()

    # Collapsible references section
    with st.expander("📖 **Standards & References**"):
        st.markdown("""
        **German Norms (DIN/VDI)**

        | Standard | Description |
        |----------|-------------|
        | DIN EN 12831 | Heat load calculation, indoor design temp (20°C) |
        | DIN EN 1264 | Floor heating systems (max 35°C Vorlauf) |
        | DIN 4703 | Radiator design temperatures |
        | VDI 2067 | Night setback recommendations (4K) |
        | VDI 6030 | Heating curve slopes per building type |

        **Building Efficiency**

        | Standard | Description |
        |----------|-------------|
        | GEG | Gebäudeenergiegesetz (Building Energy Act) |
        | EnEV | Energieeinsparverordnung (predecessor to GEG) |
        | KfW 40/55/70 | Efficiency classes (% of reference building) |

        **Parameter Sources**

        - **Slope 1.4**: Common factory default (Viessmann, Buderus, Vaillant)
        - **Room temp 20°C**: DIN EN 12831 standard comfort
        - **Night setback 4K**: VDI 2067 energy saving measure
        - **Max Vorlauf 55°C**: Heat pump limit per manufacturer specs
        - **Summer cutoff 15°C**: Standard Heizgrenztemperatur
        """)


# =============================================================================
# Tabs
# =============================================================================

tab1, tab2 = st.tabs(["📊 Simulation", "🔍 Analysis"])


# =============================================================================
# Tab 1: Simulation
# =============================================================================

with tab1:
    st.header("Heating Curve Simulation")
    st.markdown("""
    Generate synthetic heating curve data based on real weather data.
    Adjust parameters to explore different building types and noise levels.
    """)

    # Two columns: controls (scrollable) and output (fixed)
    col_controls, col_output = st.columns([1, 2])

    with col_controls:
        # Create a scrollable container for configuration
        with st.container(height=650):
            st.subheader("Configuration")

            # Building preset selector
            preset_name = st.selectbox(
                "Building Type",
                options=list(BUILDING_PRESETS.keys()),
                index=2,  # Default: Radiators + Poor Insulation
                help="Select a building type preset to auto-fill parameters"
            )

            # Get preset values
            preset = BUILDING_PRESETS[preset_name]
            st.caption(preset["description"])

            st.divider()

            # Heating curve parameters
            st.markdown("**Heating Curve Parameters**")

            slope = st.slider(
                "Slope (K)",
                min_value=PARAMETER_RANGES["slope"]["min"],
                max_value=PARAMETER_RANGES["slope"]["max"],
                value=preset["slope"],
                step=PARAMETER_RANGES["slope"]["step"],
                help=PARAMETER_RANGES["slope"]["help"]
            )

            col_a, col_b = st.columns(2)
            with col_a:
                t_room_day = st.slider(
                    "Room Target - Day (°C)",
                    min_value=PARAMETER_RANGES["t_room_day"]["min"],
                    max_value=PARAMETER_RANGES["t_room_day"]["max"],
                    value=PARAMETER_RANGES["t_room_day"]["default"],
                    step=PARAMETER_RANGES["t_room_day"]["step"],
                )
            with col_b:
                t_room_night = st.slider(
                    "Room Target - Night (°C)",
                    min_value=PARAMETER_RANGES["t_room_night"]["min"],
                    max_value=PARAMETER_RANGES["t_room_night"]["max"],
                    value=PARAMETER_RANGES["t_room_night"]["default"],
                    step=PARAMETER_RANGES["t_room_night"]["step"],
                )

            col_c, col_d = st.columns(2)
            with col_c:
                t_vorlauf_max = st.slider(
                    "Max Vorlauf (°C)",
                    min_value=PARAMETER_RANGES["t_vorlauf_max"]["min"],
                    max_value=PARAMETER_RANGES["t_vorlauf_max"]["max"],
                    value=float(preset["t_vorlauf_max"]),
                    step=PARAMETER_RANGES["t_vorlauf_max"]["step"],
                )
            with col_d:
                t_vorlauf_min = st.slider(
                    "Min Vorlauf (°C)",
                    min_value=PARAMETER_RANGES["t_vorlauf_min"]["min"],
                    max_value=PARAMETER_RANGES["t_vorlauf_min"]["max"],
                    value=float(preset["t_vorlauf_min"]),
                    step=PARAMETER_RANGES["t_vorlauf_min"]["step"],
                )

            st.divider()

            # Noise model selector
            st.markdown("**Data Quality (Noise Model)**")
            noise_model_name = st.radio(
                "Select noise level",
                options=list(NOISE_MODELS.keys()),
                index=0,
                horizontal=True,
            )
            noise_config = NOISE_MODELS[noise_model_name]
            st.caption(noise_config["description"])

            st.divider()

            # Location and Period selection
            st.markdown("**Weather Data Source**")

            location_name = st.selectbox(
                "Location",
                options=list(LOCATION_PRESETS.keys()),
                index=0,  # Default: Berlin
                help="Select a city for weather data"
            )
            location = LOCATION_PRESETS[location_name]
            st.caption(f"📍 {location['description']} ({location['latitude']}°N, {location['longitude']}°E)")

            period_name = st.selectbox(
                "Heating Season",
                options=list(WINTER_PRESETS.keys()),
                index=0,  # Default: 2023-2024
                help="Select a winter period"
            )
            period = WINTER_PRESETS[period_name]
            st.caption(f"📅 {period['description']}")

        # Generate button outside container (always visible)
        generate_clicked = st.button("🔄 Generate Simulation", type="primary", use_container_width=True)

    # Build configuration
    config = {
        "slope": slope,
        "t_base": 20.0,
        "t_room_day": t_room_day,
        "t_room_night": t_room_night,
        "t_vorlauf_min": t_vorlauf_min,
        "t_vorlauf_max": t_vorlauf_max,
        "t_outdoor_summer_cutoff": 15.0,
        "night_start_hour": 22,
        "night_end_hour": 6,
        "location": {
            "name": location_name,
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        },
        "period": {
            "name": period_name,
            "start_date": period["start_date"],
            "end_date": period["end_date"],
        },
        "noise_model": {
            "gaussian_sigma": noise_config["gaussian_sigma"],
            "dhw_spike_probability": noise_config["dhw_spike_probability"],
            "dhw_spike_magnitude": noise_config["dhw_spike_magnitude"],
            "missing_rate": noise_config["missing_rate"],
            "outlier_rate": noise_config["outlier_rate"],
            "stuck_sensor_rate": noise_config["stuck_sensor_rate"],
            "random_seed": 42,
        }
    }

    # Generate or use cached data
    if generate_clicked or "sim_data" not in st.session_state:
        with st.spinner("Fetching weather data and generating simulation..."):
            try:
                df = generate_simulation(config)
                st.session_state["sim_data"] = df
                st.session_state["sim_config"] = config
            except Exception as e:
                st.error(f"Error generating simulation: {e}")
                st.stop()

    df = st.session_state.get("sim_data")

    # Output column
    with col_output:
        if df is not None:
            st.subheader("Simulation Results")

            # Data source info - use values from stored config
            stored_config = st.session_state.get("sim_config", config)
            loc = stored_config.get("location", {"name": "Berlin, Germany", "latitude": 52.52, "longitude": 13.41})
            per = stored_config.get("period", {"name": "2023-2024", "start_date": "2023-11-01", "end_date": "2024-03-31"})

            st.info(
                f"📍 **Data Source:** [Open-Meteo Historical Weather API](https://open-meteo.com/)  \n"
                f"🌍 **Location:** {loc.get('name', 'Unknown')} ({loc['latitude']}°N, {loc['longitude']}°E)  \n"
                f"📅 **Period:** {per['start_date']} to {per['end_date']}  \n"
                f"⏱️ **Resolution:** 15-minute intervals"
            )

            # Statistics
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                st.metric("Records", f"{len(df):,}")
            with col_stat2:
                valid_count = df["t_vorlauf_noisy"].notna().sum() if "t_vorlauf_noisy" in df.columns else df["t_vorlauf_ideal"].notna().sum()
                st.metric("Valid Points", f"{valid_count:,}")
            with col_stat3:
                vorlauf_col = "t_vorlauf_noisy" if "t_vorlauf_noisy" in df.columns else "t_vorlauf_ideal"
                st.metric("Mean Vorlauf", f"{df[vorlauf_col].mean():.1f}°C")
            with col_stat4:
                st.metric("Outdoor Range", f"{df['t_outdoor'].min():.1f} - {df['t_outdoor'].max():.1f}°C")

            # Scatter plot
            vorlauf_col = "t_vorlauf_noisy" if "t_vorlauf_noisy" in df.columns else "t_vorlauf_ideal"

            # Prepare data for plotting
            plot_df = df[["t_outdoor", vorlauf_col, "is_night"]].dropna().copy()
            plot_df["Mode"] = plot_df["is_night"].map({True: "Night", False: "Day"})

            fig = px.scatter(
                plot_df,
                x="t_outdoor",
                y=vorlauf_col,
                color="Mode",
                color_discrete_map={"Day": "orange", "Night": "blue"},
                opacity=0.5,
                labels={
                    "t_outdoor": "Outdoor Temperature (°C)",
                    vorlauf_col: "Vorlauf Temperature (°C)",
                },
                title=f"Heating Curve Scatter Plot ({noise_model_name})"
            )

            # Add theoretical heating curve lines
            t_out_range = np.linspace(df["t_outdoor"].min(), df["t_outdoor"].max(), 100)
            t_vor_day = 20 + slope * (t_room_day - t_out_range)
            t_vor_night = 20 + slope * (t_room_night - t_out_range)

            # Clip to limits
            t_vor_day = np.clip(t_vor_day, t_vorlauf_min, t_vorlauf_max)
            t_vor_night = np.clip(t_vor_night, t_vorlauf_min, t_vorlauf_max)

            fig.add_trace(go.Scatter(
                x=t_out_range, y=t_vor_day,
                mode="lines",
                name="Day Curve (theory)",
                line=dict(color="red", width=2, dash="dash")
            ))
            fig.add_trace(go.Scatter(
                x=t_out_range, y=t_vor_night,
                mode="lines",
                name="Night Curve (theory)",
                line=dict(color="darkblue", width=2, dash="dash")
            ))

            fig.update_layout(
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
            )

            st.plotly_chart(fig, use_container_width=True)

            # Download button
            st.download_button(
                label="📥 Download Simulated Data (CSV)",
                data=df.to_csv(),
                file_name="heating_curve_simulation.csv",
                mime="text/csv",
            )


# =============================================================================
# Tab 2: Analysis
# =============================================================================

with tab2:
    st.header("Heating Curve Parameter Extraction")
    st.markdown("""
    Extract heating curve parameters from simulated or uploaded sensor data
    using OLS and RANSAC regression algorithms.
    """)

    # Data source selection
    data_source = st.radio(
        "Data Source",
        options=["Use Simulated Data", "Upload CSV"],
        horizontal=True,
    )

    analysis_df = None
    ground_truth = None

    if data_source == "Use Simulated Data":
        if "sim_data" in st.session_state:
            analysis_df = st.session_state["sim_data"].copy()
            # Rename column for analysis
            if "t_vorlauf_noisy" in analysis_df.columns:
                analysis_df["t_vorlauf"] = analysis_df["t_vorlauf_noisy"]
            else:
                analysis_df["t_vorlauf"] = analysis_df["t_vorlauf_ideal"]

            # Get ground truth from simulation config
            if "sim_config" in st.session_state:
                sim_config = st.session_state["sim_config"]
                ground_truth = {
                    "slope": sim_config["slope"],
                    "T_room_day": sim_config["t_room_day"],
                    "T_room_night": sim_config["t_room_night"],
                }
        else:
            st.warning("No simulated data available. Generate data in the Simulation tab first.")
            st.stop()
    else:
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=["csv"],
            help="CSV must contain columns: t_outdoor, t_vorlauf"
        )
        if uploaded_file is not None:
            try:
                analysis_df = pd.read_csv(uploaded_file, parse_dates=True, index_col=0)
                if "t_outdoor" not in analysis_df.columns or "t_vorlauf" not in analysis_df.columns:
                    st.error("CSV must contain 't_outdoor' and 't_vorlauf' columns")
                    st.stop()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                st.stop()
        else:
            st.info("Please upload a CSV file with 't_outdoor' and 't_vorlauf' columns.")
            st.stop()

    if analysis_df is not None:
        # Algorithm selection
        st.subheader("Algorithm Selection")
        col_algo1, col_algo2 = st.columns(2)
        with col_algo1:
            use_ols = st.checkbox("OLS (Ordinary Least Squares)", value=True)
        with col_algo2:
            use_ransac = st.checkbox("RANSAC (Outlier Robust)", value=True)

        algorithms = []
        if use_ols:
            algorithms.append("OLS")
        if use_ransac:
            algorithms.append("RANSAC")

        if not algorithms:
            st.warning("Select at least one algorithm")
            st.stop()

        # Run analysis
        if st.button("🔍 Extract Parameters", type="primary"):
            with st.spinner("Extracting parameters..."):
                results = extract_parameters(
                    analysis_df,
                    outdoor_col="t_outdoor",
                    vorlauf_col="t_vorlauf",
                    algorithms=algorithms,
                    t_base=20.0,
                    use_detected_modes=False if "is_night" in analysis_df.columns else True,
                    is_night_col="is_night"
                )
                st.session_state["analysis_results"] = results

        # Display results
        if "analysis_results" in st.session_state:
            results = st.session_state["analysis_results"]

            st.subheader("Extracted Parameters")

            # Detected limits
            col_lim1, col_lim2 = st.columns(2)
            with col_lim1:
                upper = results["detected_limits"]["upper"]
                st.metric(
                    "Detected Upper Limit",
                    f"{upper:.1f}°C" if upper else "Not detected"
                )
            with col_lim2:
                lower = results["detected_limits"]["lower"]
                st.metric(
                    "Detected Lower Limit",
                    f"{lower:.1f}°C" if lower else "Not detected"
                )

            st.divider()

            # Results table
            for algo, algo_results in results["algorithms"].items():
                params = algo_results.get("parameters", {})

                st.markdown(f"**{algo} Results**")

                col_res1, col_res2, col_res3 = st.columns(3)

                with col_res1:
                    K = params.get("K", float("nan"))
                    if ground_truth:
                        err = abs(K - ground_truth["slope"])
                        st.metric("Slope (K)", f"{K:.4f}", delta=f"Error: {err:.4f}")
                    else:
                        st.metric("Slope (K)", f"{K:.4f}")

                with col_res2:
                    T_day = params.get("T_room_day", float("nan"))
                    if ground_truth:
                        err = abs(T_day - ground_truth["T_room_day"])
                        st.metric("T_room Day", f"{T_day:.2f}°C", delta=f"Error: {err:.2f}°C")
                    else:
                        st.metric("T_room Day", f"{T_day:.2f}°C")

                with col_res3:
                    T_night = params.get("T_room_night", float("nan"))
                    if ground_truth:
                        err = abs(T_night - ground_truth["T_room_night"])
                        st.metric("T_room Night", f"{T_night:.2f}°C", delta=f"Error: {err:.2f}°C")
                    else:
                        st.metric("T_room Night", f"{T_night:.2f}°C")

                # R² scores
                if algo_results.get("day"):
                    r2_day = algo_results["day"].get("r2", float("nan"))
                    st.caption(f"R² (Day): {r2_day:.4f}")

                st.divider()

            # Comparison with ground truth
            if ground_truth:
                st.subheader("Ground Truth Comparison")
                st.markdown(f"""
                | Parameter | Ground Truth |
                |-----------|--------------|
                | Slope (K) | {ground_truth['slope']:.4f} |
                | T_room Day | {ground_truth['T_room_day']:.2f}°C |
                | T_room Night | {ground_truth['T_room_night']:.2f}°C |
                """)


# =============================================================================
# Footer
# =============================================================================

st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8em;">
    Heating Curve Simulator | Part of the Residential Energy Systems Project<br>
    <a href="https://github.com/albertodiazdurana">GitHub</a>
</div>
""", unsafe_allow_html=True)
