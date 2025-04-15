from entities.team import Team


class ScoreService:
    def __init__(self):
        self.user = None
        self.events = []
        self.teams = []
        self.scores = {}  # Dictionary to track team scores

    def add_event(self, event):
        self.events.append(event)

        # Update score for scoring events
        if event.type == "2-Pointer":
            if event.team.name not in self.scores:
                self.scores[event.team.name] = 0
            self.scores[event.team.name] += 2
        elif event.type == "3-Pointer":
            if event.team.name not in self.scores:
                self.scores[event.team.name] = 0
            self.scores[event.team.name] += 3

    def get_events(self):
        return self.events

    def get_team_score(self, team_name):
        return self.scores.get(team_name, 0)

    def add_team(self, team: Team):
        self.teams.append(team)
        self.scores[team.name] = 0  # Initialize team score

    def get_teams(self):
        return self.teams
