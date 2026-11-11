from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health", status_code=200, summary="Health Check")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify the API is running.
    """
    return {
        "status": "ok",
        "service": "bankdispute-api"
    }