from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import ApplicationStatus


class ApplicationCreate(BaseModel):
    job_offer_id: int
    applied_at: datetime
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus | None = None
    applied_at: datetime | None = None
    notes: str | None = None


class ApplicationResponse(BaseModel):
    id: int
    job_offer_id: int
    status: ApplicationStatus
    applied_at: datetime
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
