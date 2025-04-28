class Game:
    """Class representing a basketball game."""

    def __init__(self, game_id=None):
        """Initialize a new game."""
        self._id = game_id
        self._home_team = None
        self._away_team = None

    @property
    def id(self):
        """Get game ID."""
        return self._id

    def add_team(self, team):
        """Add a team to the game."""
        if not self._home_team:
            self._home_team = team
            return True
        elif not self._away_team:
            self._away_team = team
            return True
        return False

    def get_teams(self):
        """Get both teams in the game.

        Returns:
            tuple: (home_team, away_team)
        """
        return (self._home_team, self._away_team)

    def get_home_team(self):
        """Get home team.

        Returns:
            Team: Home team
        """
        return self._home_team

    def get_away_team(self):
        """Get away team.

        Returns:
            Team: Away team
        """
        return self._away_team
