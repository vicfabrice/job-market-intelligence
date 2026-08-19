from app.core.database import SessionLocal
from app.integrations.greenhouse.client import GreenhouseClient
from app.integrations.greenhouse.mapper import map_greenhouse_job
from app.repositories.company_repository import CompanyRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.services.job_ingestion_service import JobIngestionService

BOARD_TOKEN = "temporaltechnologies"
COMPANY_NAME = "Temporal"


def main() -> None:
    greenhouse_client = GreenhouseClient()

    database_session = SessionLocal()

    try:
        greenhouse_jobs = greenhouse_client.get_jobs(BOARD_TOKEN)

        normalized_jobs = [
            map_greenhouse_job(
                job=job,
                company_name=COMPANY_NAME,
            )
            for job in greenhouse_jobs
        ]

        company_repository = CompanyRepository(database_session)

        job_offer_repository = JobOfferRepository(database_session)

        ingestion_service = JobIngestionService(
            company_repository=company_repository,
            job_offer_repository=job_offer_repository,
        )

        result = ingestion_service.ingest(normalized_jobs)

        print(f"Received: {result.received}")
        print(f"Created: {result.created}")
        print(f"Skipped: {result.skipped}")
        print(f"Companies created: {result.companies_created}")

    finally:
        database_session.close()
        greenhouse_client.close()


if __name__ == "__main__":
    main()
