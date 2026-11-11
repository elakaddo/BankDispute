import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import UUID, Numeric, String, DateTime, func


from app.infrastructure.database.db import Base

from sqlalchemy.orm import Mapped, mapped_column


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    mti: Mapped[str] = mapped_column(String(4), nullable=False)

    stan: Mapped[str] = mapped_column(String(6), nullable=False)

    response_code: Mapped[str] = mapped_column(String(2), nullable=False)
