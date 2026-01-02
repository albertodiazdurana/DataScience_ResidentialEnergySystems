"""
Heating Curve Analysis Module

This module provides functions to extract heating curve parameters from
noisy sensor data. It includes pattern detection, regression algorithms,
and parameter extraction without requiring prior knowledge of system configuration.

Functions:
    detect_temperature_limits: Detect upper/lower temperature limits from data
    detect_day_night_modes: Detect day/night modes using clustering
    fit_ols: Fit OLS regression and extract parameters
    fit_ransac: Fit RANSAC regression (outlier robust)
    extract_parameters: Main function to extract heating curve parameters
    compare_with_ground_truth: Compare extracted parameters with known values
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple, Dict, Any

from sklearn.linear_model import LinearRegression, RANSACRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_absolute_error


def detect_temperature_limits(
    df: pd.DataFrame,
    vorlauf_col: str = 't_vorlauf',
    percentile_threshold: float = 0.01
) -> Tuple[Optional[float], Optional[float]]:
    """
    Detect upper and lower temperature limits from Vorlauf distribution.

    Uses percentile analysis to identify potential clamping/plateau regions.
    A limit is detected if the top/bottom percentile values have low variance
    compared to the overall data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing Vorlauf temperature column
    vorlauf_col : str
        Name of the Vorlauf temperature column
    percentile_threshold : float
        Fraction of data to analyze at each end (default 0.01 = 1%)

    Returns
    -------
    Tuple[Optional[float], Optional[float]]
        (upper_limit, lower_limit) - None if no limit detected
    """
    vorlauf = df[vorlauf_col].dropna().values
    vorlauf_sorted = np.sort(vorlauf)
    n = len(vorlauf_sorted)

    # Get top and bottom percentile data
    top_idx = int((1 - percentile_threshold) * n)
    bottom_idx = int(percentile_threshold * n)

    top_values = vorlauf_sorted[top_idx:]
    bottom_values = vorlauf_sorted[:bottom_idx]

    # Overall variability
    overall_std = np.std(vorlauf)

    # Detect limits if std is low (indicates plateau/clamping)
    upper_limit = None
    lower_limit = None

    if len(top_values) > 0:
        top_std = np.std(top_values)
        if top_std < overall_std / 3:
            upper_limit = np.mean(top_values)

    if len(bottom_values) > 0:
        bottom_std = np.std(bottom_values)
        if bottom_std < overall_std / 3:
            lower_limit = np.mean(bottom_values)

    return upper_limit, lower_limit


def detect_day_night_modes(
    df: pd.DataFrame,
    outdoor_col: str = 't_outdoor',
    vorlauf_col: str = 't_vorlauf',
    n_clusters: int = 2
) -> Tuple[np.ndarray, float]:
    """
    Detect day/night operating modes using K-Means clustering.

    Strategy: Fit a simple linear regression, then cluster residuals
    into two groups representing day (higher) and night (lower) modes.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with outdoor and Vorlauf temperature columns
    outdoor_col : str
        Name of outdoor temperature column
    vorlauf_col : str
        Name of Vorlauf temperature column
    n_clusters : int
        Number of clusters (default 2 for day/night)

    Returns
    -------
    Tuple[np.ndarray, float]
        (mode_labels, separation)
        mode_labels: Array of 'Day' or 'Night' for each row
        separation: Temperature difference between modes (°C)
    """
    # Get valid data
    mask = df[vorlauf_col].notna()
    X = df.loc[mask, outdoor_col].values.reshape(-1, 1)
    y = df.loc[mask, vorlauf_col].values

    # Fit simple linear regression
    lr = LinearRegression()
    lr.fit(X, y)
    y_pred = lr.predict(X)
    residuals = y - y_pred

    # Cluster residuals
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(residuals.reshape(-1, 1))

    # Determine which cluster is day (higher) vs night (lower)
    cluster_means = [residuals[clusters == i].mean() for i in range(n_clusters)]
    day_cluster = np.argmax(cluster_means)

    # Create labels
    labels = np.where(clusters == day_cluster, 'Day', 'Night')

    # Calculate separation
    separation = abs(cluster_means[0] - cluster_means[1])

    return labels, separation


def fit_ols(
    X: np.ndarray,
    y: np.ndarray
) -> Dict[str, Any]:
    """
    Fit OLS (Ordinary Least Squares) regression.

    Parameters
    ----------
    X : np.ndarray
        Outdoor temperatures (n_samples, 1)
    y : np.ndarray
        Vorlauf temperatures (n_samples,)

    Returns
    -------
    Dict[str, Any]
        Dictionary with:
        - slope: Regression slope
        - intercept: Regression intercept
        - r2: R² score
        - model: Fitted LinearRegression object
    """
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    return {
        'slope': model.coef_[0],
        'intercept': model.intercept_,
        'r2': r2_score(y, y_pred),
        'model': model
    }


def fit_ransac(
    X: np.ndarray,
    y: np.ndarray,
    min_samples: float = 0.8,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Fit RANSAC (Random Sample Consensus) regression.

    RANSAC is robust to outliers by iteratively fitting to inlier subsets.

    Parameters
    ----------
    X : np.ndarray
        Outdoor temperatures (n_samples, 1)
    y : np.ndarray
        Vorlauf temperatures (n_samples,)
    min_samples : float
        Minimum fraction of samples required as inliers
    random_state : int
        Random seed for reproducibility

    Returns
    -------
    Dict[str, Any]
        Dictionary with:
        - slope: Regression slope
        - intercept: Regression intercept
        - r2: R² score (on inliers only)
        - inlier_ratio: Fraction of data identified as inliers
        - model: Fitted RANSACRegressor object
    """
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)

    model = RANSACRegressor(random_state=random_state, min_samples=min_samples)
    model.fit(X, y)

    # Get inlier statistics
    inlier_mask = model.inlier_mask_
    y_pred_inliers = model.predict(X[inlier_mask])
    r2 = r2_score(y[inlier_mask], y_pred_inliers)

    return {
        'slope': model.estimator_.coef_[0],
        'intercept': model.estimator_.intercept_,
        'r2': r2,
        'inlier_ratio': inlier_mask.sum() / len(y),
        'model': model
    }


