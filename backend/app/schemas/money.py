from pydantic import Field
from decimal import Decimal

from pydantic import BaseModel


class MoneyRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
