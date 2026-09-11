from pydantic import BaseModel


class GreenhouseCompanyConfig(BaseModel):
    name: str
    board_token: str
    sector: str | None = None


GREENHOUSE_COMPANIES = [
    GreenhouseCompanyConfig(
        name="Anthropic",
        board_token="anthropic",
    sector="Technology",
    ),
]
