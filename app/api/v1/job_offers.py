from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enums import JobOfferStatus, WorkMode
from app.repositories.company_repository import CompanyRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.schemas.job_offer import (
    JobOfferCreate,
    JobOfferResponse,
    JobOfferUpdate,
)
from app.schemas.job_offer_filters import JobOfferFilters
from app.services.job_offer_service import JobOfferService

router = APIRouter(
    prefix="/job-offers",
    tags=["Job Offers"],
)


def get_job_offer_service(
    database_session: Session = Depends(get_db),
) -> JobOfferService:
    job_offer_repository = JobOfferRepository(database_session)
    company_repository = CompanyRepository(database_session)

    return JobOfferService(
        job_offer_repository=job_offer_repository,
        company_repository=company_repository,
    )


@router.post(
    "",
    response_model=JobOfferResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job_offer(
    job_offer_data: JobOfferCreate,
    job_offer_service: JobOfferService = Depends(get_job_offer_service),
) -> JobOfferResponse:
    return job_offer_service.create(job_offer_data)


@router.get(
    "",
    response_model=list[JobOfferResponse],
)
def get_job_offers(
    title: str | None = None,
    sector: str | None = None,
    location: str | None = None,
    work_mode: WorkMode | None = None,
    status: JobOfferStatus | None = None,
    source: str | None = None,
    company_id: int | None = None,
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    job_offer_service: JobOfferService = Depends(get_job_offer_service),
) -> list[JobOfferResponse]:
    filters = JobOfferFilters(
        title=title,
        sector=sector,
        location=location,
        work_mode=work_mode,
        status=status,
        source=source,
        company_id=company_id,
        limit=limit,
        offset=offset,
    )

    return job_offer_service.get_all(filters)


@router.get(
    "/{job_offer_id}",
    response_model=JobOfferResponse,
)
def get_job_offer(
    job_offer_id: int,
    job_offer_service: JobOfferService = Depends(get_job_offer_service),
) -> JobOfferResponse:
    return job_offer_service.get_by_id(job_offer_id)


@router.patch(
    "/{job_offer_id}",
    response_model=JobOfferResponse,
)
def update_job_offer(
    job_offer_id: int,
    job_offer_data: JobOfferUpdate,
    job_offer_service: JobOfferService = Depends(get_job_offer_service),
) -> JobOfferResponse:
    return job_offer_service.update(
        job_offer_id=job_offer_id,
        job_offer_data=job_offer_data,
    )


@router.delete(
    "/{job_offer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job_offer(
    job_offer_id: int,
    job_offer_service: JobOfferService = Depends(get_job_offer_service),
) -> Response:
    job_offer_service.delete(job_offer_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
