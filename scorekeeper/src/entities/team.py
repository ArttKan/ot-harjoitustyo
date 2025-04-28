from entities.player import Player


class Team:

    def __init__(self, name, team_id=None):
        self._name = name
        self._id = team_id
        self._players = []

    @property
    def name(self):
        """Get team name."""
        return self._name

    @property
    def id(self):
        """Get team ID."""
        return self._id

    def add_player(self, player):
        """Add a player to the team."""
        self._players.append(player)

    def get_players(self):
        """Get all players in the team."""
        return self._players