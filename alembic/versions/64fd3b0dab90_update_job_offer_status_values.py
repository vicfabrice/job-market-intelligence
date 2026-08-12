"""update job offer status values

Revision ID: 64fd3b0dab90
Revises: a8a6345894a3
Create Date: 2026-08-12 13:53:22.118695

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "64fd3b0dab90"
down_revision: str | Sequence[str] | None = "a8a6345894a3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

old_status_enum = sa.Enum(
    "saved",
    "applied",
    "interview",
    "technical_interview",
    "offer",
    "rejected",
    "withdrawn",
    name="job_offer_status_enum",
)

new_status_enum = sa.Enum(
    "active",
    "closed",
    "expired",
    name="job_offer_status_enum",
)


def upgrade() -> None:
    # 1. Sacar el default viejo para romper la dependencia con el enum
    op.alter_column(
        "job_offers",
        "status",
        server_default=None,
    )

    # 2. Pasar temporalmente la columna a texto
    op.alter_column(
        "job_offers",
        "status",
        type_=sa.String(),
        postgresql_using="status::text",
    )

    # 3. Ahora sí eliminar el enum viejo
    old_status_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )

    # 4. Crear el enum nuevo
    new_status_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    # 5. Como estamos en desarrollo, mapear todos los valores viejos a active
    op.execute(
        """
        UPDATE job_offers
        SET status = 'active'
        """
    )

    # 6. Convertir la columna al nuevo enum
    op.alter_column(
        "job_offers",
        "status",
        type_=new_status_enum,
        postgresql_using="status::job_offer_status_enum",
        server_default="active",
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "job_offers",
        "status",
        server_default=None,
    )

    op.alter_column(
        "job_offers",
        "status",
        type_=sa.String(),
        postgresql_using="status::text",
    )

    new_status_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )

    old_status_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.execute(
        """
        UPDATE job_offers
        SET status = 'saved'
        """
    )

    op.alter_column(
        "job_offers",
        "status",
        type_=old_status_enum,
        postgresql_using="status::job_offer_status_enum",
        server_default="saved",
        nullable=False,
    )
