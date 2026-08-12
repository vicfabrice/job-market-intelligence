from fastapi import APIRouter

from app.api.v1.companies import router as companies_router
from app.api.v1.job_offers import router as job_offers_router

api_router = APIRouter()

api_router.include_router(companies_router)
api_router.include_router(job_offers_router)
