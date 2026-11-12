from uuid import UUID

from app.domain.entities.transaction import Transaction
from app.infrastructure.database.models.transaction import TransactionModel
from app.infrastructure.repositories.transaction_repository import (
    TransactionRepository,
)


class TransactionUseCases:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def create(self, transaction: Transaction) -> TransactionModel:
        return await self.repository.save(transaction)

    async def get_all(self) -> list[TransactionModel]:
        return await self.repository.findAll()

    async def get_by_id(self, transaction_id: UUID) -> TransactionModel | None:
        return await self.repository.findById(transaction_id)

    async def delete(self, transaction_id: UUID) -> bool:
        return await self.repository.deleteById(transaction_id)
