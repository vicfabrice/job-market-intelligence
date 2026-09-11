from app.services.skill_normalizer import SkillNormalizer


def test_normalize_known_skill() -> None:
    normalizer = SkillNormalizer()

    result = normalizer.normalize("Python")

    assert result == "python"


def test_normalize_alias() -> None:
    normalizer = SkillNormalizer()

    result = normalizer.normalize("Postgres")

    assert result == "postgresql"


def test_normalize_is_case_insensitive() -> None:
    normalizer = SkillNormalizer()

    result = normalizer.normalize("SPRING BOOT")

    assert result == "spring_boot"


def test_normalize_unknown_skill_returns_none() -> None:
    normalizer = SkillNormalizer()

    result = normalizer.normalize("SomethingUnknown")

    assert result is None
