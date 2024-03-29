from sqlalchemy import Table
from sqlalchemy import MetaData
import rsdf


def get_table_metadata(table_name, schema):
    engine = rsdf.get_engine()
    metadata = MetaData()
    table = Table(table_name, metadata, schema=schema, autoload=True, autoload_with=engine)

    return table
