from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager

from app import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_database_tables()
    yield

app = FastAPI(lifespan=lifespan)