from app.services.job_matching_service import JobMatchingService


def test_partial_match():
    service = JobMatchingService()

    result = service.match(
        candidate_skills=["python", "aws"],
        job_offer_skills=["python", "aws", "docker", "kubernetes"],
    )

    assert result.matched_skills == ["aws", "python"]
    assert result.missing_skills == ["docker", "kubernetes"]
    assert result.score == 50.0


def test_full_match():
    service = JobMatchingService()

    result = service.match(
        candidate_skills=["python", "aws", "docker", "kubernetes"],
        job_offer_skills=["python", "aws", "docker", "kubernetes"],
    )

    assert result.matched_skills == ["aws", "docker", "kubernetes", "python"]
    assert result.missing_skills == []
    assert result.score == 100.0


def test_no_match():
    service = JobMatchingService()

    result = service.match(
        candidate_skills=["java", "c++"],
        job_offer_skills=["python", "aws", "docker", "kubernetes"],
    )

    assert result.matched_skills == []
    assert result.missing_skills == ["aws", "docker", "kubernetes", "python"]
    assert result.score == 0.0


def test_empty_job_offer_skills():
    service = JobMatchingService()

    result = service.match(
        candidate_skills=["python", "aws"],
        job_offer_skills=[],
    )

    assert result.matched_skills == []
    assert result.missing_skills == []
    assert result.score == 0.0