def extract_parameters(
    df: pd.DataFrame,
    outdoor_col: str = 't_outdoor',
    vorlauf_col: str = 't_vorlauf',
    algorithms: list = ['OLS', 'RANSAC'],
    t_base: float = 20.0,
    use_detected_modes: bool = False,
    is_night_col: Optional[str] = 'is_night'
) -> Dict[str, Any]:
    """
    Extract heating curve parameters from sensor data.

    This is the main entry point for analysis. It combines pattern detection,
    regression, and parameter extraction.

    The heating curve formula is:
        T_vorlauf = T_base + K * (T_room - T_outdoor)

    Which expands to:
        T_vorlauf = (T_base + K*T_room) - K*T_outdoor

    So: regression slope = -K, intercept = T_base + K*T_room

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with outdoor and Vorlauf temperature columns
    outdoor_col : str
        Name of outdoor temperature column
    vorlauf_col : str
        Name of Vorlauf temperature column
    algorithms : list
        List of algorithms to apply: 'OLS', 'RANSAC'
    t_base : float
        Assumed base temperature for parameter extraction (default 20°C)
    use_detected_modes : bool
        If True, use clustering to detect day/night modes.
        If False, use is_night_col from data.
    is_night_col : str, optional
        Column name for night mode indicator (used if use_detected_modes=False)

    Returns
    -------
    Dict[str, Any]
        Dictionary with:
        - detected_limits: (upper, lower) temperature limits
        - mode_separation: Temperature difference between day/night
        - results: Dict of algorithm results with extracted parameters
    """
    results = {
        'detected_limits': {'upper': None, 'lower': None},
        'mode_separation': None,
        'algorithms': {}
    }

    # Step 1: Detect temperature limits
    upper_limit, lower_limit = detect_temperature_limits(df, vorlauf_col)
    results['detected_limits']['upper'] = upper_limit
    results['detected_limits']['lower'] = lower_limit

    # Step 2: Filter to linear region (away from clamping)
    if upper_limit is not None and lower_limit is not None:
        upper_threshold = upper_limit - 1.0
        lower_threshold = lower_limit + 1.0
        linear_mask = (
            (df[vorlauf_col] < upper_threshold) &
            (df[vorlauf_col] > lower_threshold) &
            (df[vorlauf_col].notna())
        )
    else:
        linear_mask = df[vorlauf_col].notna()

    df_linear = df[linear_mask].copy()

    # Step 3: Detect or use day/night modes
    if use_detected_modes:
        mode_labels, separation = detect_day_night_modes(
            df_linear, outdoor_col, vorlauf_col
        )
        results['mode_separation'] = separation
        day_mask = mode_labels == 'Day'
        night_mask = mode_labels == 'Night'
    else:
        if is_night_col in df_linear.columns:
            day_mask = ~df_linear[is_night_col].values
            night_mask = df_linear[is_night_col].values
        else:
            # If no mode info, treat all as day
            day_mask = np.ones(len(df_linear), dtype=bool)
            night_mask = np.zeros(len(df_linear), dtype=bool)

    # Step 4: Prepare data for regression
    X_day = df_linear.loc[day_mask, outdoor_col].values.reshape(-1, 1)
    y_day = df_linear.loc[day_mask, vorlauf_col].values
    X_night = df_linear.loc[night_mask, outdoor_col].values.reshape(-1, 1)
    y_night = df_linear.loc[night_mask, vorlauf_col].values

    # Step 5: Apply each algorithm
    for algo in algorithms:
        algo_results = {'day': {}, 'night': {}, 'parameters': {}}

        if algo.upper() == 'OLS':
            # Day mode
            if len(X_day) > 0:
                day_fit = fit_ols(X_day, y_day)
                algo_results['day'] = day_fit

            # Night mode
            if len(X_night) > 0:
                night_fit = fit_ols(X_night, y_night)
                algo_results['night'] = night_fit

        elif algo.upper() == 'RANSAC':
            # Day mode
            if len(X_day) > 10:  # RANSAC needs minimum samples
                day_fit = fit_ransac(X_day, y_day)
                algo_results['day'] = day_fit

            # Night mode
            if len(X_night) > 10:
                night_fit = fit_ransac(X_night, y_night)
                algo_results['night'] = night_fit

        # Extract heating curve parameters from regression
        if algo_results['day']:
            K = -algo_results['day']['slope']  # Heating curve slope
            T_room_day = (algo_results['day']['intercept'] - t_base) / K

            algo_results['parameters']['K'] = K
            algo_results['parameters']['T_room_day'] = T_room_day

            if algo_results['night']:
                T_room_night = (algo_results['night']['intercept'] - t_base) / K
                algo_results['parameters']['T_room_night'] = T_room_night

        results['algorithms'][algo] = algo_results

    return results


