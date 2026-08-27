from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.job_offers import get_job_offer_service
from app.main import app
from app.models.enums import JobOfferStatus, WorkMode
from app.models.job_offer import JobOffer
from app.schemas.job_offer_filters import JobOfferFilters
from app.services.job_offer_service import JobOfferService


@pytest.fixture
def job_offer() -> JobOffer:
    current_time = datetime.now(UTC)

    return JobOffer(
        id=1,
        title="Python Backend Developer",
        company_id=1,
        source_url="https://acme.com/jobs/python-backend",
        location="Buenos Aires",
        work_mode=WorkMode.REMOTE,
        status=JobOfferStatus.ACTIVE,
        salary_min=Decimal(2500000),
        salary_max=Decimal(3500000),
        currency="ARS",
        description="Backend role using FastAPI",
        published_at=None,
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def job_offer_service() -> Mock:
    return Mock(spec=JobOfferService)


@pytest.fixture
def client(
    job_offer_service: Mock,
) -> TestClient:
    def override_job_offer_service() -> Mock:
        return job_offer_service

    app.dependency_overrides[get_job_offer_service] = override_job_offer_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_job_offer_returns_created_offer(
    client: TestClient,
    job_offer_service: Mock,
    job_offer: JobOffer,
) -> None:
    job_offer_service.create.return_value = job_offer

    response = client.post(
        "/api/v1/job-offers",
        json={
            "title": "Python Backend Developer",
            "company_id": 1,
            "source_url": "https://acme.com/jobs/python-backend",
            "location": "Buenos Aires",
            "work_mode": "remote",
            "salary_min": 2500000,
            "salary_max": 3500000,
            "currency": "ARS",
            "description": "Backend role using FastAPI",
        },
    )

    assert response.status_code == 201

    response_body = response.json()

    assert response_body["id"] == 1
    assert response_body["title"] == "Python Backend Developer"
    assert response_body["company_id"] == 1
    assert response_body["work_mode"] == "remote"
    assert response_body["status"] == "active"

    job_offer_service.create.assert_called_once()


def test_create_job_offer_returns_422_when_min_salary_exceeds_max(
    client: TestClient,
    job_offer_service: Mock,
) -> None:
    response = client.post(
        "/api/v1/job-offers",
        json={
            "title": "Backend Developer",
            "company_id": 1,
            "salary_min": 4000000,
            "salary_max": 3000000,
            "currency": "ARS",
        },
    )

    assert response.status_code == 422
    job_offer_service.create.assert_not_called()


def test_create_job_offer_returns_422_when_currency_is_missing(
    client: TestClient,
    job_offer_service: Mock,
) -> None:
    response = client.post(
        "/api/v1/job-offers",
        json={
            "title": "Backend Developer",
            "company_id": 1,
            "salary_min": 3000000,
        },
    )

    assert response.status_code == 422
    job_offer_service.create.assert_not_called()


def test_get_job_offers_returns_list(
    client: TestClient,
    job_offer_service: Mock,
    job_offer: JobOffer,
) -> None:
    job_offer_service.get_all.return_value = [job_offer]

    response = client.get("/api/v1/job-offers")

    assert response.status_code == 200

    response_body = response.json()

    assert len(response_body) == 1
    assert response_body[0]["id"] == 1
    assert response_body[0]["title"] == "Python Backend Developer"

    expected_filters = JobOfferFilters()

    job_offer_service.get_all.assert_called_once_with(expected_filters)


def test_get_job_offer_returns_requested_offer(
    client: TestClient,
    job_offer_service: Mock,
    job_offer: JobOffer,
) -> None:
    job_offer_service.get_by_id.return_value = job_offer

    response = client.get("/api/v1/job-offers/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1

    job_offer_service.get_by_id.assert_called_once_with(1)


def test_update_job_offer_returns_updated_offer(
    client: TestClient,
    job_offer_service: Mock,
    job_offer: JobOffer,
) -> None:
    job_offer.status = JobOfferStatus.CLOSED
    job_offer_service.update.return_value = job_offer

    response = client.patch(
        "/api/v1/job-offers/1",
        json={
            "status": "closed",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "closed"

    job_offer_service.update.assert_called_once()


def test_delete_job_offer_returns_no_content(
    client: TestClient,
    job_offer_service: Mock,
) -> None:
    job_offer_service.delete.return_value = None

    response = client.delete("/api/v1/job-offers/1")

    assert response.status_code == 204
    assert response.content == b""

    job_offer_service.delete.assert_called_once_with(1)


def test_get_job_offers_passes_filters_to_service(
    client: TestClient,
    job_offer_service: Mock,
) -> None:
    job_offer_service.get_all.return_value = []

    response = client.get(
        "/api/v1/job-offers",
        params={
            "title": "engineer",
            "sector": "Technology",
            "source": "greenhouse",
            "limit": 20,
            "offset": 10,
        },
    )

    assert response.status_code == 200

    expected_filters = JobOfferFilters(
        title="engineer",
        sector="Technology",
        source="greenhouse",
        limit=20,
        offset=10,
    )

    job_offer_service.get_all.assert_called_once_with(expected_filters)
