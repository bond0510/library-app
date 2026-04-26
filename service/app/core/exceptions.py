from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.error_codes import ErrorCode
import logging

logger = logging.getLogger(__name__)


class BusinessException(Exception):

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
    
    def __init__(self, error: ErrorCode, message: str = None):
        self.code = error.code
        self.message = message or error.message