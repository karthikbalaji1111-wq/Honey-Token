from fastapi import FastAPI

from app.api.v1.health import health_payload
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.middleware import register_middlewares

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name, version=settings.app_version)
register_middlewares(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": settings.app_name, "status": "running"}


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return health_payload()
