from fastapi import APIRouter

from backend.core.config import settings

router = APIRouter()


@router.get("/")
async def check_application_health():
    return {"status": "OK", "version": settings.VERSION, "environment": settings.ENVIRONMENT}
