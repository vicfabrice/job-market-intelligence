from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from app.models.enums import JobOfferStatus, WorkMode


class JobOfferBase(BaseModel):
    title: str
    company_id: int

    source_url: str | None = None
    location: str | None = None
    work_mode: WorkMode | None = None
    status: JobOfferStatus = JobOfferStatus.SAVED

    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    currency: str | None = None

    description: str | None = None
    published_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        title = value.strip()

        if not title:
            raise ValueError("Title cannot be empty")

        return title

    @field_validator("salary_min", "salary_max")
    @classmethod
    def validate_salary_is_positive(
        cls,
        value: Decimal | None,
    ) -> Decimal | None:
        if value is not None and value < 0:
            raise ValueError("Salary cannot be negative")

        return value

    @field_validator("currency")
    @classmethod
    def normalize_currency(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        currency = value.strip().upper()

        if len(currency) != 3:
            raise ValueError("Currency must contain exactly three characters")

        return currency


# Representa los datos necesarios para crear una oferta de trabajo
class JobOfferCreate(JobOfferBase):
    @model_validator(mode="after")
    def validate_salary_information(self) -> "JobOfferCreate":
        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_min > self.salary_max
        ):
            raise ValueError("Minimum salary cannot be greater than maximum salary")

        has_salary = self.salary_min is not None or self.salary_max is not None

        if has_salary and self.currency is None:
            raise ValueError("Currency is required when salary is provided")

        return self


# Representa una actualización parcial de una oferta de trabajo
class JobOfferUpdate(BaseModel):
    title: str | None = None
    company_id: int | None = None

    source_url: str | None = None
    location: str | None = None
    work_mode: WorkMode | None = None
    status: JobOfferStatus | None = None

    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    currency: str | None = None

    description: str | None = None
    published_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        title = value.strip()

        if not title:
            raise ValueError("Title cannot be empty")

        return title

    @field_validator("salary_min", "salary_max")
    @classmethod
    def validate_salary_is_positive(
        cls,
        value: Decimal | None,
    ) -> Decimal | None:
        if value is not None and value < 0:
            raise ValueError("Salary cannot be negative")

        return value

    @field_validator("currency")
    @classmethod
    def normalize_currency(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        currency = value.strip().upper()

        if len(currency) != 3:
            raise ValueError("Currency must contain exactly three characters")

        return currency


# Representa lo que devuelve la API al consultar una oferta de trabajo
class JobOfferResponse(JobOfferBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
