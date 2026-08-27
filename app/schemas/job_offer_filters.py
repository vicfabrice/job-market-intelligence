from pydantic import BaseModel, Field

from app.models.enums import JobOfferStatus, WorkMode


class JobOfferFilters(BaseModel):
    title: str | None = None
    sector: str | None = None
    location: str | None = None
    work_mode: WorkMode | None = None
    status: JobOfferStatus | None = None
    source: str | None = None
    company_id: int | None = None

    limit: int = Field(
        default=50,
        ge=1,
        le=100,
    )

    offset: int = Field(
        default=0,
        ge=0,
    )
