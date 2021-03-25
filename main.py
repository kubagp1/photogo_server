import json

from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from lobby import Lobby

lobbies = []

@app.route('/api/newLobby/<ownerNickname>')
def newLobby(ownerNickname):
    if not len(ownerNickname):
        res = {'created': False}
    else:
        lobby = Lobby(ownerNickname)
        lobbies.append(lobby)
        res = {
            'created': True,
            'id': lobby.id,
            'ownerToken': lobby.owner.token,
            'ownerId': lobby.owner.id,
            'ownerNickname': lobby.owner.nicknname
        }
    return json.dumps(res)

@app.route('/api/joinLobby/<lobbyId>/<nickname>')
def joinLobby(lobbyId, nickname):
    for lobby in lobbies:
        if lobby.id == lobbyId:
            player = lobby.addPlayer(nickname)
            res = {
                'success': True,
                'token': player.token,
                'id': player.id,
                'nickname': player.nicknname
            }
            return json.dumps(res)
    return json.dumps({'success': False})

@app.route('/api/playerList/<lobbyId>/<token>')
def playerList(lobbyId, token):
    for lobby in lobbies:
        if lobby.id == lobbyId:
            for player in lobby.players:
                if player.token == token:
                    players = list()
                    for player in lobby.players:
                        players.append({
                            'nickname': player.nicknname,
                            'team': 'a'
                        })
                    res = {
                        'success': True,
                        'players': players
                    }
                    return json.dumps(res)
    return json.dumps({'success': False})

app.run(host='0.0.0.0', port=91, ssl_context='adhoc')