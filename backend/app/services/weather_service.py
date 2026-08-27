from datetime import datetime, timezone

import requests
from sqlalchemy.orm import Session

from app.models.weather_forecast import WeatherForecast

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather(lat: float, lon: float, forecast_days: int = 2) -> dict:
    """Calls Open-Meteo and returns the raw parsed JSON response."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "cloud_cover,uv_index,direct_radiation,temperature_2m",
        "forecast_days": forecast_days,
    }
    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def normalize_and_store(raw: dict, db: Session) -> int:
    """
    Takes the raw Open-Meteo response, zips the parallel hourly arrays into
    individual rows, and upserts them into weather_forecasts.
    Returns the number of rows written.
    """
    lat = raw["latitude"]
    lon = raw["longitude"]
    hourly = raw["hourly"]

    times = hourly["time"]
    cloud_cover = hourly["cloud_cover"]
    uv_index = hourly["uv_index"]
    irradiance = hourly["direct_radiation"]
    temperature = hourly["temperature_2m"]

    count = 0
    for i, time_str in enumerate(times):
        forecast_time = datetime.fromisoformat(time_str).replace(tzinfo=timezone.utc)

        existing = (
            db.query(WeatherForecast)
            .filter(
                WeatherForecast.latitude == lat,
                WeatherForecast.longitude == lon,
                WeatherForecast.forecast_time == forecast_time,
            )
            .first()
        )

        if existing:
            existing.cloud_cover = cloud_cover[i]
            existing.uv_index = uv_index[i]
            existing.irradiance = irradiance[i]
            existing.temperature = temperature[i]
            existing.fetched_at = datetime.now(timezone.utc)
        else:
            db.add(
                WeatherForecast(
                    latitude=lat,
                    longitude=lon,
                    forecast_time=forecast_time,
                    cloud_cover=cloud_cover[i],
                    uv_index=uv_index[i],
                    irradiance=irradiance[i],
                    temperature=temperature[i],
                )
            )
        count += 1

    db.commit()
    return count