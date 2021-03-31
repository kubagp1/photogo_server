class NewPlayerEvent:
    def __init__(self, player):
        self.type = 'newPlayer'
        self.player = {
            'id': player.id,
            'nick': player.nick,
            'team': player.team
        }

        self.dict = {
            'type': self.type,
            'player': self.player
        }

class PlayerLeftEvent:
    def __init__(self, player):
        self.type = 'playerLeft'
        self.playerId = player.id
        self.dict = {
            'type': self.type,
            'playerId': self.playerId
        }

class PlayerSwitchedTeamEvent:
    def __init__(self, player):
        self.type = 'playerSwitchedTeam'
        self.playerId = player.id
        self.dict = {
            'type': self.type,
            'playerId': self.playerId
        }

class LobbySettingChangedEvent:
    def __init__(self, setting, newValue):
        self.type = 'lobbySettingChanged'
        self.setting = setting
        self.newValue = newValue
        self.dict = {
            'type': self.type,
            'setting': self.setting,
            'newValue': self.newValue
        }

class NewLobbyStateEvent:
    def __init__(self, newState):
        self.type = 'newLobbyState'
        self.newState = newState
        self.dict = {
            'type': self.type,
            'newState': self.newState
        }

class NewPictureEvent:
    def __init__(self, picture):
        self.type = 'newPicture'
        self.pictureId = picture.id
        self.dict = {
            'type': self.type,
            'pictureId': self.pictureId
        }

class PictureSolvedEvent:
    def __init__(self, picture):
        self.type = 'pictureSolved'
        self.pictureId = picture.id
        self.dict = {
            'type': self.type,
            'pictureId': self.pictureId
        }