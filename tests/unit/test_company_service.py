from datetime import UTC, datetime
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate
from app.services.company_service import CompanyService


@pytest.fixture
def company_repository() -> Mock:
    return Mock(spec=CompanyRepository)


@pytest.fixture
def company_service(
    company_repository: Mock,
) -> CompanyService:
    return CompanyService(company_repository)


@pytest.fixture
def company_data() -> CompanyCreate:
    return CompanyCreate(
        name="Globant",
        website="https://www.globant.com",
        sector="Software",
        country="Argentina",
    )


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


def test_create_company_successfully(
    company_service: CompanyService,
    company_repository: Mock,
    company_data: CompanyCreate,
    company: Company,
) -> None:
    company_repository.get_by_name.return_value = None
    company_repository.create.return_value = company

    result = company_service.create(company_data)

    assert result == company

    company_repository.get_by_name.assert_called_once_with(company_data.name)
    company_repository.create.assert_called_once_with(company_data)


def test_create_company_raises_conflict_when_name_exists(
    company_service: CompanyService,
    company_repository: Mock,
    company_data: CompanyCreate,
    company: Company,
) -> None:
    company_repository.get_by_name.return_value = company

    with pytest.raises(HTTPException) as exception_info:
        company_service.create(company_data)

    assert exception_info.value.status_code == 409
    assert exception_info.value.detail == "A company with this name already exists"

    company_repository.get_by_name.assert_called_once_with(company_data.name)
    company_repository.create.assert_not_called()


def test_get_all_companies(
    company_service: CompanyService,
    company_repository: Mock,
    company: Company,
) -> None:
    company_repository.get_all.return_value = [company]

    result = company_service.get_all()

    assert result == [company]
    company_repository.get_all.assert_called_once_with()


def test_get_company_by_id_successfully(
    company_service: CompanyService,
    company_repository: Mock,
    company: Company,
) -> None:
    company_repository.get_by_id.return_value = company

    result = company_service.get_by_id(company.id)

    assert result == company
    company_repository.get_by_id.assert_called_once_with(company.id)


def test_get_company_by_id_raises_not_found(
    company_service: CompanyService,
    company_repository: Mock,
) -> None:
    company_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        company_service.get_by_id(999)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Company not found"

    company_repository.get_by_id.assert_called_once_with(999)
