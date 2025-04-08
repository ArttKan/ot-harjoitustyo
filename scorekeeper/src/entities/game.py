
class Game:

    def __init__(self):
        self.home_team = None
        self.away_team = None

    def add_home_team(self, home_team):
        self.home_team = home_team

    def add_away_team(self, away_team):
        self.away_team = away_team

    def get_teams(self):
        away_team = None
        if self.away_team:
            away_team = self.away_team.name
        return [self.home_team.name, away_team]
