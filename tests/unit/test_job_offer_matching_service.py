from unittest.mock import Mock

import pytest

from app.services.job_matching_service import JobMatchingService
from app.services.job_offer_matching_service import JobOfferMatchingService


def test_match_existing_job_offer():
    job_offer_repository = Mock()
    job_offer = Mock()

    job_offer.skills = [
        Mock(normalized_name="python"),
        Mock(normalized_name="docker"),
        Mock(normalized_name="aws"),
    ]

    job_offer_repository.get_by_id.return_value = job_offer

    service = JobOfferMatchingService(
        job_offer_repository=job_offer_repository,
        job_matching_service=JobMatchingService(),
    )

    result = service.match(
        job_offer_id=1,
        candidate_skills=["python", "aws"],
    )

    assert result.matched_skills == ["aws", "python"]
    assert result.missing_skills == ["docker"]
    assert result.score == pytest.approx(66.67, abs=0.01)

    job_offer_repository.get_by_id.assert_called_once_with(1)


def test_match_nonexistent_job_offer():
    job_offer_repository = Mock()
    job_offer_repository.get_by_id.return_value = None

    service = JobOfferMatchingService(
        job_offer_repository=job_offer_repository,
        job_matching_service=JobMatchingService(),
    )

    with pytest.raises(ValueError, match="Job offer 999 not found"):
        service.match(
            job_offer_id=999,
            candidate_skills=["python"],
        )
