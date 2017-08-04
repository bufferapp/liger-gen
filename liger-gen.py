import sys
from liger_gen.db import get_table_metadata
from liger_gen.generate import LigerView
#Command line
import click
@click.command()
@click.argument('table_name')
@click.option('--schema',default='dbt')
def generate(table_name, schema):
    table = get_table_metadata(table_name, schema)
    l = LigerView(table)
    l.generate_lookml(sys.stdout)

if __name__ == '__main__':
    generate()
