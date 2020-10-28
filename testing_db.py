import _sqlite3
conn = _sqlite3.connect('garbage.db')
c = conn.cursor()
'''
c.execute(""" CREATE TABLE Persons (Personid INTEGER PRIMARY KEY,
                                    LastName varchar(255) NOT NULL,
                                    FirstName varchar(255),
                                    Age int
                                    )   """)


c.execute("""INSERT INTO g_list (bin_id, date, time, per_filled, air_poll, odour)
            VALUES(6, "02-03-2020", "8:08PM", "16", "Good", "None")""")
conn.commit()
'''

# c.execute("""UPDATE g_list set per_filled = "85", air_poll = "150" WHERE bin_id = 1  """)
c.execute("""UPDATE loc set imp_location = 13 WHERE bin_id = 1  """)
conn.commit()
'''




c.execute("SELECT * FROM users")
conn.commit()

rows = c.fetchall()
print(rows)

c.execute("SELECT * FROM loc")
conn.commit()
rows = c.fetchall()
print(rows)

c.execute("SELECT * FROM g_list")
conn.commit()
rows = c.fetchall()
print(rows)
'''
conn.close()