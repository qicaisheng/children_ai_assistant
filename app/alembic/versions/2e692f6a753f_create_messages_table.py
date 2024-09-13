"""Create messages table

Revision ID: 2e692f6a753f
Revises: 
Create Date: 2024-09-13 11:19:20.238307

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e692f6a753f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('role_code', sa.Integer, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('audio_id', sa.ARRAY(sa.String), nullable=True, default=[]),
        sa.Column('message_type', sa.String, nullable=False),
        sa.Column('parent_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('created_time', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('messages')
