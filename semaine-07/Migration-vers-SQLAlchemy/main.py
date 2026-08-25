from fastapi import FastAPI

from .routers import tasks

app = FastAPI(
    title="API Tasks",
    version="3.0.0",
)

app.include_router(tasks.router)