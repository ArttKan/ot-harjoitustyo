import itertools


class Team:

    id_iter = itertools.count()

    def __init__(self, name):
        self._name = name
        self._id = next(self.id_iter)
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
