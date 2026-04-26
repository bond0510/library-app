import logging
from app.core.context import trace_id_ctx

class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_ctx.get()
        return True