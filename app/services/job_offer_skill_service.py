from app.models.job_offer import JobOffer
from app.repositories.skill_repository import SkillRepository
from app.services.skill_extractor import SkillExtractor


class JobOfferSkillService:
    def __init__(
        self,
        skill_repository: SkillRepository,
        skill_extractor: SkillExtractor,
    ) -> None:
        self.skill_repository = skill_repository
        self.skill_extractor = skill_extractor

    def extract_and_assign(
        self,
        job_offer: JobOffer,
    ) -> None:
        if not job_offer.description:
            return

        normalized_skills = self.skill_extractor.extract(job_offer.description)

        for normalized_name in normalized_skills:
            skill = self.skill_repository.get_by_normalized_name(normalized_name)

            if skill is None:
                skill = self.skill_repository.create(
                    name=normalized_name,
                    normalized_name=normalized_name,
                )

            if skill not in job_offer.skills:
                job_offer.skills.append(skill)
