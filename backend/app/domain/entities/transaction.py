from dataclasses import dataclass, field as dataclass_field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.value_objects.money import Money


@dataclass
class Transaction:
    amount: Money
    mti: str
    stan: str
    response_code: str

    id: UUID = dataclass_field(default_factory=uuid4)
    created_at: datetime = dataclass_field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
