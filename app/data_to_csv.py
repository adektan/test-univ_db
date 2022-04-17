import pandas as pd
from config import db_engine
import os

query = '''
select * from analytics.datamart_agg_attandence
'''

dirpath = os.getcwd()
print("dirpath = ", dirpath, "\n")
output_path = os.path.join(dirpath,'report_attendance.csv')
print(output_path,"\n")

df = pd.read_sql(query, con=db_engine)
df.to_csv(output_path, index=False)

print('File CSV has been created')