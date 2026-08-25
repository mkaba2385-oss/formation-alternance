from fastapi import FastAPI

from .db import Base, engine
from .routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Tasks",
    version="2.0.0",
)

app.include_router(tasks.router)