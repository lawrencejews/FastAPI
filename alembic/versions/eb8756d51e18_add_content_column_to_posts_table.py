"""add content column to posts table

Revision ID: eb8756d51e18
Revises: 4c7a94fc7576
Create Date: 2023-02-14 17:46:51.413572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb8756d51e18'
down_revision = '4c7a94fc7576'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
