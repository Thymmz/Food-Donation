import sqlite3

conn = sqlite3.connect('users1.db')

c = conn.cursor()
c.execute("CREATE TABLE users1 (username TEXT PRIMARY KEY, encryptedpassword TEXT NOT NULL, re_password TEXT NOT NULL)")

conn.commit()
conn.close()