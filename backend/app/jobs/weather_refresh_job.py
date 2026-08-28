import logging

from app.database import SessionLocal
from app.models.panel_spec import PanelSpec
from app.services.forecast_service import generate_forecast_for_panel_spec
from app.services.weather_service import fetch_weather, normalize_and_store

logger = logging.getLogger("weather_refresh_job")


def refresh_all_locations() -> None:
    """
    Refreshes weather (and regenerates predictions) for every distinct
    location that has at least one panel spec registered.
    """
    db = SessionLocal()
    try:
        panel_specs = db.query(PanelSpec).all()

        seen_locations = set()
        refreshed = 0
        failed = 0

        for spec in panel_specs:
            location_key = (spec.latitude, spec.longitude)

            if location_key not in seen_locations:
                try:
                    raw = fetch_weather(spec.latitude, spec.longitude)
                    normalize_and_store(raw, db, lat=spec.latitude, lon=spec.longitude)
                    seen_locations.add(location_key)
                except Exception as e:
                    logger.warning(f"Weather refresh failed for {location_key}: {e}")
                    failed += 1
                    continue

            generate_forecast_for_panel_spec(spec, db)
            refreshed += 1

        logger.info(
            f"Weather refresh job complete: {refreshed} panel specs updated, "
            f"{len(seen_locations)} unique locations fetched, {failed} failures."
        )
    finally:
        db.close()