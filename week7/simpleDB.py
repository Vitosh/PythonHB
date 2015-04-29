import sqlite3

conn = sqlite3.connect("polyglot.db")
cursor = conn.cursor()

result = cursor.execute("SELECT id, language FROM languages")

for row in result:
    print(row)