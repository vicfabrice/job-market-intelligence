from app.repositories.job_offer_repository import JobOfferRepository
from app.services.job_matching_service import (
    JobMatchingService,
    JobMatchResult,
)


class JobOfferMatchingService:
    def __init__(
        self,
        job_offer_repository: JobOfferRepository,
        job_matching_service: JobMatchingService,
    ) -> None:
        self.job_offer_repository = job_offer_repository
        self.job_matching_service = job_matching_service

    def match(
        self,
        job_offer_id: int,
        candidate_skills: list[str],
    ) -> JobMatchResult:
        job_offer = self.job_offer_repository.get_by_id(job_offer_id)

        if job_offer is None:
            raise ValueError(f"Job offer {job_offer_id} not found")

        job_offer_skills = [skill.normalized_name for skill in job_offer.skills]

        return self.job_matching_service.match(
            candidate_skills=candidate_skills,
            job_offer_skills=job_offer_skills,
        )
