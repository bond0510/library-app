from contextvars import ContextVar

trace_id_ctx = ContextVar("trace_id", default="N/A")