"""add project comments table

Revision ID: a8d2e82854a1
Revises: 6a16ac9bb444
Create Date: 2026-03-13 14:19:07.944529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8d2e82854a1'
down_revision: Union[str, None] = '6a16ac9bb444'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "project_comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_project_comments_project_created",
        "project_comments",
        ["project_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_project_comments_author_id",
        "project_comments",
        ["author_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_project_comments_author_id", table_name="project_comments")
    op.drop_index("ix_project_comments_project_created", table_name="project_comments")
    op.drop_table("project_comments")
