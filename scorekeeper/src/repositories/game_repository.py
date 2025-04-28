class GameRepository:
    def __init__(self):
        self.current_game = None
        self.game_scores = {}  # {team_name: score}

    def start_new_game(self, game):
        """Start a new game."""
        self.current_game = game
        self.game_scores = {}
        return game

    def get_current_game(self):
        """Get the current game."""
        return self.current_game

    def update_score(self, team_name, points):
        """Update score for a team."""
        if team_name not in self.game_scores:
            self.game_scores[team_name] = 0
        self.game_scores[team_name] += points

    def get_score(self, team_name):
        """Get current score for a team."""
        return self.game_scores.get(team_name, 0)
