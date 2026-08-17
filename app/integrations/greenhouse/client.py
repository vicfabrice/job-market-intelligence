import httpx

from app.integrations.greenhouse.schemas import GreenhouseJob


class GreenhouseClient:
    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

    def __init__(
        self,
        client: httpx.Client | None = None,
    ) -> None:
        self.client = client or httpx.Client(timeout=10.0)

    def get_jobs(
        self,
        board_token: str,
    ) -> list[GreenhouseJob]:
        url = f"{self.BASE_URL}/{board_token}/jobs"

        response = self.client.get(url)

        response.raise_for_status()

        data = response.json()

        return [GreenhouseJob.model_validate(job) for job in data["jobs"]]
