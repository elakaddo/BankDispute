from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.transaction import TransactionChannel
from app.schemas.money import MoneyRequest


class TransactionRequest(BaseModel):
    amount: MoneyRequest

    mti: str = Field(min_length=4, max_length=4)
    stan: str = Field(min_length=6, max_length=6)
    response_code: str = Field(min_length=2, max_length=2)

    transaction_date: datetime

    card_token: str = Field(min_length=1, max_length=100)
    merchant_id: str = Field(min_length=1, max_length=50)
    terminal_id: str | None = Field(default=None, max_length=50)

    merchant_category_code: str = Field(min_length=4, max_length=4)

    channel: TransactionChannel
    entry_mode: str = Field(min_length=1, max_length=20)

    merchant_country: str = Field(min_length=2, max_length=2)
    card_country: str | None = Field(default=None, min_length=2, max_length=2)

    device_id: str | None = Field(default=None, max_length=100)

    is_card_present: bool

    three_ds_version: str | None = Field(default=None, max_length=10)
    three_ds_status: str | None = Field(default=None, max_length=30)
    authentication_method: str | None = Field(default=None, max_length=30)


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    amount: Decimal
    currency: str

    mti: str
    stan: str
    response_code: str

    transaction_date: datetime

    card_token: str
    merchant_id: str
    terminal_id: str | None

    merchant_category_code: str
    channel: TransactionChannel
    entry_mode: str

    merchant_country: str
    card_country: str | None
    device_id: str | None

    is_card_present: bool

    three_ds_version: str | None
    three_ds_status: str | None
    authentication_method: str | None

    created_at: datetime
