from fastapi import HTTPException, status

from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate


class CompanyService:
    def __init__(
        self,
        company_repository: CompanyRepository,
    ) -> None:
        self.company_repository = company_repository

    def create(self, company_data: CompanyCreate) -> Company:
        existing_company = self.company_repository.get_by_name(company_data.name)

        if existing_company is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A company with this name already exists",
            )

        return self.company_repository.create(company_data)

    def get_all(self) -> list[Company]:
        return self.company_repository.get_all()

    def get_by_id(self, company_id: int) -> Company:
        company = self.company_repository.get_by_id(company_id)

        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )

        return company
