from datetime import datetime

from pydantic import BaseModel


class GreenhouseLocation(BaseModel):
    name: str


class GreenhouseJob(BaseModel):
    id: int
    title: str
    absolute_url: str
    location: GreenhouseLocation
    updated_at: datetime
