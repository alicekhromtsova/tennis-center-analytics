import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="tennis_center",
    user="postgres",
    password="7255"
)
cursor = conn.cursor()

with open("sql/marts.sql", "r", encoding="utf-8") as f:
    marts_sql = f.read()

cursor.execute(marts_sql)
conn.commit()

print("Витрины созданы")