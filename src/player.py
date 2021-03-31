import gen
import time
from events import *

class Player:
    def __init__(self, lobby, nick, team, isOwner=False):
        self.lobby = lobby
        self.id = gen.genId()
        self.token = gen.genToken()
        self.nick = nick
        self.isOwner = isOwner
        self.team = 'a'
        self.pendingEvents = []
        self.lastSeen = time.time()

    def switchTeam(self):
        self.team = 'a' if self.team == 'b' else 'b'
        self.lobby.pushEvent(PlayerSwitchedTeamEvent(self))