from pydantic import BaseModel, Field, ConfigDict
from app.schemas.money import MoneyRequest
from decimal import Decimal
from uuid import UUID
from datetime import datetime


class TransactionRequest(BaseModel):
    amount: MoneyRequest
    mti: str = Field(min_length=4, max_length=4)
    stan: str = Field(min_length=6, max_length=6)
    response_code: str = Field(min_length=2, max_length=2)


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    amount: Decimal
    currency: str
    mti: str
    stan: str
    response_code: str
    created_at: datetime
