import logging

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("stormchain")


def register_error_handlers(application):
    @application.exception_handler(RequestValidationError)
    async def validation_error(request, exception):
        errors = [
            {key: error[key] for key in ("loc", "msg", "type")} for error in exception.errors()
        ]
        return JSONResponse({"detail": errors}, status_code=422)

    @application.exception_handler(SQLAlchemyError)
    async def database_error(request, exception):
        logger.error("Database request failed: %s", type(exception).__name__)
        return JSONResponse({"detail": "Database unavailable"}, status_code=503)
