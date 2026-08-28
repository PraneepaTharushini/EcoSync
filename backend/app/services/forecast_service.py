import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.panel_spec import PanelSpec
from app.models.predicted_output import PredictedOutput
from app.models.weather_forecast import WeatherForecast

logger = logging.getLogger("forecast_service")

STANDARD_TEST_IRRADIANCE = 1000.0
DEFAULT_PERFORMANCE_RATIO = 0.80

ORIENTATION_FACTOR = {
    "S": 1.00,
    "N": 0.92,
    "E": 0.95,
    "W": 0.95,
}


def calculate_physics_baseline(
    irradiance: float,
    capacity_kw: float,
    orientation: str = "S",
    performance_ratio: float = DEFAULT_PERFORMANCE_RATIO,
) -> float:
    """
    Predicts kWh output for a single hour given that hour's irradiance and the
    panel's rated capacity. This is the physics-formula fallback — used if the
    ML model is unavailable or fails for any reason.
    """
    if irradiance is None or irradiance <= 0:
        return 0.0

    orientation_factor = ORIENTATION_FACTOR.get(orientation, 1.0)
    predicted_kwh = (
        (irradiance / STANDARD_TEST_IRRADIANCE)
        * capacity_kw
        * performance_ratio
        * orientation_factor
    )
    return round(predicted_kwh, 4)


def predict_hour(w: WeatherForecast, panel_spec: PanelSpec) -> tuple[float, str]:
    """
    Predicts kWh for one hour, preferring the trained ML model and falling
    back to the physics baseline if the model is unavailable or errors.
    Returns (predicted_kwh, model_version).
    """
    try:
        from app.ml.model_runtime import predict_kwh

        kwh = predict_kwh(
            irradiance=w.irradiance or 0.0,
            ambient_temperature=w.temperature or 25.0,
            forecast_time=w.forecast_time,
            capacity_kw=panel_spec.capacity_kw,
        )
        return kwh, "rf-v1"
    except Exception as e:
        logger.warning(f"ML prediction failed, falling back to physics baseline: {e}")
        kwh = calculate_physics_baseline(
            irradiance=w.irradiance,
            capacity_kw=panel_spec.capacity_kw,
            orientation=panel_spec.orientation,
        )
        return kwh, "physics-baseline-v1"


def generate_forecast_for_panel_spec(panel_spec: PanelSpec, db: Session) -> int:
    """
    Looks up cached weather for this panel's location, predicts each hour
    (ML model preferred, physics baseline as fallback), and upserts the
    results into predicted_output. Returns the number of hours predicted.
    """
    weather_rows = (
        db.query(WeatherForecast)
        .filter(
            WeatherForecast.latitude == panel_spec.latitude,
            WeatherForecast.longitude == panel_spec.longitude,
        )
        .order_by(WeatherForecast.forecast_time)
        .all()
    )

    count = 0
    for w in weather_rows:
        predicted_kwh, model_version = predict_hour(w, panel_spec)

        existing = (
            db.query(PredictedOutput)
            .filter(
                PredictedOutput.user_id == panel_spec.user_id,
                PredictedOutput.forecast_time == w.forecast_time,
            )
            .first()
        )

        if existing:
            existing.predicted_kwh = predicted_kwh
            existing.model_version = model_version
        else:
            db.add(
                PredictedOutput(
                    user_id=panel_spec.user_id,
                    forecast_time=w.forecast_time,
                    predicted_kwh=predicted_kwh,
                    model_version=model_version,
                )
            )
        count += 1

    db.commit()
    return count