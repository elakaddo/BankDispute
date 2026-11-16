from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.transactions import router as transactions_router
from app.api.v1.alerts import router as alerts_router
from app.core.config import get_settings
from fastapi.middleware.cors import CORSMiddleware


def create_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="BankDispute est un copilote intelligent qui assiste les analystes monétiques dans l'investigation des incidents de paiement. ",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin.strip()
            for origin in settings.CORS_ORIGINS.split(",")
            if origin.strip()
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
    )
    application.include_router(health_router, prefix=settings.API_V1_PREFIX)
    application.include_router(transactions_router, prefix=settings.API_V1_PREFIX)
    application.include_router(alerts_router, prefix=settings.API_V1_PREFIX)

    return application


app = create_application()
