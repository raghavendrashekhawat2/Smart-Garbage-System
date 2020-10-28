
import sqlite3

conn = sqlite3.connect('garbage.db')
c = conn.cursor()


c.execute(""" CREATE TABLE users (user_id  integer primary key,
                name text,
                user_name text,
                password text,
                gender varchar(7),
                age int)
                """)


c.execute(""" CREATE TABLE loc (bin_id integer primary key,
                country text,
                state text,
                city text,
                lat double,
                lng double,
                imp_location int
                )""")


c.execute(""" CREATE TABLE g_list (bin_id integer primary key,
               date varchar(10),
               time varchar(10),
               per_filled float,
               air_poll text,
               odour text,
               priority int
                )""")


c.execute(""" CREATE TABLE history (bin_id integer primary key,
                date varchar(10),
                time varchar(10),
                per_filled float,
                air_poll text,
                odour text
                priority int
                )""")



#c.execute(""" DROP TABLE g_list""")
conn.commit()
conn.close()
