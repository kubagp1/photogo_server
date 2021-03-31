import gen
from player import Player
from events import *
from picture import Picture

import threading, time

class Lobby:
    def __init__(self):
        self.id = gen.genId()
        self.state = 'waiting'
        self.settings = {
            'secondPhaseTimeout': 2400, # In seconds
            'photosPerTeam': 10,
            'firstPhasePreview': True, # Determines if team A can see teams B pictures during first phase and vice-versa
            'secondPhasePreview': True # Determines if team A can see teams B pictures during second phase and vice-versa
        }
        self.players = []
        self.pictures = []

    def joinPlayer(self, nick):
        if not len(self.players):
            isOwner = True
            team = 'a'
        else:
            isOwner = False
            if len(self.players)%2: # This is to make players team auto swaps like that A B A B A ...
                team = 'b'

        newPlayer = Player(self, nick, team, isOwner)

        self.pushEvent(NewPlayerEvent(newPlayer)) # Push event for other players

        self.players.append(newPlayer)

        for player in self.players: # Push all players to new player as events
            newPlayer.pendingEvents.append(NewPlayerEvent(player))

        return newPlayer

    def pushEvent(self, event):
        for player in self.players:
            player.pendingEvents.append(event)

    def changeSetting(self, setting, value):
        if setting not in self.settings:
            return False
        if type(self.settings[setting]) != type(value): # Checks e.g if you are trying to set time to string based on old (predefined) value
            return False

        self.settings[setting] = value
        self.pushEvent(LobbySettingChangedEvent(setting, newValue))
        return True

    def phase2timeLimiter(self):
        self.phase2end = time.time() + self.settings['secondPhaseTimeout']
        while time.time() <= phase2end:
            time.sleep(1)
            if self.state != 'phase2':
                break
        if self.state == 'phase2':
            self.nextState()

    def nextState(self):
        if self.state == 'waiting':
            self.state = 'phase1'
        elif self.state == 'phase1':
            self.state = 'phase2'
            threading.Thread(target=self.phase2timeLimiter).start()
        elif self.state == 'phase2':
            self.state = 'summary'

        self.pushEvent(NewLobbyStateEvent(self.state))

    def newPicture(self, player, absPath):
        if self.state != 'phase1':
            return False

        if len(filter(lambda a: True if a.team == player.team else False, self.pictures)) + 1 <= self.settings['photosPerTeam']: # If picture limit haven't been reached yet.
            picture = Picture(absPath, player.team)
            self.pictures.append(picture)
            self.pushEvent(NewPictureEvent(picture))
            if len(self.pictures) >= self.settings['photosPerTeam'] * 2:
                self.nextState()
            return True
        else:
            return False

    def solvePicture(self, picture, player):
        if picture.team == player.team or self.state != 'phase2':
            return False
        picture.solved = True
        self.pushEvent(PictureSolvedEvent(picture))

        allSolved = True
        for picture in self.pictures:
            if not picture.solved:
                allSolved = False
                break
        if allSolved:
            self.nextState()
        return True