from typing import List
from uuid import UUID
from sqlalchemy import select, delete
from app.domain.entities.transaction import Transaction
from sqlalchemy.ext.asyncio import AsyncSession
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
        )

    async def save(self, transaction: Transaction) -> Transaction:
        model = self._convertTransactionToModel(transaction)

        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return transaction

        except Exception:
            await self.session.rollback()
            raise

    async def findAll(self) -> List[TransactionModel]:
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
        await self.session.delete(transaction)
        await self.session.commit()
        return True
