from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyResponse
from app.services.company_service import CompanyService

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


def get_company_service(
    database_session: Session = Depends(get_db),
) -> CompanyService:
    repository = CompanyRepository(database_session)

    return CompanyService(repository)


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    company_data: CompanyCreate,
    company_service: CompanyService = Depends(get_company_service),
) -> CompanyResponse:
    return company_service.create(company_data)


@router.get(
    "",
    response_model=list[CompanyResponse],
)
def get_companies(
    company_service: CompanyService = Depends(get_company_service),
) -> list[CompanyResponse]:
    return company_service.get_all()


@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
)
def get_company(
    company_id: int,
    company_service: CompanyService = Depends(get_company_service),
) -> CompanyResponse:
    return company_service.get_by_id(company_id)
