import httpx

from app.integrations.greenhouse.client import GreenhouseClient


def test_get_jobs_returns_greenhouse_jobs() -> None:
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        assert str(request.url) == (
            "https://boards-api.greenhouse.io/v1/boards/example-company/jobs"
        )

        return httpx.Response(
            200,
            json={
                "jobs": [
                    {
                        "id": 123456,
                        "title": "Backend Engineer",
                        "absolute_url": ("https://example.com/jobs/123456"),
                        "location": {"name": "Remote"},
                        "updated_at": ("2026-08-17T12:00:00Z"),
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)

    http_client = httpx.Client(transport=transport)

    greenhouse_client = GreenhouseClient(client=http_client)

    jobs = greenhouse_client.get_jobs("example-company")

    assert len(jobs) == 1

    job = jobs[0]

    assert job.id == 123456
    assert job.title == "Backend Engineer"
    assert job.location.name == "Remote"
