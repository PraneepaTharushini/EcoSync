from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.panel_spec import PanelSpec
from app.models.predicted_output import PredictedOutput
from app.models.weather_forecast import WeatherForecast

STANDARD_TEST_IRRADIANCE = 1000.0  # W/m^2, the irradiance panels are rated at
DEFAULT_PERFORMANCE_RATIO = 0.80  # accounts for real-world losses: dust, wiring, inverter, heat

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
    panel's rated capacity. This is the physics-formula fallback — no ML, no
    historical training data required, works from day one.
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


def generate_forecast_for_panel_spec(panel_spec: PanelSpec, db: Session) -> int:
    """
    Looks up cached weather for this panel's location, runs the physics baseline
    on every available hour, and upserts the results into predicted_output.
    Returns the number of hours predicted.
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
        predicted_kwh = calculate_physics_baseline(
            irradiance=w.irradiance,
            capacity_kw=panel_spec.capacity_kw,
            orientation=panel_spec.orientation,
        )

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
            existing.model_version = "physics-baseline-v1"
        else:
            db.add(
                PredictedOutput(
                    user_id=panel_spec.user_id,
                    forecast_time=w.forecast_time,
                    predicted_kwh=predicted_kwh,
                    model_version="physics-baseline-v1",
                )
            )
        count += 1

    db.commit()
    return count