import logging
import uuid

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from structlog.contextvars import bind_contextvars, clear_contextvars

from exceptions import BusinessError, ConflictError, NotFoundError, ValidationError


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger()

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    clear_contextvars()

    request_id = str(uuid.uuid4())

    bind_contextvars(request_id=request_id)

    try:
        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        return response

    finally:
        clear_contextvars()


@app.exception_handler(BusinessError)
async def business_error_handler(
    request: Request,
    exc: BusinessError,
) -> JSONResponse:
    logger.warning(
        "business_error",
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details,
        path=request.url.path,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        },
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "unexpected_error",
        path=request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Une erreur interne est survenue.",
            "details": None,
        },
    )


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id == 404:
        raise NotFoundError(
            message="Utilisateur introuvable",
            details={"user_id": user_id},
        )

    if user_id == 409:
        raise ConflictError(
            message="Cet utilisateur existe déjà",
            details={"user_id": user_id},
        )

    if user_id == 422:
        raise ValidationError(
            message="Données utilisateur invalides",
            details={"field": "user_id"},
        )

    if user_id == 500:
        raise RuntimeError("Erreur technique secrète")

    return {
        "id": user_id,
        "name": "Issa",
    }