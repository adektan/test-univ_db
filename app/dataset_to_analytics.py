import pandas as pd
import psycopg2
import sqlalchemy
from pytz import timezone
from datetime import datetime
from config import analytics_source, db_engine, schema_analytics

# layer schema from dataset, to fact, dim , and also datamart layer for this case using truncate insert, although maybe it also insert update

schema_name = schema_analytics

for table, query in analytics_source.items():
    if not db_engine.dialect.has_schema(db_engine, schema_name):
        db_engine.execute(sqlalchemy.schema.CreateSchema(schema_name))
    
    df = pd.read_sql(query, con=db_engine)
    total_rows = str(df.shape)

    r = df.to_sql(table, db_engine, if_exists="replace", schema=schema_name, index=False)

    print('Table {0} in schema {1} has been insert, total rows and column : {2}'.format(table, schema_name, total_rows))