from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate


class CompanyRepository:
    def __init__(self, database_session: Session) -> None:
        self.database_session = database_session

    def create(self, company_data: CompanyCreate) -> Company:
        company = Company(
            name=company_data.name,
            website=(
                str(company_data.website) if company_data.website is not None else None
            ),
            sector=company_data.sector,
            country=company_data.country,
        )

        self.database_session.add(company)
        self.database_session.commit()
        self.database_session.refresh(company)

        return company

    def get_all(self) -> list[Company]:
        statement = select(Company).order_by(Company.name)

        return list(self.database_session.scalars(statement).all())

    def get_by_id(self, company_id: int) -> Company | None:
        return self.database_session.get(Company, company_id)

    def get_by_name(self, company_name: str) -> Company | None:
        statement = select(Company).where(Company.name == company_name)

        return self.database_session.scalar(statement)
