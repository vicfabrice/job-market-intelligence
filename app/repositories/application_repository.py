from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
)


class ApplicationRepository:
    def __init__(self, database_session: Session) -> None:
        self.database_session = database_session

    def create(
        self,
        application_data: ApplicationCreate,
    ) -> Application:
        application = Application(**application_data.model_dump())

        self.database_session.add(application)
        self.database_session.commit()
        self.database_session.refresh(application)

        return application

    def get_all(self) -> list[Application]:
        statement = select(Application).order_by(Application.applied_at.desc())

        return list(self.database_session.scalars(statement).all())

    def get_by_id(
        self,
        application_id: int,
    ) -> Application | None:
        return self.database_session.get(
            Application,
            application_id,
        )

    def get_by_job_offer_id(
        self,
        job_offer_id: int,
    ) -> Application | None:
        statement = select(Application).where(Application.job_offer_id == job_offer_id)

        return self.database_session.scalar(statement)

    def update(
        self,
        application: Application,
        application_data: ApplicationUpdate,
    ) -> Application:
        update_data = application_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(application, field, value)

        self.database_session.commit()
        self.database_session.refresh(application)

        return application

    def delete(
        self,
        application: Application,
    ) -> None:
        self.database_session.delete(application)
        self.database_session.commit()
