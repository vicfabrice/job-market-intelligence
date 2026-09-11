from app.core.database import SessionLocal
from app.integrations.greenhouse.client import GreenhouseClient
from app.integrations.greenhouse.config import GREENHOUSE_COMPANIES
from app.integrations.greenhouse.mapper import map_greenhouse_job
from app.repositories.company_repository import CompanyRepository
from app.repositories.job_offer_repository import JobOfferRepository
from app.repositories.skill_repository import SkillRepository
from app.services.job_ingestion_service import JobIngestionService
from app.services.job_offer_skill_service import JobOfferSkillService
from app.services.skill_extractor import SkillExtractor
from app.services.skill_normalizer import SkillNormalizer


def main() -> None:
    greenhouse_client = GreenhouseClient()
    database_session = SessionLocal()

    try:
        company_repository = CompanyRepository(database_session)
        job_offer_repository = JobOfferRepository(database_session)
        skill_repository = SkillRepository(database_session)

        skill_normalizer = SkillNormalizer()
        skill_extractor = SkillExtractor(skill_normalizer)

        job_offer_skill_service = JobOfferSkillService(
            skill_repository=skill_repository,
            skill_extractor=skill_extractor,
        )
        ingestion_service = JobIngestionService(
            company_repository=company_repository,
            job_offer_repository=job_offer_repository,
            database_session=database_session,
            job_offer_skill_service=job_offer_skill_service,
        )

        for company_config in GREENHOUSE_COMPANIES:
            print(f"\nImporting {company_config.name} ({company_config.board_token})")

            greenhouse_jobs = greenhouse_client.get_jobs(company_config.board_token)

            normalized_jobs = [
                map_greenhouse_job(
                    job=job,
                    company_name=company_config.name,
                    sector=company_config.sector,
                )
                for job in greenhouse_jobs
            ]

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
