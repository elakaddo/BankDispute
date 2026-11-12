from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.transaction import Transaction
from app.infrastructure.database.models.transaction import TransactionModel


class TransactionRepository:
    def __init__(self, sessionBDD: AsyncSession):
        self.session = sessionBDD

    def _convertTransactionToModel(self, t: Transaction) -> TransactionModel:
        return TransactionModel(
            id=t.id,
            amount=t.amount.amount,
            currency=t.amount.currency,
            mti=t.mti,
            stan=t.stan,
            response_code=t.response_code,
            transaction_date=t.transaction_date,
            card_token=t.card_token,
            merchant_id=t.merchant_id,
            terminal_id=t.terminal_id,
            merchant_category_code=t.merchant_category_code,
            channel=t.channel,
            entry_mode=t.entry_mode,
            merchant_country=t.merchant_country,
            card_country=t.card_country,
            device_id=t.device_id,
            is_card_present=t.is_card_present,
            three_ds_version=t.three_ds_version,
            three_ds_status=t.three_ds_status,
            authentication_method=t.authentication_method,
        )

    async def save(self, transaction: Transaction) -> TransactionModel:
        model = self._convertTransactionToModel(transaction)
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return model
        except Exception:
            await self.session.rollback()
            raise

    async def findAll(self) -> list[TransactionModel]:
        result = await self.session.execute(select(TransactionModel))
        return list(result.scalars().all())

    async def findById(self, transactionId: UUID) -> TransactionModel | None:
        result = await self.session.execute(
            select(TransactionModel).where(TransactionModel.id == transactionId)
        )
        return result.scalar_one_or_none()

    async def deleteById(self, transactionId: UUID) -> bool:
        transaction = await self.findById(transactionId)

        if transaction is None:
            return False

        try:
            await self.session.delete(transaction)
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            raise
