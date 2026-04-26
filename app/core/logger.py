import logging
from logging.handlers import RotatingFileHandler
from app.core.logging_filter import TraceIdFilter
import os

LOG_DIR = "logs"
LOG_FILE = "app.log"

def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid duplicate logs (important in FastAPI reload)
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
         "%(asctime)s | %(levelname)s | %(trace_id)s | %(name)s | %(message)s"
    )

    # ✅ Console Appender
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(TraceIdFilter())
    # ✅ File Appender (with rotation)
    file_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(TraceIdFilter())

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)