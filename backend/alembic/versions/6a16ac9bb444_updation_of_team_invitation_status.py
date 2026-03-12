"""updation of team invitation status

Revision ID: 6a16ac9bb444
Revises: 4e6809542774
Create Date: 2026-03-12 02:06:56.507106

"""

from typing import Sequence, Union


from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a16ac9bb444"
down_revision: Union[str, None] = "4e6809542774"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE team_invitations "
        "MODIFY COLUMN status ENUM('pending','accepted','declined') NOT NULL"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE team_invitations " "MODIFY COLUMN status VARCHAR(50) NOT NULL"
    )
