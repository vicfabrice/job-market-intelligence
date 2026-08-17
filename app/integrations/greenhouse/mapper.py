from app.integrations.greenhouse.schemas import GreenhouseJob
from app.schemas.normalized_job_offer import NormalizedJobOffer


def map_greenhouse_job(
    job: GreenhouseJob,
    company_name: str,
) -> NormalizedJobOffer:
    return NormalizedJobOffer(
        external_id=str(job.id),
        source="greenhouse",
        company_name=company_name,
        title=job.title,
        source_url=job.absolute_url,
        location=job.location.name,
        published_at=job.updated_at,
    )
