from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from .api import health_check, v1
from .core.config import settings

app = FastAPI(
    tilte="Grupo Boticário - Backend",
    version=settings.VERSION,
    description="Backend para o processo seletivo do grupo boticário",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=UJSONResponse,
)

app.include_router(v1.endpoints, prefix="/v1")
app.include_router(health_check.router, prefix="/healh-check")
