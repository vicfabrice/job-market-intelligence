from datetime import UTC, datetime
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.companies import get_company_service
from app.main import app
from app.models.company import Company
from app.services.company_service import CompanyService


@pytest.fixture
def company() -> Company:
    current_time = datetime.now(UTC)

    return Company(
        id=1,
        name="Globant",
        website="https://www.globant.com/",
        sector="Software",
        country="Argentina",
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def company_service() -> Mock:
    return Mock(spec=CompanyService)


@pytest.fixture
def client(
    company_service: Mock,
) -> TestClient:
    def override_company_service() -> Mock:
        return company_service

    app.dependency_overrides[get_company_service] = override_company_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_company_returns_created_company(
    client: TestClient,
    company_service: Mock,
    company: Company,
) -> None:
    company_service.create.return_value = company

    response = client.post(
        "/api/v1/companies",
        json={
            "name": "Globant",
            "website": "https://www.globant.com",
            "sector": "Software",
            "country": "Argentina",
        },
    )

    assert response.status_code == 201

    response_body = response.json()

    assert response_body["id"] == 1
    assert response_body["name"] == "Globant"
    assert response_body["sector"] == "Software"
    assert response_body["country"] == "Argentina"

    company_service.create.assert_called_once()


def test_create_company_returns_422_for_invalid_name(
    client: TestClient,
    company_service: Mock,
) -> None:
    response = client.post(
        "/api/v1/companies",
        json={
            "name": "G",
            "website": "https://www.globant.com",
            "sector": "Software",
            "country": "Argentina",
        },
    )

    assert response.status_code == 422
    company_service.create.assert_not_called()


def test_get_companies_returns_company_list(
    client: TestClient,
    company_service: Mock,
    company: Company,
) -> None:
    company_service.get_all.return_value = [company]

    response = client.get("/api/v1/companies")

    assert response.status_code == 200

    response_body = response.json()

    assert len(response_body) == 1
    assert response_body[0]["id"] == 1
    assert response_body[0]["name"] == "Globant"

    company_service.get_all.assert_called_once_with()


def test_get_company_returns_requested_company(
    client: TestClient,
    company_service: Mock,
    company: Company,
) -> None:
    company_service.get_by_id.return_value = company

    response = client.get("/api/v1/companies/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Globant"

    company_service.get_by_id.assert_called_once_with(1)
