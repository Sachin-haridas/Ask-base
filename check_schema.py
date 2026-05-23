# add to check_schema.py or create a new file called export_data.py
import psycopg2
import json

conn = psycopg2.connect('postgresql://postgres:Sachincena%4072@localhost:5432/ai_analytics_db')
cur = conn.cursor()

for table in ['customers', 'products', 'orders']:
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    print(f"\n-- {table} --")
    for row in rows:
        print(row)

cur.close()
conn.close()