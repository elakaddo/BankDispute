from dataclasses import dataclass
from dataclasses import field as dataclass_field
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from app.domain.value_objects.money import Money


class TransactionChannel(str, Enum):
    POS = "POS"
    ECOMMERCE = "ECOMMERCE"
    ATM = "ATM"


@dataclass
class Transaction:
    amount: Money
    mti: str
    stan: str
    response_code: str
    transaction_date: datetime
    card_token: str
    merchant_id: str
    merchant_category_code: str
    channel: TransactionChannel
    entry_mode: str
    merchant_country: str
    is_card_present: bool

    id: UUID = dataclass_field(default_factory=uuid4)
    terminal_id: str | None = None
    card_country: str | None = None
    device_id: str | None = None
    three_ds_version: str | None = None
    three_ds_status: str | None = None
    authentication_method: str | None = None
    created_at: datetime = dataclass_field(default_factory=lambda: datetime.now(UTC))
