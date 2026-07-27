from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)
app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


@app.get("/health/database")
def database_health_check(
    database_session: Session = Depends(get_db),
) -> dict[str, str]:
    database_session.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }
