from datetime import UTC, datetime

from app.integrations.greenhouse.mapper import (
    map_greenhouse_job,
)
from app.integrations.greenhouse.schemas import (
    GreenhouseJob,
    GreenhouseLocation,
)


def test_map_greenhouse_job_returns_normalized_job() -> None:
    job = GreenhouseJob(
        id=123456,
        title="Backend Engineer",
        absolute_url="https://example.com/jobs/123456",
        location=GreenhouseLocation(name="Remote"),
        updated_at=datetime(
            2026,
            8,
            17,
            12,
            0,
            tzinfo=UTC,
        ),
    )

    result = map_greenhouse_job(
        job=job,
        company_name="Example Company",
    )

    assert result.external_id == "123456"
    assert result.source == "greenhouse"
    assert result.company_name == "Example Company"
    assert result.title == "Backend Engineer"
    assert result.location == "Remote"
