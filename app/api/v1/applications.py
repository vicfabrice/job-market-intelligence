from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


def get_application_service(
    database_session: Session = Depends(get_db),
) -> ApplicationService:
    application_repository = ApplicationRepository(database_session)
    job_offer_repository = JobOfferRepository(database_session)

    return ApplicationService(
        application_repository=application_repository,
        job_offer_repository=job_offer_repository,
    )


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application_data: ApplicationCreate,
    application_service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    return application_service.create(application_data)


@router.get(
    "",
    response_model=list[ApplicationResponse],
)
def get_applications(
    application_service: ApplicationService = Depends(get_application_service),
) -> list[ApplicationResponse]:
    return application_service.get_all()


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application(
    application_id: int,
    application_service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    return application_service.get_by_id(application_id)


@router.patch(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    application_service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    return application_service.update(
        application_id=application_id,
        application_data=application_data,
    )


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_application(
    application_id: int,
    application_service: ApplicationService = Depends(get_application_service),
) -> Response:
    application_service.delete(application_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
