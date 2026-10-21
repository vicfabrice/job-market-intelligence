from pydantic import BaseModel, Field


class JobMatchRequest(BaseModel):
    candidate_skills: list[str] = Field(min_length=1)


class JobMatchResponse(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    score: float
