import pandas as pd
import psycopg2
import sqlalchemy
from pytz import timezone
from datetime import datetime
from config import sources, db_engine, schema_dataset

# layer schema from raw layer, this schema truncate insert for this case, although maybe it also insert update
# this schema should query able data from source

schema_name = schema_dataset

for table, value in sources.items():
    if not db_engine.dialect.has_schema(db_engine, schema_name):
        db_engine.execute(sqlalchemy.schema.CreateSchema(schema_name))
    
    df = pd.read_sql(value['query_to_dataset'], con=db_engine)
    total_rows = str(df.shape)

    r = df.to_sql(table, db_engine, if_exists="replace", schema=schema_name, index=False)

    print('Table {0} in schema {1} has been insert, total rows and column : {2}'.format(table, schema_name, total_rows))