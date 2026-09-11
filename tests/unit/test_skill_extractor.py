from app.services.skill_extractor import SkillExtractor
from app.services.skill_normalizer import SkillNormalizer


def test_extracts_skills_from_text() -> None:
    extractor = SkillExtractor(SkillNormalizer())

    text = """
    We are looking for a backend engineer with experience in
    Python, FastAPI, PostgreSQL and Docker.
    """

    result = extractor.extract(text)

    assert result == [
        "docker",
        "fastapi",
        "postgresql",
        "python",
    ]


def test_extracts_aliases_as_normalized_skills() -> None:
    extractor = SkillExtractor(SkillNormalizer())

    text = """
    Experience with Postgres and Kubernetes is required.
    """

    result = extractor.extract(text)

    assert result == [
        "kubernetes",
        "postgresql",
    ]


def test_does_not_return_duplicates() -> None:
    extractor = SkillExtractor(SkillNormalizer())

    text = """
    Python experience required.
    Strong Python knowledge is expected.
    """

    result = extractor.extract(text)

    assert result == ["python"]


def test_is_case_insensitive() -> None:
    extractor = SkillExtractor(SkillNormalizer())

    text = """
    Experience with PYTHON and FASTAPI.
    """

    result = extractor.extract(text)

    assert result == [
        "fastapi",
        "python",
    ]


def test_returns_empty_list_when_no_known_skills_are_found() -> None:
    extractor = SkillExtractor(SkillNormalizer())

    text = """
    We are looking for someone with strong communication skills.
    """

    result = extractor.extract(text)

    assert result == []
