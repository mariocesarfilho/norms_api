import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

def database_exception_handler(
    request: Request, exc: SQLAlchemyError
):
    logger.error("Database error: %s",
        exc,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erro interno ao acessar o banco de dados.",
            "data": None,
        }
    )