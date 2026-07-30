from fastapi import FastAPI

from app.middleware.exception_handler import GlobalExceptionMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_timing import RequestTimingMiddleware


def register_middlewares(app: FastAPI) -> None:
    app.add_middleware(GlobalExceptionMiddleware)
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(RequestIDMiddleware)
