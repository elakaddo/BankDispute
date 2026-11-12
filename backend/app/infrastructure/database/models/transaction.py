import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    UUID,
    Boolean,
    DateTime,
    Enum,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.entities.transaction import TransactionChannel
from app.infrastructure.database.db import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    mti: Mapped[str] = mapped_column(String(4), nullable=False)
    stan: Mapped[str] = mapped_column(String(6), nullable=False)
    response_code: Mapped[str] = mapped_column(String(2), nullable=False)

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    card_token: Mapped[str] = mapped_column(String(100), nullable=False)
    merchant_id: Mapped[str] = mapped_column(String(50), nullable=False)
    terminal_id: Mapped[str | None] = mapped_column(String(50), nullable=True)

    merchant_category_code: Mapped[str] = mapped_column(String(4), nullable=False)

    channel: Mapped[TransactionChannel] = mapped_column(
        Enum(TransactionChannel, name="transaction_channel"),
        nullable=False,
    )

    entry_mode: Mapped[str] = mapped_column(String(20), nullable=False)

    merchant_country: Mapped[str] = mapped_column(String(2), nullable=False)
    card_country: Mapped[str | None] = mapped_column(String(2), nullable=True)

    device_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    is_card_present: Mapped[bool] = mapped_column(Boolean, nullable=False)

    three_ds_version: Mapped[str | None] = mapped_column(String(10), nullable=True)
    three_ds_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    authentication_method: Mapped[str | None] = mapped_column(String(30), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