def compare_with_ground_truth(
    extracted: Dict[str, Any],
    ground_truth: Dict[str, float]
) -> Dict[str, Dict[str, float]]:
    """
    Compare extracted parameters with ground truth values.

    Parameters
    ----------
    extracted : Dict[str, Any]
        Results from extract_parameters()
    ground_truth : Dict[str, float]
        Dictionary with keys: 'slope', 'T_room_day', 'T_room_night'

    Returns
    -------
    Dict[str, Dict[str, float]]
        Dictionary with errors for each algorithm
    """
    comparison = {}

    for algo, algo_results in extracted['algorithms'].items():
        params = algo_results.get('parameters', {})
        errors = {}

        if 'K' in params:
            errors['K_error'] = abs(params['K'] - ground_truth['slope'])

        if 'T_room_day' in params:
            errors['T_day_error'] = abs(params['T_room_day'] - ground_truth['T_room_day'])

        if 'T_room_night' in params:
            errors['T_night_error'] = abs(params['T_room_night'] - ground_truth['T_room_night'])

        comparison[algo] = {
            'extracted': params,
            'errors': errors
        }

    return comparison


def format_results_table(
    all_results: Dict[str, Dict],
    ground_truth: Optional[Dict[str, float]] = None
) -> str:
    """
    Format extraction results as a text table.

    Parameters
    ----------
    all_results : Dict[str, Dict]
        Dictionary mapping model names to extract_parameters() results
    ground_truth : Dict, optional
        Ground truth for error calculation

    Returns
    -------
    str
        Formatted table string
    """
    lines = []
    lines.append("=" * 80)
    lines.append("HEATING CURVE EXTRACTION RESULTS")
    lines.append("=" * 80)

    for model_name, results in all_results.items():
        lines.append(f"\n{model_name}:")
        lines.append("-" * 80)
        lines.append(f"{'Algorithm':<10} {'K':<10} {'T_day (°C)':<12} {'T_night (°C)':<14}")

        if ground_truth:
            lines[-1] += f"{'K Error':<10} {'T_day Err':<12} {'T_night Err':<12}"

        lines.append("-" * 80)

        for algo, algo_results in results['algorithms'].items():
            params = algo_results.get('parameters', {})
            K = params.get('K', float('nan'))
            T_day = params.get('T_room_day', float('nan'))
            T_night = params.get('T_room_night', float('nan'))

            line = f"{algo:<10} {K:<10.4f} {T_day:<12.2f} {T_night:<14.2f}"

            if ground_truth:
                K_err = abs(K - ground_truth['slope'])
                T_day_err = abs(T_day - ground_truth['T_room_day'])
                T_night_err = abs(T_night - ground_truth['T_room_night'])
                line += f"{K_err:<10.4f} {T_day_err:<12.2f} {T_night_err:<12.2f}"

            lines.append(line)

    return "\n".join(lines)
