from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class CompanyBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
        examples=["Globant"],
    )
    website: HttpUrl | None = None
    sector: str | None = Field(
        default=None,
        max_length=150,
        examples=["Software"],
    )
    country: str | None = Field(
        default=None,
        max_length=100,
        examples=["Argentina"],
    )


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )
    website: HttpUrl | None = None
    sector: str | None = Field(default=None, max_length=150)
    country: str | None = Field(default=None, max_length=100)


class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
