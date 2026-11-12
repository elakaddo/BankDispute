"""enrich transaction model

Revision ID: 33c885fbb224
Revises: 3af4c5116514
Create Date: 2026-11-12 01:10:50.738723
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "33c885fbb224"
down_revision: str | Sequence[str] | None = "3af4c5116514"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

channel_enum = postgresql.ENUM(
    "POS",
    "ECOMMERCE",
    "ATM",
    name="transaction_channel",
)

channel_enum.create(op.get_bind(), checkfirst=True)


def upgrade() -> None:
    # Ajouter les colonnes obligatoires temporairement nullable
    op.add_column(
        "transactions",
        sa.Column("transaction_date", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("card_token", sa.String(100), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("merchant_id", sa.String(50), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("terminal_id", sa.String(50), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("merchant_category_code", sa.String(4), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column(
            "channel",
            channel_enum,
            nullable=True,
        ),
    )
    op.add_column(
        "transactions",
        sa.Column("entry_mode", sa.String(20), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("merchant_country", sa.String(2), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("card_country", sa.String(2), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("device_id", sa.String(100), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("is_card_present", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("three_ds_version", sa.String(10), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("three_ds_status", sa.String(30), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("authentication_method", sa.String(30), nullable=True),
    )

    # Migrer les anciennes transactions avec des valeurs fictives
    op.execute("""
        UPDATE transactions
        SET
            transaction_date = created_at,
            card_token = 'legacy_' || id::text,
            merchant_id = 'UNKNOWN',
            merchant_category_code = '0000',
            channel = 'POS',
            entry_mode = 'UNKNOWN',
            merchant_country = 'FR',
            is_card_present = TRUE
    """)

    # Rendre les colonnes obligatoires
    for column in (
        "transaction_date",
        "card_token",
        "merchant_id",
        "merchant_category_code",
        "channel",
        "entry_mode",
        "merchant_country",
        "is_card_present",
    ):
        op.alter_column(
            "transactions",
            column,
            existing_type=sa.String(),
            nullable=False,
        )


def downgrade() -> None:
    op.drop_column("transactions", "authentication_method")
    op.drop_column("transactions", "three_ds_status")
    op.drop_column("transactions", "three_ds_version")
    op.drop_column("transactions", "is_card_present")
    op.drop_column("transactions", "device_id")
    op.drop_column("transactions", "card_country")
    op.drop_column("transactions", "merchant_country")
    op.drop_column("transactions", "entry_mode")
    op.drop_column("transactions", "channel")
    channel_enum.drop(op.get_bind(), checkfirst=True)
    op.drop_column("transactions", "merchant_category_code")
    op.drop_column("transactions", "terminal_id")
    op.drop_column("transactions", "merchant_id")
    op.drop_column("transactions", "card_token")
    op.drop_column("transactions", "transaction_date")
