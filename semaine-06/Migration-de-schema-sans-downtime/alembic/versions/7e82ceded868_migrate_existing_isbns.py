"""migrate existing isbns

Revision ID: 7e82ceded868
Revises: efa0ad6538e3
Create Date: 2026-08-20 17:06:44.532236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e82ceded868'
down_revision: Union[str, Sequence[str], None] = 'efa0ad6538e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            INSERT INTO isbns (isbn, book_id)
            SELECT isbn, id
            FROM books
            WHERE isbn IS NOT NULL
            """
        )
    )



def downgrade() -> None:
    op.execute("DELETE FROM isbns")
