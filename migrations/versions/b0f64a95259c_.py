"""empty message

Revision ID: b0f64a95259c
Revises: 55b94f76cdba
Create Date: 2023-05-21 16:40:57.063804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0f64a95259c'
down_revision = '55b94f76cdba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audio_recordings',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_audio_recordings_uuid'), 'audio_recordings', ['uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_audio_recordings_uuid'), table_name='audio_recordings')
    op.drop_table('audio_recordings')
    # ### end Alembic commands ###
