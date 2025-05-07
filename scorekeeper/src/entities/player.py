class Player:
    """Class representing a basketball player."""

    def __init__(self, name, number, player_id=None):
        """Initialize a new player.

        Args:
            name (str): Player name
            number (int): Jersey number
            player_id (int, optional): Player ID from database
        """
        self._name = name
        self._number = number
        self._id = player_id

    @property
    def name(self):
        """Get player name."""
        return self._name

    @property
    def number(self):
        """Get player number."""
        return self._number

    @property
    def id(self):
        """Get player ID."""
        return self._id

    def __str__(self):
        """String representation of the player."""
        return f"{self._number} {self._name}"
