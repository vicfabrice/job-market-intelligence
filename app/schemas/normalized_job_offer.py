from datetime import datetime

from pydantic import BaseModel


class NormalizedJobOffer(BaseModel):
    external_id: str
    source: str

    company_name: str
    title: str

    source_url: str | None = None
    location: str | None = None
    description: str | None = None
    published_at: datetime | None = None
