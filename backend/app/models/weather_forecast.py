import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    forecast_time = Column(DateTime(timezone=True), nullable=False, index=True)

    cloud_cover = Column(Float, nullable=True)
    uv_index = Column(Float, nullable=True)
    irradiance = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)

    fetched_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))