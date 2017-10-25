import sqlite3


conn = sqlite3.connect('class.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS class')
cur.execute('CREATE TABLE class (name TEXT, age INTEGER)')

cur.execute('INSERT INTO class (name, age) VALUES (?,?)', ('Caethan', 36))


cur.execute('INSERT INTO class (name, age) VALUES ("Albert", 33)')
cur.execute('INSERT INTO class (name, age) VALUES ("Rohin", 24)')
# cur.execute("INSERT INTO class (name, age) VALUES ("Etinosa", 13)")
# cur.execute("INSERT INTO class (name, age) VALUES ("Manal", 16)")


cur.close()
conn.commit() #needed to insert data

conn.close()

# Code: http://www.pythonlearn.com/code3/db1.py
# Or select Download from this trinket's left-hand menu
