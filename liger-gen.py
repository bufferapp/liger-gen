import sys
from liger_gen.db import get_table_metadata
from liger_gen.generate import LigerView
#Command line
import click
@click.command()
@click.argument('table_name')
def generate(table_name):
    table = get_table_metadata(table_name)
    l = LigerView(table)
    l.generate_lookml(sys.stdout)

if __name__ == '__main__':
    generate()
