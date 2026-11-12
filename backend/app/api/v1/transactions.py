from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.transaction_use_cases import TransactionUseCases
from app.domain.entities.transaction import Transaction
from app.domain.value_objects.money import Money
from app.infrastructure.database.db import get_db
from app.infrastructure.repositories.transaction_repository import TransactionRepository
from app.schemas.transactionFormat import TransactionRequest, TransactionResponse

router = APIRouter(tags=["Transactions"])


def get_transaction_use_cases(
    session: AsyncSession = Depends(get_db),
) -> TransactionUseCases:
    repository = TransactionRepository(session)
    return TransactionUseCases(repository)


@router.post(
    "/transactions",
    status_code=201,
    response_model=TransactionResponse,
)
async def create_transaction(
    request: TransactionRequest,
    use_cases: TransactionUseCases = Depends(get_transaction_use_cases),
):
    transaction = Transaction(
        amount=Money(
            amount=request.amount.amount,
            currency=request.amount.currency,
        ),
        mti=request.mti,
        stan=request.stan,
        response_code=request.response_code,
        transaction_date=request.transaction_date,
        card_token=request.card_token,
        merchant_id=request.merchant_id,
        terminal_id=request.terminal_id,
        merchant_category_code=request.merchant_category_code,
        channel=request.channel,
        entry_mode=request.entry_mode,
        merchant_country=request.merchant_country,
        card_country=request.card_country,
        device_id=request.device_id,
        is_card_present=request.is_card_present,
        three_ds_version=request.three_ds_version,
        three_ds_status=request.three_ds_status,
        authentication_method=request.authentication_method,
    )

    return await use_cases.create(transaction)


@router.get(
    "/transactions",
    status_code=200,
    response_model=list[TransactionResponse],
)
async def get_all_transactions(
    use_cases: TransactionUseCases = Depends(get_transaction_use_cases),
):
    return await use_cases.get_all()


@router.get(
    "/transactions/{id}",
    status_code=200,
    response_model=TransactionResponse,
)
async def get_transaction_by_id(
    id: UUID,
    use_cases: TransactionUseCases = Depends(get_transaction_use_cases),
):
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
