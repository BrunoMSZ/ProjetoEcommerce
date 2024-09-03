
import psycopg2
import boto3

ENDPOINT="sonicpads.c50yoy0muka9.sa-east-1.rds.amazonaws.com"
PORT="3306"
USER="admin"
REGION="sa-east-1a"
DBNAME="sonicpads"

try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER)
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))                
                