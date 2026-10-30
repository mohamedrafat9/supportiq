"""add ticket status check constraint

Revision ID: 633600576f58
Revises: 844c85379158
Create Date: 2026-10-30 01:44:00.821077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '633600576f58'
down_revision: Union[str, Sequence[str], None] = '844c85379158'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_ticket_status",
        "tickets",
        "status IN ('open', 'in_progress', 'resolved', 'closed')",
    )


def downgrade() -> None:
    op.drop_constraint(
        "check_ticket_status",
        "tickets",
        type_="check",
    )
