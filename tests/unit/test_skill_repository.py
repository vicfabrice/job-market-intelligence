from unittest.mock import Mock

from app.models.skill import Skill
from app.repositories.skill_repository import SkillRepository


def test_get_by_normalized_name_returns_skill() -> None:
    database_session = Mock()
    repository = SkillRepository(database_session)

    expected_skill = Skill(
        name="Python",
        normalized_name="python",
    )

    database_session.scalar.return_value = expected_skill

    result = repository.get_by_normalized_name("python")

    assert result == expected_skill
    database_session.scalar.assert_called_once()


def test_get_by_normalized_name_returns_none_when_not_found() -> None:
    database_session = Mock()
    repository = SkillRepository(database_session)

    database_session.scalar.return_value = None

    result = repository.get_by_normalized_name("python")

    assert result is None


def test_create_skill() -> None:
    database_session = Mock()
    repository = SkillRepository(database_session)

    result = repository.create(
        name="Python",
        normalized_name="python",
    )

    assert result.name == "Python"
    assert result.normalized_name == "python"

    database_session.add.assert_called_once_with(result)
    database_session.flush.assert_called_once()
    database_session.commit.assert_not_called()
    database_session.refresh.assert_not_called()
