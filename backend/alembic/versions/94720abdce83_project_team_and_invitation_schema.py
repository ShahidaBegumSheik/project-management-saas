"""project team and invitation schema

Revision ID: 94720abdce83
Revises: 2f290d3b5ee1
Create Date: 2026-03-11 23:29:50.581480

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "94720abdce83"
down_revision: Union[str, None] = "2f290d3b5ee1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # allow projects without team
    with op.batch_alter_table("projects") as batch_op:
        batch_op.alter_column("team_id", existing_type=sa.Integer(), nullable=True)

    # add description column to project activities
    with op.batch_alter_table("project_activities") as batch_op:
        batch_op.add_column(
            sa.Column("description", sa.String(length=500), nullable=True)
        )
    op.execute(
        "UPDATE project_activities SET description = action WHERE description IS NULL"
    )
    with op.batch_alter_table("project_activities") as batch_op:
        batch_op.alter_column(
            "description", existing_type=sa.String(length=500), nullable=False
        )

    # update team invitations
    with op.batch_alter_table("team_invitations") as batch_op:
        batch_op.add_column(sa.Column("inviter_user_id", sa.Integer(), nullable=True))
        batch_op.alter_column(
            "invited_user_id", existing_type=sa.Integer(), nullable=True
        )
    op.execute(
        "UPDATE team_invitations SET inviter_user_id = invited_user_id WHERE inviter_user_id IS NULL"
    )

    with op.batch_alter_table("team_invitations") as batch_op:
        batch_op.alter_column(
            "inviter_user_id", existing_type=sa.Integer(), nullable=False
        )


def downgrade() -> None:
    with op.batch_alter_table("team_invitations") as batch_op:
        batch_op.drop_column("inviter_user_id")
        batch_op.alter_column(
            "invited_user_id", existing_type=sa.Integer(), nullable=False
        )

    with op.batch_alter_table("project_activities") as batch_op:
        batch_op.drop_column("description")

    with op.batch_alter_table("projects") as batch_op:
        batch_op.alter_column("team_id", existing_type=sa.Integer(), nullable=False)
