from sqlalchemy import Column, ForeignKey, Integer, Table

from app.core.database import Base

job_offer_skills = Table(
    "job_offer_skills",
    Base.metadata,
    Column(
        "job_offer_id",
        Integer,
        ForeignKey(
            "job_offers.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "skill_id",
        Integer,
        ForeignKey(
            "skills.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)
