import uuid


class Event:
    def __init__(self, event_type, content, user=None):
        self.type = event_type
        self.content = content
        self.user = user
        self.event_id = uuid.uuid4()


class FoulEvent(Event):
    def __init__(self, content, user=None, player_name=None):
        super().__init__("Foul", content, user)
        if not player_name:
            raise ValueError("Player name is required for a Foul event")
        self.player_name = player_name


class TechnicalFoulEvent(Event):
    def __init__(self, content, user=None, player_name=None):
        super().__init__("Technical Foul", content, user)
        if not player_name:
            raise ValueError(
                "Player name is required for a Technical Foul event")
        self.player_name = player_name


class ThreePointEvent(Event):
    def __init__(self, content, user=None, player_name=None):
        super().__init__("Technical Foul", content, user)
        if not player_name:
            raise ValueError("Player name is required for a 3-Point event")
        self.player_name = player_name


class TwoPointEvent(Event):
    def __init__(self, content, user=None, player_name=None):
        super().__init__("Technical Foul", content, user)
        if not player_name:
            raise ValueError("Player name is required for a 2-Point event")
        self.player_name = player_name


class ReboundEvent(Event):
    def __init__(self, content, user=None, player_name=None):
        super().__init__("Technical Foul", content, user)
        if not player_name:
            raise ValueError("Player name is required for a Rebound event")
        self.player_name = player_name
