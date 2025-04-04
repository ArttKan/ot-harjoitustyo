from entities.event import Event
from entities.team import Team


class ScoreService:
    def __init__(self):
        self.user = None
        self.events = []
        self.teams = []

    def add_event(self, content, type):
        event = Event(type, content=content, user=self.user)
        self.events.append(event)

    def get_events(self):
        return self.events

    def add_team(self, team: Team):
        self.teams.append(team)

    def get_teams(self, team):
        return self.teams
