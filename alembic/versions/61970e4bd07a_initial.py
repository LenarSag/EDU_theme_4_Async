"""initial

Revision ID: 61970e4bd07a
Revises: 
Create Date: 2024-12-31 13:36:09.282297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '61970e4bd07a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trading_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exchange_product_id', sa.String(), nullable=False),
    sa.Column('exchange_product_name', sa.String(), nullable=False),
    sa.Column('oil_id', sa.String(), nullable=True),
    sa.Column('delivery_basis_id', sa.String(), nullable=True),
    sa.Column('delivery_basis_name', sa.String(), nullable=True),
    sa.Column('delivery_type_id', sa.String(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_subject_score_student_id', table_name='subject_score')
    op.drop_table('subject_score')
    op.drop_index('ix_student_id', table_name='student')
    op.drop_table('student')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('student_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='student_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_student_id', 'student', ['id'], unique=False)
    op.create_table('subject_score',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subject_name', postgresql.ENUM('математика', 'русский язык', 'информатика', 'физика', 'химия', 'биология', name='subjectname'), autoincrement=False, nullable=False),
    sa.Column('score', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='subject_score_student_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='subject_score_pkey')
    )
    op.create_index('ix_subject_score_student_id', 'subject_score', ['student_id'], unique=False)
    op.drop_table('trading_results')
    # ### end Alembic commands ###
