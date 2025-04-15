

class Event:
    def __init__(self, event_type, player, team):
        self.type = event_type
        self.player = player
        self.team = team


class FoulEvent(Event):
    def __init__(self, player, team):
        super().__init__("Foul", player, team)


class TechnicalFoulEvent(Event):
    def __init__(self, player, team):
        super().__init__("Technical Foul", player, team)


class ThreePointEvent(Event):
    def __init__(self, player, team):
        super().__init__("3-Pointer", player, team)


class TwoPointEvent(Event):
    def __init__(self, player, team):
        super().__init__("2-Pointer", player, team)


class ReboundEvent(Event):
    def __init__(self, player, team):
        super().__init__("Rebound", player, team)
