from unittest.mock import Mock

from app.repositories.job_offer_repository import JobOfferRepository
from app.schemas.job_offer import JobOfferCreate


def test_create_job_offer_flushes_without_committing() -> None:
    database_session = Mock()
    repository = JobOfferRepository(database_session)

    job_offer_data = JobOfferCreate(
        title="Backend Engineer",
        company_id=1,
        source_url="https://example.com/job",
        source="greenhouse",
        external_id="123",
    )

    result = repository.create(job_offer_data)

    assert result.title == "Backend Engineer"
    assert result.company_id == 1
    assert result.source == "greenhouse"
    assert result.external_id == "123"

    database_session.add.assert_called_once_with(result)
    database_session.flush.assert_called_once()

    database_session.commit.assert_not_called()
    database_session.refresh.assert_not_called()
