import asyncio
import uuid

import structlog
from fastapi import FastAPI, Request
from structlog.contextvars import bind_contextvars, clear_contextvars


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger()

app = FastAPI()


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    clear_contextvars()

    request_id = str(uuid.uuid4())

    bind_contextvars(request_id=request_id)

    logger.info("request_started", path=request.url.path)

    try:
        response = await call_next(request)

        logger.info(
            "request_finished",
            path=request.url.path,
            status_code=response.status_code,
        )

        response.headers["X-Request-ID"] = request_id

        return response

    finally:
        clear_contextvars()


@app.get("/")
async def home():
    logger.info("home_endpoint_called")

    return {"message": "Hello"}


@app.get("/test")
async def test():
    logger.info("test_started")

    await asyncio.sleep(2)

    logger.info("test_finished")

    return {"message": "Test terminé"}