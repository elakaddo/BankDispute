from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.alert import (
    AlertType,
    AlertSeverity,
    AlertStatus,
)


class AlertRequest(BaseModel):
    transaction_id: UUID
    alert_type: AlertType
    severity: AlertSeverity
    description: str = Field(min_length=1, max_length=1000)
    risk_score: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        decimal_places=2,
    )


class AlertStatusUpdate(BaseModel):
    status: AlertStatus


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    transaction_id: UUID
    alert_type: AlertType
    severity: AlertSeverity
    status: AlertStatus
    description: str
    risk_score: Decimal | None
    created_at: datetime
    updated_at: datetime
