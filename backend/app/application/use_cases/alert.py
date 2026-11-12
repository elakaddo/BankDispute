from uuid import UUID

from app.domain.entities.alert import Alert, AlertStatus
from app.infrastructure.database.models.alert import AlertModel
from app.infrastructure.repositories.alert_repository import AlertRepository


class AlertUseCases:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    async def create(self, alert: Alert) -> AlertModel | None:
        if not await self.repository.transaction_exists(alert.transaction_id):
            return None

        return await self.repository.save(alert)

    async def get_all(self) -> list[AlertModel]:
        return await self.repository.find_all()

    async def get_by_id(self, alert_id: UUID) -> AlertModel | None:
        return await self.repository.find_by_id(alert_id)

    async def update_status(
        self,
        alert_id: UUID,
        status: AlertStatus,
    ) -> AlertModel | None:
        return await self.repository.update_status(alert_id, status)

    async def delete(self, alert_id: UUID) -> bool:
        return await self.repository.delete_by_id(alert_id)
