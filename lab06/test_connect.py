# test_connect.py
import mysql.connector as mc

conn = mc.connect(
    host="cscdata.centre.edu",
    user="db_agent_b2",        # change per team
    password="MadKen_25",  # your team's password
    database="gravity_books"
)

cur = conn.cursor()

print("Sample titles from v_books:")
cur.execute("SELECT title FROM v_books LIMIT 3;")
row = cur.fetchone()
while row:
    print(" -", row[0])
    row = cur.fetchone()

print("\nBooks with 'gravity' in the title:")
cur.execute("SELECT title FROM book WHERE title LIKE '%gravity%';")
row = cur.fetchone()
while row:
    print(" -", row[0])
    row = cur.fetchone()

cur.close()
conn.close()
