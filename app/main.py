from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app import database
from app.routes import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_database_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(health.router)