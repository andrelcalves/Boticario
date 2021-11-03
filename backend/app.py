from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import UJSONResponse

from backend.core import controller
from backend.core.models import CreateSeller

from .api import auth, health_check, v1
from .core.config import settings
from .core.helpers.database import session_context
from .core.helpers.exceptions import DatabaseError, NotAuthorizedError, NotFoundError, ServiceError
from .core.helpers.logger import logger

app = FastAPI(
    tilte="Grupo Boticário - Backend",
    version=settings.VERSION,
    description="Backend para o processo seletivo do grupo boticário",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=UJSONResponse,
)

app.include_router(v1.endpoints, prefix="/v1", tags=["v1"])
app.include_router(auth.router, prefix="/auth", tags=["Authorization"])
app.include_router(health_check.router, prefix="/health-check")


@app.exception_handler(RequestValidationError)
async def unprocessable_entity_error(request: Request, exc: RequestValidationError):
    return UJSONResponse(content={"message": exc.errors()}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return UJSONResponse(content={"message": exc.detail}, status_code=exc.status_code)


@app.exception_handler(DatabaseError)
async def database_error(request: Request, exc: DatabaseError):
    return UJSONResponse(content={"message": exc.detail}, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(NotFoundError)
async def not_found_error(request: Request, exc: NotFoundError):
    return UJSONResponse(content={"message": exc.detail}, status_code=status.HTTP_204_NO_CONTENT)


@app.exception_handler(NotAuthorizedError)
async def not_authorized_error(request: Request, exc: NotAuthorizedError):
    return UJSONResponse(
        content={"message": exc.detail},
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(Exception)
async def unknown_error(request: Request, exc: Exception):
    return UJSONResponse(content={"message": str(exc)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.exception_handler(Exception)
async def service_error(request: Request, exc: ServiceError):
    return UJSONResponse(
        content={"message": f"Error on service {exc.service}, {exc.detail}"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.on_event("startup")
async def start_application():
    try:
        with session_context() as session:
            try:
                logger.info("Searching for first seller..")
                controller.seller.get_by_cpf(session, settings.FIRST_SELLER_CPF)

            except NotFoundError:
                logger.info("Couldn't be found the first seller, starting creation")
                controller.seller.create(
                    session,
                    CreateSeller(
                        cpf=settings.FIRST_SELLER_CPF,
                        name=settings.FIRST_SELLER_NAME,
                        email=settings.FIRST_SELLER_EMAIL,
                        password=settings.FIRST_SELLER_PASSWORD,
                        confirm_password=settings.FIRST_SELLER_PASSWORD,
                    ),
                )

    except Exception as err:  # In some cases the creation fails because the workers tried to create at the same time
        logger.error(f"Couldn't create the Fist Seller: {err}")

    else:
        logger.info("Firt seller created with success!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:app",
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
        log_level=settings.LOG_LEVEL,
        access_log=True,
        workers=settings.WORKERS,
        timeout_keep_alive=50,
    )
