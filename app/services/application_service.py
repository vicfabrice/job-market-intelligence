from fastapi import HTTPException, status

from app.models.application import Application
from app.repositories.application_repository import (
    ApplicationRepository,
)
from app.repositories.job_offer_repository import (
    JobOfferRepository,
)
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
)


class ApplicationService:
    def __init__(
        self,
        application_repository: ApplicationRepository,
        job_offer_repository: JobOfferRepository,
    ) -> None:
        self.application_repository = application_repository
        self.job_offer_repository = job_offer_repository

    def create(
        self,
        application_data: ApplicationCreate,
    ) -> Application:
        job_offer = self.job_offer_repository.get_by_id(application_data.job_offer_id)

        if job_offer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job offer not found",
            )

        existing_application = self.application_repository.get_by_job_offer_id(
            application_data.job_offer_id
        )

        if existing_application is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=("An application for this job offer already exists"),
            )

        return self.application_repository.create(application_data)

    def get_all(self) -> list[Application]:
        return self.application_repository.get_all()

    def get_by_id(
        self,
        application_id: int,
    ) -> Application:
        application = self.application_repository.get_by_id(application_id)

        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        return application

    def update(
        self,
        application_id: int,
        application_data: ApplicationUpdate,
    ) -> Application:
        application = self.get_by_id(application_id)

        return self.application_repository.update(
            application=application,
            application_data=application_data,
        )

    def delete(
        self,
        application_id: int,
    ) -> None:
        application = self.get_by_id(application_id)

        self.application_repository.delete(application)
