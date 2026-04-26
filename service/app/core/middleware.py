import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.context import trace_id_ctx

class TraceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id
        trace_id_ctx.set(trace_id)

        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response