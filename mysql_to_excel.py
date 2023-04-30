

import mysql.connector
import pandas as pd

table_name = 'Thesecret'
db_name = 'crawling'
output_file = "Thesecret_blogs"


conn = mysql.connector.connect(host="localhost", user="root", passwd="Lalita@123", db=db_name,charset="utf8", use_unicode=True)
cursor = conn.cursor(dictionary=True)

cursor.execute(f'select * from {table_name}')
df = pd.DataFrame(cursor.fetchall())
df.to_excel(f'{output_file}.xlsx',index=False)