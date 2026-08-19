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
        external_id="5209443007",
        source="greenhouse",
        company_name="Temporal",
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

    company_repository.get_by_name.assert_not_called()
    company_repository.create.assert_not_called()
    job_offer_repository.create.assert_not_called()
