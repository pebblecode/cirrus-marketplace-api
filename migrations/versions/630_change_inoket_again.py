"""Add Inoket-1

Revision ID: 630_Inoket
Revises: 620_Inoket
Create Date: 2015-06-17 14:44:08.138355
"""

# revision identifiers, used by Alembic.
revision = '630_Inoket'
down_revision = '620_Inoket'

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
    # Leave off for now until clarified by Stephen
    pass

    # # Delete the old one
    
    # conn = op.get_bind()
    # res = conn.execute("SELECT id FROM frameworks WHERE slug = 'inoket-1'")
    # framework = list(res.fetchall())

    # op.execute("""
    #     DELETE FROM framework_lots WHERE framework_id={}
    # """.format(framework[0]['id']))

    # op.execute("""
    #     DELETE from lots WHERE slug in ('supply_teachers');
    # """)

    # op.execute(
    #     frameworks.delete().where(frameworks.c.name == 'Inoket Framework'))

    # # Make a new one

    # op.execute(
    #     frameworks.insert().
    #     values({'name': op.inline_literal('Inoket Framework'),
    #             'framework': op.inline_literal('inoket-1'),
    #             'slug': op.inline_literal('inoket-1'),
    #             'status': op.inline_literal('open'),
    #             'clarification_questions_open': op.inline_literal(False),
    #             }))

    # lot_table = table(
    #     'lots',
    #     column('name', String),
    #     column('slug', String),
    #     column('one_service_limit', Boolean)
    # )

    # op.bulk_insert(lot_table, [
    #     {'name': 'Supply Teachers', 'slug': 'supply_teachers', 'one_service_limit': False},
    #     {'name': 'Infrastructure as a Service', 'slug': 'iaas', 'one_service_limit': False},
    #     {'name': 'Platform as a Service', 'slug': 'paas', 'one_service_limit': False},
    #     {'name': 'Software as a Service', 'slug': 'saas', 'one_service_limit': False},
    #     {'name': 'Specialist Cloud Services', 'slug': 'scs', 'one_service_limit': False}
    # ])

    # conn = op.get_bind()
    # res = conn.execute("SELECT id FROM frameworks WHERE slug = 'inoket-1'")
    # framework = list(res.fetchall())

    # # Add more lots like this when necessary, just supply teachers for now
    # res = conn.execute("SELECT id FROM lots WHERE slug in ('supply_teachers', 'iaas', 'paas', 'saas', 'scs')")
    # lots = list(res.fetchall())

    # if len(framework) == 0:
    #     raise Exception("Framework not found")

    # for lot in lots:
    #     op.execute("INSERT INTO framework_lots (framework_id, lot_id) VALUES({}, {})".format(
    #         framework[0]["id"], lot["id"]))


def downgrade():
    # Leave off for now until clarified by Stephen
    pass

    # # Delete the new one

    # conn = op.get_bind()
    # res = conn.execute("SELECT id FROM frameworks WHERE slug = 'inoket-1'")
    # framework = list(res.fetchall())

    # op.execute("""
    #     DELETE FROM framework_lots WHERE framework_id={}
    # """.format(framework[0]['id']))

    # op.execute("""
    #     DELETE from lots WHERE slug in ('supply_teachers', 'iaas', 'paas', 'saas', 'scs');
    # """)
    
    # op.execute(
    #     frameworks.delete().where(frameworks.c.name == 'Inoket Framework'))

    # # Make the old one

    # op.execute(
    #     frameworks.insert().
    #     values({'name': op.inline_literal('Inoket Framework'),
    #             'framework': op.inline_literal('inoket-1'),
    #             'slug': op.inline_literal('inoket-1'),
    #             'status': op.inline_literal('open'),
    #             'clarification_questions_open': op.inline_literal(False),
    #             }))

    # lot_table = table(
    #     'lots',
    #     column('name', String),
    #     column('slug', String),
    #     column('one_service_limit', Boolean)
    # )

    # op.bulk_insert(lot_table, [
    #     {'name': 'Supply Teachers', 'slug': 'supply_teachers', 'one_service_limit': False}
    # ])

    # conn = op.get_bind()
    # res = conn.execute("SELECT id FROM frameworks WHERE slug = 'inoket-1'")
    # framework = list(res.fetchall())

    # # Add more lots like this when necessary, just supply teachers for now
    # res = conn.execute("SELECT id FROM lots WHERE slug in ('supply_teachers')")
    # lots = list(res.fetchall())

    # if len(framework) == 0:
    #     raise Exception("Framework not found")

    # for lot in lots:
    #     op.execute("INSERT INTO framework_lots (framework_id, lot_id) VALUES({}, {})".format(
    #         framework[0]["id"], lot["id"]))


