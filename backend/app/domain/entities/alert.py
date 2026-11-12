from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4


class AlertType(str, Enum):
    AMOUNT_ANOMALY = "AMOUNT_ANOMALY"
    GEOLOCATION_ANOMALY = "GEOLOCATION_ANOMALY"
    TRANSACTION_VELOCITY = "TRANSACTION_VELOCITY"
    MULTIPLE_DECLINES = "MULTIPLE_DECLINES"
    MANUAL = "MANUAL"


class AlertSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


@dataclass
class Alert:
    transaction_id: UUID
    alert_type: AlertType
    severity: AlertSeverity
    description: str

    id: UUID = field(default_factory=uuid4)
    status: AlertStatus = AlertStatus.NEW
    risk_score: Decimal | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
