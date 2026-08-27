from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.panel_spec import PanelSpec
from app.models.predicted_output import PredictedOutput
from app.models.user import User
from app.models.weather_forecast import WeatherForecast
from app.services.forecast_service import generate_forecast_for_panel_spec
from app.services.weather_service import fetch_weather, normalize_and_store

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("/raw")
def get_raw_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    db: Session = Depends(get_db),
):
    try:
        raw = fetch_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Could not reach weather provider: {e}")

    stored_count = normalize_and_store(raw, db)

    rows = (
        db.query(WeatherForecast)
        .filter(WeatherForecast.latitude == raw["latitude"], WeatherForecast.longitude == raw["longitude"])
        .order_by(WeatherForecast.forecast_time)
        .all()
    )

    return {
        "latitude": raw["latitude"],
        "longitude": raw["longitude"],
        "stored_count": stored_count,
        "hourly": [
            {
                "forecast_time": r.forecast_time.isoformat(),
                "cloud_cover": r.cloud_cover,
                "uv_index": r.uv_index,
                "irradiance": r.irradiance,
                "temperature": r.temperature,
            }
            for r in rows
        ],
    }


@router.get("/predicted")
def get_predicted_forecast(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the logged-in user's predicted kWh output per hour, based on their
    saved panel spec and the most recently cached weather for their location.
    """
    panel_spec = (
        db.query(PanelSpec)
        .filter(PanelSpec.user_id == current_user.id)
        .first()
    )

    if not panel_spec:
        raise HTTPException(
            status_code=404,
            detail="No panel spec found for this user. Complete onboarding first.",
        )

    try:
        raw = fetch_weather(panel_spec.latitude, panel_spec.longitude)
        normalize_and_store(raw, db)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Could not reach weather provider: {e}")

    count = generate_forecast_for_panel_spec(panel_spec, db)

    predictions = (
        db.query(PredictedOutput)
        .filter(PredictedOutput.user_id == current_user.id)
        .order_by(PredictedOutput.forecast_time)
        .all()
    )

    return {
        "user_id": str(current_user.id),
        "capacity_kw": panel_spec.capacity_kw,
        "orientation": panel_spec.orientation,
        "predicted_count": count,
        "hourly": [
            {
                "forecast_time": p.forecast_time.isoformat(),
                "predicted_kwh": p.predicted_kwh,
                "model_version": p.model_version,
            }
            for p in predictions
        ],
    }