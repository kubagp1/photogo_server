import gen
from player import Player

class Lobby():
    def __init__(self, ownerNickname):
        self.players = list()
        self.players.append(Player(isOwner=True, nicknname=ownerNickname))
        self.owner = self.players[0]
        self.id = gen.genId()

    def addPlayer(self, nickname):
        for player in self.players:
            if player.nicknname == nickname:
                nickname += '_'
        player = Player(nickname)
        self.players.append(player)
        return player