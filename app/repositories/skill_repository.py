from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.skill import Skill


class SkillRepository:
    def __init__(self, database_session: Session) -> None:
        self.database_session = database_session

    def get_by_normalized_name(
        self,
        normalized_name: str,
    ) -> Skill | None:
        statement = select(Skill).where(Skill.normalized_name == normalized_name)

        return self.database_session.scalar(statement)

    def create(
        self,
        name: str,
        normalized_name: str,
    ) -> Skill:
        skill = Skill(
            name=name,
            normalized_name=normalized_name,
        )

        self.database_session.add(skill)
        self.database_session.flush()

        return skill
