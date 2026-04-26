# app/main.py

import logging

from fastapi import FastAPI

from app.controllers import borrow_controller
from app.controllers import book_controller
from app.controllers import member_controller
from app.core.logger import setup_logging
from app.core.middleware import TraceIdMiddleware
from app.core.exception_handlers import ExceptionHandler
from fastapi.middleware.cors import CORSMiddleware

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="Library API",root_path="/api/v1",
              description="APIs for managing books, members, and borrows",
                version="1.0.0")

# Middleware
app.add_middleware(TraceIdMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register global exception handlers
ExceptionHandler.register(app)


app.include_router(borrow_controller.router)
app.include_router(book_controller.router)
app.include_router(member_controller.router)