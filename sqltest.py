import sqlite3
import event

conn = sqlite3.connect('events.db')

cursor = conn.cursor()

cursor.execute("""CREATE TABLE events (
               ID INTEGER PRIMARY KEY AUTOINCREMENT,
               type text,
               name text,
               description text,
               hostid integer
)""")

coolEvent = event.Event("coolevent", "baller", 1, event.EVENT_SSU)
cursor.execute("INSERT INTO events (type, name, description, hostid) VALUES (:type, :name, :description, :host)", {
    'type': coolEvent.eType,
    'name': coolEvent.name, 
    'description': coolEvent.description, 
    'host': coolEvent.host
    })

conn.commit()

cursor.execute("SELECT * FROM events")

print(cursor.fetchall())

conn.commit()

conn.close()