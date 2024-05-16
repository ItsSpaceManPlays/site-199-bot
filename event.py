EVENT_SSU = "ssu"
EVENT_SSD = "ssd"

class Event():
    def __init__(self, eventName: str, eventDescription: str, hostId: int, eventType: str) -> None:
        self.name = eventName
        self.description = eventDescription
        self.host = hostId
        self.eType = eventType
    