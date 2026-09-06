from unittest.mock import Mock

from app.models.job_offer import JobOffer
from app.models.skill import Skill
from app.services.job_offer_skill_service import JobOfferSkillService


def test_does_nothing_when_job_offer_has_no_description() -> None:
    database_session = Mock()
    skill_repository = Mock()
    skill_extractor = Mock()

    service = JobOfferSkillService(
        skill_repository=skill_repository,
        skill_extractor=skill_extractor,
    )

    job_offer = JobOffer(
        title="Backend Engineer",
        description=None,
    )

    service.extract_and_assign(job_offer)

    skill_extractor.extract.assert_not_called()
    skill_repository.get_by_normalized_name.assert_not_called()
    database_session.commit.assert_not_called()


def test_assigns_existing_skill_to_job_offer() -> None:
    database_session = Mock()
    skill_repository = Mock()
    skill_extractor = Mock()

    service = JobOfferSkillService(
        skill_repository=skill_repository,
        skill_extractor=skill_extractor,
    )

    job_offer = JobOffer(
        title="Backend Engineer",
        description="Python experience required",
    )
    job_offer.skills = []

    python_skill = Skill(
        name="Python",
        normalized_name="python",
    )

    skill_extractor.extract.return_value = ["python"]
    skill_repository.get_by_normalized_name.return_value = python_skill

    service.extract_and_assign(job_offer)

    assert python_skill in job_offer.skills

    skill_repository.get_by_normalized_name.assert_called_once_with("python")
    skill_repository.create.assert_not_called()


def test_creates_and_assigns_missing_skill() -> None:
    database_session = Mock()
    skill_repository = Mock()
    skill_extractor = Mock()

    service = JobOfferSkillService(
        skill_repository=skill_repository,
        skill_extractor=skill_extractor,
    )

    job_offer = JobOffer(
        title="Backend Engineer",
        description="Python experience required",
    )
    job_offer.skills = []

    python_skill = Skill(
        name="python",
        normalized_name="python",
    )

    skill_extractor.extract.return_value = ["python"]
    skill_repository.get_by_normalized_name.return_value = None
    skill_repository.create.return_value = python_skill

    service.extract_and_assign(job_offer)

    skill_repository.create.assert_called_once_with(
        name="python",
        normalized_name="python",
    )

    assert python_skill in job_offer.skills
