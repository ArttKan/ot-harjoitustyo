import uuid


class Event:

    def __init__(self, type, content, user=None):
        self.content = content
        self.type = type
        self.user = user
        self.event_id = uuid.uuid4()
