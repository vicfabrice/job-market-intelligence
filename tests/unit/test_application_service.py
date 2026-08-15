from datetime import UTC, datetime
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.application import Application
from app.models.enums import ApplicationStatus
from app.models.job_offer import JobOffer
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
)
from app.services.application_service import ApplicationService


@pytest.fixture
def application_repository() -> Mock:
    return Mock(spec=ApplicationRepository)


@pytest.fixture
def job_offer_repository() -> Mock:
    return Mock(spec=JobOfferRepository)


@pytest.fixture
def application_service(
    application_repository: Mock,
    job_offer_repository: Mock,
) -> ApplicationService:
    return ApplicationService(
        application_repository=application_repository,
        job_offer_repository=job_offer_repository,
    )


@pytest.fixture
def job_offer() -> JobOffer:
    current_time = datetime.now(UTC)

    return JobOffer(
        id=1,
        title="Python Backend Developer",
        company_id=1,
        status="active",
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def application_data() -> ApplicationCreate:
    return ApplicationCreate(
        job_offer_id=1,
        applied_at=datetime.now(UTC),
        notes="Applied through company website",
    )


@pytest.fixture
def application() -> Application:
    current_time = datetime.now(UTC)

    return Application(
        id=1,
        job_offer_id=1,
        status=ApplicationStatus.APPLIED,
        applied_at=current_time,
        notes="Applied through company website",
        created_at=current_time,
        updated_at=current_time,
    )


def test_create_application_successfully(
    application_service: ApplicationService,
    application_repository: Mock,
    job_offer_repository: Mock,
    application_data: ApplicationCreate,
    application: Application,
    job_offer: JobOffer,
) -> None:
    job_offer_repository.get_by_id.return_value = job_offer
    application_repository.get_by_job_offer_id.return_value = None
    application_repository.create.return_value = application

    result = application_service.create(application_data)

    assert result == application

    job_offer_repository.get_by_id.assert_called_once_with(
        application_data.job_offer_id
    )
    application_repository.get_by_job_offer_id.assert_called_once_with(
        application_data.job_offer_id
    )
    application_repository.create.assert_called_once_with(application_data)


def test_create_application_raises_not_found_when_job_offer_does_not_exist(
    application_service: ApplicationService,
    application_repository: Mock,
    job_offer_repository: Mock,
    application_data: ApplicationCreate,
) -> None:
    job_offer_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        application_service.create(application_data)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Job offer not found"

    application_repository.create.assert_not_called()


def test_create_application_raises_conflict_when_application_exists(
    application_service: ApplicationService,
    application_repository: Mock,
    job_offer_repository: Mock,
    application_data: ApplicationCreate,
    application: Application,
    job_offer: JobOffer,
) -> None:
    job_offer_repository.get_by_id.return_value = job_offer
    application_repository.get_by_job_offer_id.return_value = application

    with pytest.raises(HTTPException) as exception_info:
        application_service.create(application_data)

    assert exception_info.value.status_code == 409
    assert (
        exception_info.value.detail
        == "An application for this job offer already exists"
    )

    application_repository.create.assert_not_called()


def test_get_application_by_id_successfully(
    application_service: ApplicationService,
    application_repository: Mock,
    application: Application,
) -> None:
    application_repository.get_by_id.return_value = application

    result = application_service.get_by_id(1)

    assert result == application
    application_repository.get_by_id.assert_called_once_with(1)


def test_get_application_by_id_raises_not_found(
    application_service: ApplicationService,
    application_repository: Mock,
) -> None:
    application_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        application_service.get_by_id(999)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Application not found"


def test_update_application_successfully(
    application_service: ApplicationService,
    application_repository: Mock,
    application: Application,
) -> None:
    update_data = ApplicationUpdate(status=ApplicationStatus.INTERVIEW)

    application_repository.get_by_id.return_value = application
    application_repository.update.return_value = application

    result = application_service.update(
        application_id=1,
        application_data=update_data,
    )

    assert result == application

    application_repository.update.assert_called_once_with(
        application=application,
        application_data=update_data,
    )


def test_delete_application_successfully(
    application_service: ApplicationService,
    application_repository: Mock,
    application: Application,
) -> None:
    application_repository.get_by_id.return_value = application

    result = application_service.delete(1)

    assert result is None
    application_repository.delete.assert_called_once_with(application)
