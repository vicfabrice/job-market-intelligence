from unittest.mock import Mock

import pytest

from app.repositories.company_repository import CompanyRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.schemas.normalized_job_offer import NormalizedJobOffer
from app.services.job_ingestion_service import JobIngestionService


@pytest.fixture
def company_repository() -> Mock:
    return Mock(spec=CompanyRepository)


@pytest.fixture
def job_offer_repository() -> Mock:
    return Mock(spec=JobOfferRepository)


@pytest.fixture
def ingestion_service(
    company_repository: Mock,
    job_offer_repository: Mock,
) -> JobIngestionService:
    return JobIngestionService(
        company_repository=company_repository,
        job_offer_repository=job_offer_repository,
    )


@pytest.fixture
def normalized_job() -> NormalizedJobOffer:
    return NormalizedJobOffer(
        external_id="123",
        source="greenhouse",
        company_name="Temporal",
        sector="Technology",
        title="Backend Engineer",
        source_url="https://example.com/job",
        location="Remote",
    )


@pytest.fixture
def normalized_job_new_company() -> NormalizedJobOffer:
    return NormalizedJobOffer(
        external_id="1234",
        source="greenhouse",
        company_name="New Company",
        sector="Technology",
        title="Backend Engineer",
        source_url="https://example.com/job",
        location="Remote",
    )


def test_ingest_skips_existing_job_offer(
    ingestion_service: JobIngestionService,
    company_repository: Mock,
    job_offer_repository: Mock,
    normalized_job: NormalizedJobOffer,
) -> None:
    job_offer_repository.get_by_source_and_external_id.return_value = Mock()

    result = ingestion_service.ingest([normalized_job])

    assert result.received == 1
    assert result.created == 0
    assert result.skipped == 1
    assert result.companies_created == 0

    company_repository.create.assert_not_called()
    job_offer_repository.create.assert_not_called()


def test_ingest_company_does_not_exist_creates_company(
    ingestion_service: JobIngestionService,
    company_repository: Mock,
    job_offer_repository: Mock,
    normalized_job_new_company: NormalizedJobOffer,
) -> None:
    job_offer_repository.get_by_source_and_external_id.return_value = None
    company_repository.get_by_name.return_value = None
    company_repository.create.return_value = Mock(id=2)

    result = ingestion_service.ingest([normalized_job_new_company])

    assert result.received == 1
    assert result.created == 1
    assert result.skipped == 0
    assert result.companies_created == 1

    company_repository.create.assert_called_once()
    job_offer_repository.create.assert_called_once()


def test_ingest_existing_job_updates_missing_company_sector(
    ingestion_service: JobIngestionService,
    company_repository: Mock,
    job_offer_repository: Mock,
    normalized_job: NormalizedJobOffer,
) -> None:
    existing_company = Mock(
        id=1,
        sector=None,
    )

    existing_job_offer = Mock()

    company_repository.get_by_name.return_value = existing_company
    company_repository.update_sector.return_value = existing_company

    job_offer_repository.get_by_source_and_external_id.return_value = existing_job_offer

    result = ingestion_service.ingest([normalized_job])

    assert result.received == 1
    assert result.created == 0
    assert result.skipped == 1
    assert result.companies_created == 0

    company_repository.get_by_name.assert_called_once_with(normalized_job.company_name)

    company_repository.update_sector.assert_called_once_with(
        company=existing_company,
        sector=normalized_job.sector,
    )

    job_offer_repository.get_by_source_and_external_id.assert_called_once_with(
        source=normalized_job.source,
        external_id=normalized_job.external_id,
    )

    job_offer_repository.create.assert_not_called()
    company_repository.create.assert_not_called()
