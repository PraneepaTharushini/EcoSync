"""
Loads the trained Random Forest model and exposes a predict function that
takes the SAME fields your live WeatherForecast rows already have (irradiance,
temperature) plus a timestamp and capacity_kw - no extra data collection needed.

Bridges one real gap: the training data included MODULE_TEMPERATURE (a solar
panel's own surface temperature, measured directly by the sensor), but
Open-Meteo only gives ambient air temperature. We estimate module temperature
using a standard, published approximation (not invented for this project):

    module_temp ≈ ambient_temp + irradiance_ratio * (NOCT - 20)

where NOCT (Nominal Operating Cell Temperature) is a standard panel spec,
typically ~45°C, published by every panel manufacturer. This is the same
approximation used in NREL's own PVWatts calculator.
"""
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

MODEL_PATH = Path(__file__).parent / "models" / "rf_v1.joblib"
NOCT_CELSIUS = 45.0  # typical published Nominal Operating Cell Temperature

_bundle = None


def _load():
    global _bundle
    if _bundle is None:
        _bundle = joblib.load(MODEL_PATH)
    return _bundle


def estimate_module_temperature(ambient_temp: float, irradiance_ratio: float) -> float:
    return ambient_temp + irradiance_ratio * (NOCT_CELSIUS - 20)


def predict_kwh(
    irradiance: float,
    ambient_temperature: float,
    forecast_time: datetime,
    capacity_kw: float,
) -> float:
    """
    irradiance: W/m^2, as stored in your WeatherForecast rows (Open-Meteo's
                direct_radiation field).
    ambient_temperature: degrees C, from WeatherForecast.temperature.
    forecast_time: the hour being predicted.
    capacity_kw: the user's real panel capacity from PanelSpec.

    Returns predicted kWh for that hour.
    """
    bundle = _load()
    model = bundle["model"]

    irradiance_ratio = max(irradiance, 0.0) / 1000.0  # match training data's normalization
    module_temp = estimate_module_temperature(ambient_temperature, irradiance_ratio)

    features = pd.DataFrame([{
        "irradiance_ratio": irradiance_ratio,
        "AMBIENT_TEMPERATURE": ambient_temperature,
        "MODULE_TEMPERATURE": module_temp,
        "hour_of_day": forecast_time.hour,
        "day_of_year": forecast_time.timetuple().tm_yday,
    }])[bundle["feature_cols"]]

    capacity_factor = model.predict(features)[0]
    capacity_factor = max(0.0, capacity_factor)  # never predict negative output

    
    return float(round(capacity_factor * capacity_kw, 4))