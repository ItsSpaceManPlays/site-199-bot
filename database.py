import sqlite3
from event import Event

db_conn = sqlite3.connect("events.db")
cursor = db_conn.cursor()

def insert_event(event: Event):
    with db_conn:
        cursor.execute("INSERT INTO events (type, name, description, hostid) VALUES (:type, :name, :description, :host)", {
            'type': event.eType,
            'name': event.name,
            'description': event.description,
            'host': event.host
        })

def remove_event(event: Event):
    with db_conn:
        cursor.execute("DELETE FROM events WHERE type = :type AND name = :name AND description = :description AND hostid = :host", {
            'type': event.eType,
            'name': event.name,
            'description': event.description,
            'host': event.host
        })

def update_description(event: Event, newDescription: str):
    with db_conn:
        cursor.execute("UPDATE events SET description = :description WHERE type = :type AND name = :name AND hostid = :host", {
            'type': event.eType,
            'name': event.name,
            'description': newDescription,
            'host': event.host
        })
    
def get_all_events_by_name(eventName: str):
    cursor.execute("SELECT * FROM events WHERE name = :name", {'name': eventName})
    return cursor.fetchall()

def get_event_by_id(id: int):
    cursor.execute("SELECT * FROM events WHERE ID = :id", {'id': id})
    return cursor.fetchone()

def get_all_events():
    cursor.execute("SELECT * FROM events")
    return cursor.fetchall()