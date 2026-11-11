from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.transactions import router as transactions_router
from app.core.config import get_settings


def create_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="BankDispute est un copilote intelligent qui assiste les analystes monétiques dans l'investigation des incidents de paiement. ",
    )

    application.include_router(health_router, prefix=settings.API_V1_PREFIX)
    application.include_router(transactions_router, prefix=settings.API_V1_PREFIX)

    return application


app = create_application()
