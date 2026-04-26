import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import BusinessException
from .error_codes import ErrorCodes

logger = logging.getLogger(__name__)


class ExceptionHandler:

    @staticmethod
    def register(app: FastAPI):

        @app.exception_handler(BusinessException)
        async def business_exception_handler(request: Request, exc: BusinessException):
            trace_id = getattr(request.state, "trace_id", "N/A")

            logger.error(f"[{trace_id}] {exc.code} - {exc.message}")

            return JSONResponse(
                status_code=400,
                content={
                    "code": exc.code,
                    "message": exc.message,
                    "traceId": trace_id
                }
            )

        @app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            trace_id = getattr(request.state, "trace_id", "N/A")

            logger.exception(f"[{trace_id}] Unexpected error")

            return JSONResponse(
                status_code=500,
                content={
                    "code": ErrorCodes.INTERNAL_SERVER_ERROR.code,
                    "message": ErrorCodes.INTERNAL_SERVER_ERROR.message,
                    "traceId": trace_id
                }
            )
        
        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            trace_id = getattr(request.state, "trace_id", "N/A")

            errors = []
            for err in exc.errors():
                field = ".".join([str(loc) for loc in err["loc"] if loc != "body"])
                errors.append({
                    "field": field,
                    "message": err["msg"]
                })

            logger.error(f"[{trace_id}] Validation failed: {errors}")

            return JSONResponse(
                status_code=422,
                content={
                    "code": ErrorCodes.VALIDATION_ERROR.code,
                    "message": ErrorCodes.VALIDATION_ERROR.message,
                    "traceId": trace_id,
                    "errors": errors
                }
            )