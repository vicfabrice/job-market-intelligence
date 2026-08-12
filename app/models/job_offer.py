from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import JobOfferStatus, WorkMode

if TYPE_CHECKING:
    from app.models.company import Company


class JobOffer(Base):
    __tablename__ = "job_offers"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey(
            "companies.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    work_mode: Mapped[WorkMode | None] = mapped_column(
        Enum(
            WorkMode,
            name="work_mode_enum",
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        nullable=True,
        index=True,
    )

    status: Mapped[JobOfferStatus] = mapped_column(
        Enum(
            JobOfferStatus,
            name="job_offer_status_enum",
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        nullable=False,
        default=JobOfferStatus.SAVED,
        server_default=JobOfferStatus.SAVED.value,
        index=True,
    )

    salary_min: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=True,
    )

    salary_max: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=True,
    )

    currency: Mapped[str | None] = mapped_column(
        String(3),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    company: Mapped["Company"] = relationship(
        back_populates="job_offers",
    )
