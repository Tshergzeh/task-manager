from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app import database
from app.routes import health, users, auth, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_database_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tasks.router)
