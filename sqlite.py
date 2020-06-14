import sqlite3
import time
import datetime
import random

conn = sqlite3.connect('drawingIdeas.db')
f = open("randomLists/randomIdeas.txt","r")
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS drawingIdeas(idea TEXT, tag TEXT, value TEXT)')

def data_entry():
    c.execute("INSERT INTO drawingIdeas VALUES('Pencil', 'Object', 'Happy')")
    conn.commit()
    c.close()
    conn.close() 

#creates a new entry in drawingideas.db, which contains a (idea, tag, value) ordered triple
def dynamic_data_entry():
    for line in f:
        idea = str(line.strip())
        tag = 'Idea'
        value = 'Happy'
        c.execute("INSERT INTO drawingIdeas (idea, tag, value) VALUES(?, ?, ?)", (idea, tag, value))
    conn.commit()

def read_from_db():
    # gets a random row
    c.execute("SELECT * FROM drawingIdeas WHERE tag='Thing' OR tag='Food' ORDER BY RANDOM() LIMIT 1")
    data = c.fetchall()
    for row in data:
        idea = row[0]
    print(idea)

# create_table()
dynamic_data_entry()
# read_from_db()

# for i in range(10):
#     dynamic_data_entry()
#     time.sleep(1)

c.close()
conn.close()