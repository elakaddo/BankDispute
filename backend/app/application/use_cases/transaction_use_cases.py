from typing import List

from uuid import UUID

from app.domain.entities.transaction import Transaction
from app.infrastructure.repositories.transaction_repository import TransactionRepository
from app.infrastructure.database.models.transaction import TransactionModel


class TransactionUseCases:

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def create(self, transaction: Transaction) -> Transaction:
        return await self.repository.save(transaction)

    async def get_all(self) -> List[TransactionModel]:
        return await self.repository.findAll()

    async def get_by_id(self, transaction_id: UUID) -> TransactionModel | None:
        return await self.repository.findById(transaction_id)

    async def delete(self, transaction_id: UUID) -> bool:
        return await self.repository.deleteById(transaction_id)
