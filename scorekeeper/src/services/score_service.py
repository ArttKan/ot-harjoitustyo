from entities.event import Event


class ScoreService:
    def __init__(self):
        self.user = None
        self.events = []

    def add_event(self, content, type):
        event = Event(type, content=content, user=self.user)
        self.events.append(event)

    def get_events(self):
        return self.events
