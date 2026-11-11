"""create_initial_tables

Revision ID: 8f32d33f8802
Revises: 
Create Date: 2026-11-11 23:00:20.119714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '8f32d33f8802'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Table: project 
    op.create_table(
        'project',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_is_deleted'), 'project', ['is_deleted'], unique=False)

    # Table: interview (depends on project)
    op.create_table(
        'interview',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('project_id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('sum_embedding', pgvector.sqlalchemy.vector.VECTOR(dim=768), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['project.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interview_is_deleted'), 'interview', ['is_deleted'], unique=False)

    # Table: requirement (no FK dependencies)
    op.create_table(
        'requirement',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('requirement', sa.Text(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('r_embedding', pgvector.sqlalchemy.vector.VECTOR(dim=768), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requirement_is_deleted'), 'requirement', ['is_deleted'], unique=False)

    # Table: q_recommendation (depends on interview; source_qa_id FK added after qa table creation)
    op.create_table(
        'q_recommendation',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('interview_id', sa.Uuid(), nullable=False),
        sa.Column('source_qa_id', sa.Uuid(), nullable=True),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['interview_id'], ['interview.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_q_recommendation_is_deleted'), 'q_recommendation', ['is_deleted'], unique=False)

    # Table: qa (depends on interview and q_recommendation)
    op.create_table(
        'qa',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('interview_id', sa.Uuid(), nullable=False),
        sa.Column('selected_recommendation_id', sa.Uuid(), nullable=True),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('q_embedding', pgvector.sqlalchemy.vector.VECTOR(dim=768), nullable=True),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('a_embedding', pgvector.sqlalchemy.vector.VECTOR(dim=768), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['interview_id'], ['interview.id']),
        sa.ForeignKeyConstraint(['selected_recommendation_id'], ['q_recommendation.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_qa_is_deleted'), 'qa', ['is_deleted'], unique=False)

    # Circular FK: now that qa exists, link q_recommendation.source_qa_id -> qa.id
    op.create_foreign_key(
        'fk_q_recommendation_source_qa_id',
        'q_recommendation',
        'qa',
        ['source_qa_id'],
        ['id']
    )

    # Table: qa_requirement (junction: depends on requirement and qa)
    op.create_table(
        'qa_requirement',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('requirement_id', sa.Uuid(), nullable=False),
        sa.Column('qa_id', sa.Uuid(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['qa_id'], ['qa.id']),
        sa.ForeignKeyConstraint(['requirement_id'], ['requirement.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_qa_requirement_is_deleted'), 'qa_requirement', ['is_deleted'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_qa_requirement_is_deleted'), table_name='qa_requirement')
    op.drop_table('qa_requirement')

    op.drop_constraint('fk_q_recommendation_source_qa_id', 'q_recommendation', type_='foreignkey')

    op.drop_index(op.f('ix_qa_is_deleted'), table_name='qa')
    op.drop_table('qa')

    op.drop_index(op.f('ix_q_recommendation_is_deleted'), table_name='q_recommendation')
    op.drop_table('q_recommendation')

    op.drop_index(op.f('ix_requirement_is_deleted'), table_name='requirement')
    op.drop_table('requirement')

    op.drop_index(op.f('ix_interview_is_deleted'), table_name='interview')
    op.drop_table('interview')

    op.drop_index(op.f('ix_project_is_deleted'), table_name='project')
    op.drop_table('project')
