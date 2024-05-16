import json

DATABASE_FILE = open("data/db.json", "w+")

DATA = json.load(DATABASE_FILE)
EVENTS = DATA["events"]

def update_data():
    json.dump(DATABASE_FILE, DATABASE_FILE, indent=4)

def get_all_ssu_events():
    return EVENTS["ssu"]

def get_all_ssd_events():
    return EVENTS["ssd"]

def create_event(eventType: str, eventData):
    if eventType == "ssu":
        EVENTS["ssu"].append(eventData)
    if eventType == "ssd":
        EVENTS["ssd"].append(eventData)

    update_data()