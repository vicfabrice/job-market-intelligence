from datetime import UTC, datetime
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.applications import get_application_service
from app.main import app
from app.models.application import Application
from app.models.enums import ApplicationStatus
from app.services.application_service import ApplicationService


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


@pytest.fixture
def application_service() -> Mock:
    return Mock(spec=ApplicationService)


@pytest.fixture
def client(
    application_service: Mock,
) -> TestClient:
    def override_application_service() -> Mock:
        return application_service

    app.dependency_overrides[get_application_service] = override_application_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_application_returns_created_application(
    client: TestClient,
    application_service: Mock,
    application: Application,
) -> None:
    application_service.create.return_value = application

    response = client.post(
        "/api/v1/applications",
        json={
            "job_offer_id": 1,
            "applied_at": "2026-08-15T12:00:00Z",
            "notes": "Applied through company website",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["id"] == 1
    assert body["job_offer_id"] == 1
    assert body["status"] == "applied"

    application_service.create.assert_called_once()


def test_get_applications_returns_list(
    client: TestClient,
    application_service: Mock,
    application: Application,
) -> None:
    application_service.get_all.return_value = [application]

    response = client.get("/api/v1/applications")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["id"] == 1
    assert body[0]["status"] == "applied"

    application_service.get_all.assert_called_once_with()


def test_get_application_returns_requested_application(
    client: TestClient,
    application_service: Mock,
    application: Application,
) -> None:
    application_service.get_by_id.return_value = application

    response = client.get("/api/v1/applications/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1

    application_service.get_by_id.assert_called_once_with(1)


def test_update_application_returns_updated_application(
    client: TestClient,
    application_service: Mock,
    application: Application,
) -> None:
    application.status = ApplicationStatus.INTERVIEW
    application_service.update.return_value = application

    response = client.patch(
        "/api/v1/applications/1",
        json={
            "status": "interview",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "interview"

    application_service.update.assert_called_once()


def test_update_application_returns_422_for_invalid_status(
    client: TestClient,
    application_service: Mock,
) -> None:
    response = client.patch(
        "/api/v1/applications/1",
        json={
            "status": "banana",
        },
    )

    assert response.status_code == 422
    application_service.update.assert_not_called()


def test_delete_application_returns_no_content(
    client: TestClient,
    application_service: Mock,
) -> None:
    application_service.delete.return_value = None

    response = client.delete("/api/v1/applications/1")

    assert response.status_code == 204
    assert response.content == b""

    application_service.delete.assert_called_once_with(1)
