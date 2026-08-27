import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class PredictedOutput(Base):
    __tablename__ = "predicted_output"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    forecast_time = Column(DateTime(timezone=True), nullable=False, index=True)
    predicted_kwh = Column(Float, nullable=False)
    model_version = Column(String, nullable=True)  # e.g. "physics-baseline", "rf-v1", "xgb-v2"

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))