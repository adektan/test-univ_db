import pandas as pd
import psycopg2
import sqlalchemy
from pytz import timezone
from datetime import datetime
from config import sources, db_engine, schema_raw

# layer schema for as is data from source, this schema will append data and keep historical data from source as is
schema_name = schema_raw

def _get_data(source, url): 
    file_id=url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?id=' + file_id
    df = pd.read_csv(dwn_url)
    table_name = source
    return df, table_name

for table, value in sources.items():
    data = _get_data(table, value['url'])
    if not db_engine.dialect.has_schema(db_engine, schema_name):
        db_engine.execute(sqlalchemy.schema.CreateSchema(schema_name))
    
    asia_jakarta = timezone('Asia/Jakarta')
    tz_time = datetime.now(asia_jakarta)
    data[0]['insert_time'] = tz_time
    df = data[0]
    total_rows = str(df.shape)
    r = df.to_sql(data[1], db_engine, if_exists="append", schema=schema_name, index=False)
    
    print('Table {0} in schema {1} has been insert, total rows and column : {2}'.format(table, schema_name, total_rows))
    
    
    