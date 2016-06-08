"""Add Cirrus

Revision ID: 600_Cirrus
Revises: 590
Create Date: 2015-06-17 14:44:08.138355
"""

# revision identifiers, used by Alembic.
revision = '600_Cirrus'
down_revision = '590'

from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Boolean


frameworks = table('frameworks',
    column('name', String),
    column('framework', String),
    column('slug', String),
    column('status', String),
    column('clarification_questions_open', Boolean)
)


def upgrade():
    op.execute(
        frameworks.insert().
        values({'name': op.inline_literal('Cirrus Framework'),
                'framework': op.inline_literal('cirrus'),
                'slug': op.inline_literal('cirrus'),
                'status': op.inline_literal('open'),
                'clarification_questions_open': op.inline_literal(False),
                }))

    lot_table = table(
        'lots',
        column('name', String),
        column('slug', String),
        column('one_service_limit', Boolean)
    )

    op.bulk_insert(lot_table, [
        {'name': 'Contingent Labour and Consultancy Services', 'slug': 'clcs', 'one_service_limit': False},
        {'name': 'Catering Services', 'slug': 'catering', 'one_service_limit': False},
    ])

    conn = op.get_bind()
    res = conn.execute("SELECT id FROM frameworks WHERE slug = 'cirrus'")
    framework = list(res.fetchall())

    res = conn.execute("SELECT id FROM lots WHERE slug in ('clcs', 'catering', 'saas', 'iaas')")
    lots = list(res.fetchall())

    if len(framework) == 0:
        raise Exception("Framework not found")

    for lot in lots:
        op.execute("INSERT INTO framework_lots (framework_id, lot_id) VALUES({}, {})".format(
            framework[0]["id"], lot["id"]))


def downgrade():

    conn = op.get_bind()
    res = conn.execute("SELECT id FROM frameworks WHERE slug = 'cirrus'")
    framework = list(res.fetchall())

    op.execute("""
        DELETE FROM framework_lots WHERE framework_id={}
    """.format(framework[0]['id']))

    op.execute("""
        DELETE from lots WHERE slug in ('clcs', 'catering');
    """)
    
    op.execute(
        frameworks.delete().where(frameworks.c.name == 'Cirrus Framework'))