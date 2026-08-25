from fastapi import FastAPI

from routers import orders, tasks

app = FastAPI(
    title="API Tasks",
    version="4.0.0",
)

app.include_router(tasks.router)
app.include_router(orders.router)