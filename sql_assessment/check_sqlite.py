import sqlite3
conn = sqlite3.connect(r'C:\Users\Admin\Desktop\worklogs\product_enhancement\data\digii_campus.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", [r[0] for r in c.fetchall()])
