from fastapi import FastAPI
import app.models
from app.infra.database import engine
from app.core.exception_handlers import database_exception_handler
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.norm_router import router as norm_router
from app.api.routes.user_router import router as user_router
from app.api.routes.auth_router import router as auth_router
from app.api.routes.dashboard_router import router as dashboard_router

app = FastAPI()

app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler
)

app.include_router(
    norm_router,
    prefix="/api/v1",
)

app.include_router(
    user_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    dashboard_router,
    prefix="/api/v1",
)
