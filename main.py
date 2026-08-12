from fastapi import FastAPI
import app.models
from app.infra.database import engine
from app.core.exception_handlers import database_exception_handler
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.norms_router import router

app = FastAPI()

app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler
)

app.include_router(
    router,
    prefix="/api/v1",
)
