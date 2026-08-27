from decimal import Decimal

from fastapi import HTTPException, status

from app.models.job_offer import JobOffer
from app.repositories.company_repository import CompanyRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.schemas.job_offer import JobOfferCreate, JobOfferUpdate
from app.schemas.job_offer_filters import JobOfferFilters


class JobOfferService:
    def __init__(
        self,
        job_offer_repository: JobOfferRepository,
        company_repository: CompanyRepository,
    ):
        self.job_offer_repository = job_offer_repository
        self.company_repository = company_repository

    def create(
        self,
        job_offer_data: JobOfferCreate,
    ) -> JobOffer:
        self._validate_company_exists(job_offer_data.company_id)

        return self.job_offer_repository.create(job_offer_data)

    def get_all(
        self,
        filters: JobOfferFilters,
    ) -> list[JobOffer]:
        return self.job_offer_repository.get_all(filters)

    def get_by_id(
        self,
        job_offer_id: int,
    ) -> JobOffer:
        job_offer = self.job_offer_repository.get_by_id(job_offer_id)

        if job_offer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job offer not found",
            )

        return job_offer

    def update(
        self,
        job_offer_id: int,
        job_offer_data: JobOfferUpdate,
    ) -> JobOffer:
        job_offer = self.get_by_id(job_offer_id)

        if "company_id" in job_offer_data.model_fields_set:
            if job_offer_data.company_id is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Company ID cannot be null",
                )

            self._validate_company_exists(job_offer_data.company_id)

        salary_min = self._get_updated_value(
            field_name="salary_min",
            update_data=job_offer_data,
            current_value=job_offer.salary_min,
        )

        salary_max = self._get_updated_value(
            field_name="salary_max",
            update_data=job_offer_data,
            current_value=job_offer.salary_max,
        )

        currency = self._get_updated_value(
            field_name="currency",
            update_data=job_offer_data,
            current_value=job_offer.currency,
        )

        self._validate_salary_information(
            salary_min=salary_min,
            salary_max=salary_max,
            currency=currency,
        )

        return self.job_offer_repository.update(
            job_offer=job_offer,
            job_offer_data=job_offer_data,
        )

    def delete(
        self,
        job_offer_id: int,
    ) -> None:
        job_offer = self.get_by_id(job_offer_id)

        self.job_offer_repository.delete(job_offer)

    def _validate_company_exists(
        self,
        company_id: int,
    ) -> None:
        company = self.company_repository.get_by_id(company_id)

        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )

    @staticmethod
    def _get_updated_value(
        field_name: str,
        update_data: JobOfferUpdate,
        current_value: object,
    ) -> object:
        if field_name in update_data.model_fields_set:
            return getattr(update_data, field_name)

        return current_value

    @staticmethod
    def _validate_salary_information(
        salary_min: Decimal | None,
        salary_max: Decimal | None,
        currency: str | None,
    ) -> None:
        if (
            salary_min is not None
            and salary_max is not None
            and salary_min > salary_max
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=("Minimum salary cannot be greater than maximum salary"),
            )

        has_salary = salary_min is not None or salary_max is not None

        if has_salary and currency is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=("Currency is required when salary is provided"),
            )
