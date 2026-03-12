"""add email verification fields to users

Revision ID: df0fe3c8aa25
Revises: c55bfc75ce69
Create Date: 2026-03-11 13:27:47.612727

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "df0fe3c8aa25"
down_revision: Union[str, None] = "c55bfc75ce69"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "email_verified", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )
    op.add_column(
        "users", sa.Column("verification_token", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "verification_token")
    op.drop_column("users", "email_verification")
