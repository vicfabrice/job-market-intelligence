from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_offer import JobOffer
from app.schemas.job_offer import JobOfferCreate, JobOfferUpdate


class JobOfferRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job_offer_data: JobOfferCreate) -> JobOffer:
        job_offer = JobOffer(**job_offer_data.model_dump())

        self.db.add(job_offer)
        self.db.commit()
        self.db.refresh(job_offer)

        return job_offer

    def get_all(self) -> list[JobOffer]:
        statement = select(JobOffer).order_by(JobOffer.created_at.desc())

        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        job_offer_id: int,
    ) -> JobOffer | None:
        return self.db.get(
            JobOffer,
            job_offer_id,
        )

    def update(
        self,
        job_offer: JobOffer,
        job_offer_data: JobOfferUpdate,
    ) -> JobOffer:
        update_data = job_offer_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(job_offer, field, value)

        self.db.commit()
        self.db.refresh(job_offer)

        return job_offer

    def delete(
        self,
        job_offer: JobOffer,
    ) -> None:
        self.db.delete(job_offer)
        self.db.commit()

    def get_by_source_and_external_id(
        self,
        source: str,
        external_id: str,
    ) -> JobOffer | None:
        statement = select(JobOffer).where(
            JobOffer.source == source,
            JobOffer.external_id == external_id,
        )

        return self.db.scalar(statement)
