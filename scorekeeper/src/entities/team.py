from entities.player import Player


class Team:

    def __init__(self, name):
        self.name = name
        self.players = []
        self.points = 0

    def add_player(self, player: Player):
        self.players.append(Player)

    def get_players(self):
        return self.players
