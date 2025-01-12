from uuid import uuid4
from fastapi import FastAPI, Request
from shared.loggable import Loggable
from starlette.middleware.base import BaseHTTPMiddleware

class UuidMiddleware(BaseHTTPMiddleware, Loggable):
    def __init__(self, app: FastAPI):
        BaseHTTPMiddleware.__init__(self, app)
        Loggable.__init__(self, prefix="UuidMiddleware")

    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid4())
        request.state.trace_id = trace_id

        self.info(f"Request {trace_id} received", trace_id)

        response = await call_next(request)

        response.headers["X-Trace-Id"] = trace_id

        return response
