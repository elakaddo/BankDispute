from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.alert import Alert, AlertStatus
from app.infrastructure.database.models.alert import AlertModel
from app.infrastructure.database.models.transaction import TransactionModel


class AlertRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def transaction_exists(self, transaction_id: UUID) -> bool:
        result = await self.session.execute(
            select(TransactionModel.id).where(TransactionModel.id == transaction_id)
        )
        return result.scalar_one_or_none() is not None

    async def save(self, alert: Alert) -> AlertModel:
        model = AlertModel(
            id=alert.id,
            transaction_id=alert.transaction_id,
            alert_type=alert.alert_type.value,
            severity=alert.severity.value,
            status=alert.status.value,
            description=alert.description,
            risk_score=alert.risk_score,
        )

        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return model
        except Exception:
            await self.session.rollback()
            raise

    async def find_all(self) -> list[AlertModel]:
        result = await self.session.execute(
            select(AlertModel).order_by(AlertModel.created_at.desc())
        )
        return list(result.scalars().all())

    async def find_by_id(self, alert_id: UUID) -> AlertModel | None:
        result = await self.session.execute(
            select(AlertModel).where(AlertModel.id == alert_id)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        alert_id: UUID,
        status: AlertStatus,
    ) -> AlertModel | None:
        alert = await self.find_by_id(alert_id)

        if alert is None:
            return None

        try:
            alert.status = status.value
            await self.session.commit()
            await self.session.refresh(alert)
            return alert
        except Exception:
            await self.session.rollback()
            raise

    async def delete_by_id(self, alert_id: UUID) -> bool:
        alert = await self.find_by_id(alert_id)

        if alert is None:
            return False

        try:
            await self.session.delete(alert)
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            raise
