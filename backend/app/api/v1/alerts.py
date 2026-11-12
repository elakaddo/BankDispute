from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.alert import AlertUseCases
from app.domain.entities.alert import Alert
from app.infrastructure.database.db import get_db
from app.infrastructure.repositories.alert_repository import AlertRepository
from app.schemas.alert import (
    AlertRequest,
    AlertResponse,
    AlertStatusUpdate,
)

router = APIRouter(tags=["Alerts"])


def get_alert_use_cases(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> AlertUseCases:
    repository = AlertRepository(session)
    return AlertUseCases(repository)


@router.post(
    "/alerts",
    status_code=status.HTTP_201_CREATED,
    response_model=AlertResponse,
)
async def create_alert(
    request: AlertRequest,
    use_cases: Annotated[AlertUseCases, Depends(get_alert_use_cases)],
):
    alert = Alert(
        transaction_id=request.transaction_id,
        alert_type=request.alert_type,
        severity=request.severity,
        description=request.description,
        risk_score=request.risk_score,
    )

    result = await use_cases.create(alert)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    return result


@router.get(
    "/alerts",
    response_model=list[AlertResponse],
)
async def get_all_alerts(
    use_cases: Annotated[AlertUseCases, Depends(get_alert_use_cases)],
):
    return await use_cases.get_all()


@router.get(
    "/alerts/{alert_id}",
    response_model=AlertResponse,
)
async def get_alert_by_id(
    alert_id: UUID,
    use_cases: Annotated[AlertUseCases, Depends(get_alert_use_cases)],
):
    alert = await use_cases.get_by_id(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return alert


@router.patch(
    "/alerts/{alert_id}/status",
    response_model=AlertResponse,
)
async def update_alert_status(
    alert_id: UUID,
    request: AlertStatusUpdate,
    use_cases: Annotated[AlertUseCases, Depends(get_alert_use_cases)],
):
    alert = await use_cases.update_status(alert_id, request.status)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return alert


@router.delete(
    "/alerts/{alert_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_alert(
    alert_id: UUID,
    use_cases: Annotated[AlertUseCases, Depends(get_alert_use_cases)],
):
    deleted = await use_cases.delete(alert_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
