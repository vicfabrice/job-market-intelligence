from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.company import Company
from app.models.enums import JobOfferStatus, WorkMode
from app.models.job_offer import JobOffer
from app.repositories.company_repository import CompanyRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.schemas.job_offer import JobOfferCreate, JobOfferUpdate
from app.services.job_offer_service import JobOfferService


@pytest.fixture
def job_offer_repository() -> Mock:
    return Mock(spec=JobOfferRepository)


@pytest.fixture
def company_repository() -> Mock:
    return Mock(spec=CompanyRepository)


@pytest.fixture
def job_offer_service(
    job_offer_repository: Mock, company_repository: Mock
) -> JobOfferService:
    return JobOfferService(
        job_offer_repository=job_offer_repository,
        company_repository=company_repository,
    )


@pytest.fixture
def company() -> Company:
    current_time = datetime.now(UTC)
    return Company(
        id=1,
        name="Acme",
        website="https://acme.com",
        sector="Technology",
        country="Argentina",
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def job_offer_data() -> JobOfferCreate:
    return JobOfferCreate(
        title="Software Engineer",
        company_id=1,
        source_url="https://example.com/jobs/software-engineer",
        location="Buenos Aires",
        work_mode=WorkMode.REMOTE,
        salary_min=Decimal(2500000),
        salary_max=Decimal(3000000),
        currency="ARS",
        description="We are looking for a talented software engineer.",
    )


@pytest.fixture
def job_offer() -> JobOffer:
    current_time = datetime.now(UTC)

    return JobOffer(
        id=1,
        title="Software Engineer",
        company_id=1,
        source_url="https://example.com/jobs/software-engineer",
        location="Buenos Aires",
        work_mode=WorkMode.REMOTE,
        status=JobOfferStatus.ACTIVE,
        salary_min=Decimal(2500000),
        salary_max=Decimal(3000000),
        currency="ARS",
        description="We are looking for a talented software engineer.",
        published_at=None,
        created_at=current_time,
        updated_at=current_time,
    )


def test_create_job_offer_success(
    job_offer_service: JobOfferService,
    job_offer_repository: Mock,
    company_repository: Mock,
    company: Company,
    job_offer_data: JobOfferCreate,
    job_offer: JobOffer,
) -> None:
    company_repository.get_by_id.return_value = company
    job_offer_repository.create.return_value = job_offer

    result = job_offer_service.create(job_offer_data)

    assert result == job_offer
    company_repository.get_by_id.assert_called_once_with(job_offer_data.company_id)
    job_offer_repository.create.assert_called_once_with(job_offer_data)


def test_create_job_offer_raises_not_found_if_company_does_not_exist(
    job_offer_service: JobOfferService,
    job_offer_repository: Mock,
    job_offer_data: JobOfferCreate,
    company_repository: Mock,
) -> None:
    company_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        job_offer_service.create(job_offer_data)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Company not found"

    job_offer_repository.create.assert_not_called()


def test_job_offer_by_id_success(
    job_offer_service: JobOfferService, job_offer_repository: Mock, job_offer: JobOffer
) -> None:
    job_offer_repository.get_by_id.return_value = job_offer

    result = job_offer_service.get_by_id(1)

    assert result == job_offer
    job_offer_repository.get_by_id.assert_called_once_with(1)


def test_get_job_offer_by_id_raises_not_found_if_job_offer_does_not_exist(
    job_offer_service: JobOfferService, job_offer_repository: Mock
) -> None:
    job_offer_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        job_offer_service.get_by_id(999)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Job offer not found"


def test_update_job_offer_success(
    job_offer_service: JobOfferService, job_offer_repository: Mock, job_offer: JobOffer
) -> None:
    update_data = JobOfferUpdate(status=JobOfferStatus.CLOSED)

    job_offer_repository.get_by_id.return_value = job_offer
    job_offer_repository.update.return_value = job_offer

    result = job_offer_service.update(job_offer_id=1, job_offer_data=update_data)

    job_offer_repository.get_by_id.assert_called_once_with(1)
    job_offer_repository.update.assert_called_once_with(
        job_offer=job_offer, job_offer_data=update_data
    )

    assert result == job_offer

    job_offer_repository.update.assert_called_once_with(
        job_offer=job_offer, job_offer_data=update_data
    )


def test_update_job_offer_raises_not_found_for_invalid_company(
    job_offer_service: JobOfferService,
    job_offer_repository: Mock,
    company_repository: Mock,
    job_offer: JobOffer,
) -> None:
    update_data = JobOfferUpdate(company_id=999)

    job_offer_repository.get_by_id.return_value = job_offer
    company_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        job_offer_service.update(
            job_offer_id=1,
            job_offer_data=update_data,
        )

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Company not found"

    job_offer_repository.update.assert_not_called()


def test_update_job_offer_raises_error_when_min_salary_exceeds_max(
    job_offer_service: JobOfferService,
    job_offer_repository: Mock,
    job_offer: JobOffer,
) -> None:
    update_data = JobOfferUpdate(salary_min=Decimal(4000000))

    job_offer_repository.get_by_id.return_value = job_offer

    with pytest.raises(HTTPException) as exception_info:
        job_offer_service.update(
            job_offer_id=1,
            job_offer_data=update_data,
        )

    assert exception_info.value.status_code == 422
    assert (
        exception_info.value.detail
        == "Minimum salary cannot be greater than maximum salary"
    )

    job_offer_repository.update.assert_not_called()


def test_update_job_offer_raises_error_when_salary_has_no_currency(
    job_offer_service: JobOfferService,
    job_offer_repository: Mock,
    job_offer: JobOffer,
) -> None:
    update_data = JobOfferUpdate(currency=None)

    job_offer_repository.get_by_id.return_value = job_offer

    with pytest.raises(HTTPException) as exception_info:
        job_offer_service.update(
            job_offer_id=1,
            job_offer_data=update_data,
        )

    assert exception_info.value.status_code == 422
    assert exception_info.value.detail == "Currency is required when salary is provided"

    job_offer_repository.update.assert_not_called()


def test_delete_job_offer_successfully(
    job_offer_service: JobOfferService,
    job_offer_repository: Mock,
    job_offer: JobOffer,
) -> None:
    job_offer_repository.get_by_id.return_value = job_offer

    result = job_offer_service.delete(1)

    assert result is None
    job_offer_repository.delete.assert_called_once_with(job_offer)
