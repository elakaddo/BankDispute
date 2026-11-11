from typing import List

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.domain.entities.transaction import Transaction

from app.schemas.transactionFormat import (
    TransactionRequest,
    TransactionResponse,
)
from app.application.use_cases.transaction_use_cases import TransactionUseCases
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.db import get_db
from app.infrastructure.repositories.transaction_repository import TransactionRepository
from app.domain.value_objects.money import Money

router = APIRouter(tags=["Transactions"])


def get_transaction_use_cases(
    session: AsyncSession = Depends(get_db),
) -> TransactionUseCases:
    repository = TransactionRepository(session)
    return TransactionUseCases(repository)


@router.post("/transactions", status_code=201)
async def create_transaction(
    request: TransactionRequest,
    use_cases: TransactionUseCases = Depends(get_transaction_use_cases),
) -> Transaction:
    transaction = Transaction(
        amount=Money(amount=request.amount.amount, currency=request.amount.currency),
        mti=request.mti,
        stan=request.stan,
        response_code=request.response_code,
    )
    return await use_cases.create(transaction)


@router.get("/transactions", status_code=200)
async def get_all_transactions(
    use_cases: TransactionUseCases = Depends(get_transaction_use_cases),
) -> List[TransactionResponse]:
    return await use_cases.get_all()


@router.get("/transactions/{id}", status_code=200, response_model=TransactionResponse)
async def get_transaction_by_id(
    id: UUID,
    use_cases: TransactionUseCases = Depends(get_transaction_use_cases),
) -> TransactionResponse:
    transaction = await use_cases.get_by_id(id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.delete("/transactions/{id}", status_code=204)
async def delete_transaction_by_id(
    id: UUID,
    use_cases: TransactionUseCases = Depends(get_transaction_use_cases),
):
    deleted = await use_cases.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
