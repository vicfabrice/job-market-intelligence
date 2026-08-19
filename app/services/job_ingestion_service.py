from app.repositories.company_repository import CompanyRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.schemas.company import CompanyCreate
from app.schemas.job_ingestion import JobIngestionResult
from app.schemas.job_offer import JobOfferCreate
from app.schemas.normalized_job_offer import NormalizedJobOffer


class JobIngestionService:
    def __init__(
        self,
        company_repository: CompanyRepository,
        job_offer_repository: JobOfferRepository,
    ) -> None:
        self.company_repository = company_repository
        self.job_offer_repository = job_offer_repository

    def ingest(
        self,
        jobs: list[NormalizedJobOffer],
    ) -> JobIngestionResult:
        result = JobIngestionResult(received=len(jobs))

        for job in jobs:
            existing_job_offer = (
                self.job_offer_repository.get_by_source_and_external_id(
                    source=job.source,
                    external_id=job.external_id,
                )
            )

            if existing_job_offer is not None:
                result.skipped += 1
                continue

            company = self.company_repository.get_by_name(job.company_name)

            if company is None:
                company = self.company_repository.create(
                    CompanyCreate(
                        name=job.company_name,
                    )
                )

                result.companies_created += 1

            self.job_offer_repository.create(
                JobOfferCreate(
                    title=job.title,
                    company_id=company.id,
                    source=job.source,
                    external_id=job.external_id,
                    source_url=job.source_url,
                    location=job.location,
                    description=job.description,
                    published_at=job.published_at,
                )
            )

            result.created += 1

        return result
