from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.job_matching_service import JobMatchResult

client = TestClient(app)


def test_match_job_offer_returns_result():
    expected_result = JobMatchResult(
        matched_skills=["aws", "python"],
        missing_skills=["kubernetes", "postgresql"],
        score=50.0,
    )

    with patch("app.api.v1.job_offers.JobOfferMatchingService") as mock_service_class:
        mock_service = mock_service_class.return_value
        mock_service.match.return_value = expected_result

        response = client.post(
            "/api/v1/job-offers/123/match",
            json={
                "candidate_skills": ["python", "aws"],
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "matched_skills": ["aws", "python"],
        "missing_skills": ["kubernetes", "postgresql"],
        "score": 50.0,
    }

    mock_service.match.assert_called_once_with(
        job_offer_id=123,
        candidate_skills=["python", "aws"],
    )


def test_match_job_offer_not_found():
    with patch("app.api.v1.job_offers.JobOfferMatchingService") as mock_service_class:
        mock_service = mock_service_class.return_value
        mock_service.match.side_effect = ValueError("Job offer 999 not found")

        response = client.post(
            "/api/v1/job-offers/999/match",
            json={
                "candidate_skills": ["python"],
            },
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job offer 999 not found",
    }


def test_match_job_offer_rejects_empty_skills():
    response = client.post(
        "/api/v1/job-offers/123/match",
        json={
            "candidate_skills": [],
        },
    )

    assert response.status_code == 422
