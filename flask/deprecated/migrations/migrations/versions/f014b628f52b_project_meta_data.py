"""project meta data

Revision ID: f014b628f52b
Revises: c250914d23de
Create Date: 2018-12-17 12:07:25.809212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f014b628f52b'
down_revision = 'c250914d23de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_story', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'project_meta_data', ['project_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_story', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###