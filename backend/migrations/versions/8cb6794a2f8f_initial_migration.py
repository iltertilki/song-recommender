"""Initial migration.

Revision ID: 8cb6794a2f8f
Revises: 
Create Date: 2024-04-29 14:38:48.559633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cb6794a2f8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_rating_user', 'user', ['user_id'], ['id'])  # Named foreign key

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.drop_constraint('fk_rating_user', type_='foreignkey')  # Use the same name to drop it
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###