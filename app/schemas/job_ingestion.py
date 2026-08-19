from pydantic import BaseModel


class JobIngestionResult(BaseModel):
    received: int = 0
    created: int = 0
    skipped: int = 0
    companies_created: int = 0
