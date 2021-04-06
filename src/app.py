from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# flask config end

import threading
import time
import os

import gen
from lobby import Lobby
from events import *

lobbies = []

INACTIVE_PLAYER_LIMIT = 20
EMPTY_LOBBY_LIMIT = 20

PICTURES_DIR = 'pictures/'

def inactivityKiller():
    while True:
        time.sleep(EMPTY_LOBBY_LIMIT)
        
        i = 0
        for lobby in lobbies:
            for j in range(len(lobby.players)):
                if lobby.players[j].lastSeen < time.time() - INACTIVE_PLAYER_LIMIT: # If player didnt report being alive for INACTIVE_PLAYER_LIMIT destroy him
                    lobby.pushEvent(PlayerLeftEvent(lobby.players[j]))
                    print("Player {} ({}) was exterminated due to lack of activity".format(lobby.players[j].id, lobby.players[j].nick))
                    lobby.players.pop(j)

            if not len(lobby.players):
                print('Lobby {} was killed due to lack of players.'.format(lobby.id))
                lobbies.pop(i)
                break
            print('Lobby {} is still alive with {} players'.format(lobby.id, len(lobby.players)))

            i+=1

threading.Thread(target=inactivityKiller, daemon=True).start()

def auth(lobbyId, token):
    for lobby in lobbies:
        if lobby.id == lobbyId:
            for player in lobby.players:
                if player.token == token:
                    return lobby, player
            raise Exception("Matching token not found in this lobby")
    raise Exception("Lobby not found")

# --------------- NEW LOBBY ----------------- #
@app.route('/api/newLobby', methods=['GET'])
def newLobby():
    newLobby = Lobby()
    lobbies.append(newLobby)
    return jsonify({'success': True, 'lobbyId': newLobby.id})

# --------------- JOIN LOBBY ----------------- #
@app.route('/api/joinLobby/<lobbyId>/<nick>', methods=['GET'])
def joinLobby(lobbyId, nick):
    for lobby in lobbies:
        if lobby.id == lobbyId:
            player = lobby.joinPlayer(nick)
            return jsonify({
                'success': True,
                'id': player.id,
                'token': player.token,
                'nick': player.nick,
                'isOwner': player.isOwner
            })
    return jsonify({'success': False, 'description': 'Lobby not found'})

# --------------- FETCH EVENTS ----------------- #
@app.route('/api/fetchEvents/<lobbyId>/<token>', methods=['GET'])
def fetchEvents(lobbyId, token):
    try:
        lobby, player = auth(lobbyId, token)
    except Exception as e:
        return jsonify({
            'success': False,
            'description': e.args[0]
        })

    res = []
    for event in player.pendingEvents:
        res.append(event.dict)
    player.pendingEvents = [] # Reset pending events
    return jsonify(res)

# --------------- HEART BEAT ----------------- #
@app.route('/api/iAmAlive/<lobbyId>/<token>', methods=['GET'])
def heartbeat(lobbyId, token):
    try:
        lobby, player = auth(lobbyId, token)
    except Exception as e:
        return jsonify({
            'success': False,
            'description': e.args[0]
        })
    player.lastSeen = time.time()
    return jsonify({'success': True})

# --------------- CHANGE TEAM ----------------- #
@app.route('/api/changeTeam/<lobbyId>/<token>', methods=['GET'])
def changeTeam(lobbyId, token):
    try:
        lobby, player = auth(lobbyId, token)
    except Exception as e:
        return jsonify({
            'success': False,
            'description': e.args[0]
        })

    player.switchTeam()

    return jsonify({'success': True})

# --------------- CHANGE SETTING ------------- #
@app.route('/api/changeSetting/<lobbyId>/<setting>/<value>/<token>', methods=['GET'])
def changeSetting(lobbyId, setting, value, token):
    try:
        lobby, player = auth(lobbyId, token)
    except Exception as e:
        return jsonify({
            'success': False,
            'description': e.args[0]
        })

    if player.isOwner:
        if lobby.changeSetting(setting, value): # lobby.changeSetting returns True if changes will be aplied
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})

# --------------- START GAME ------------- #
@app.route('/api/startGame/<lobbyId>/<token>', methods=['GET'])
def startGame(lobbyId, token):
    try:
        lobby, player = auth(lobbyId, token)
    except Exception as e:
        return jsonify({
            'success': False,
            'description': e.args[0]
        })

    if not player.isOwner:
        return jsonify({'success': False})
    
    lobby.nextState()
    return jsonify({'success': True})

# --------------- NEW PICTURE ------------- #
@app.route('/api/newPicture/<lobbyId>/<token>', methods=['POST'])
def newPicture(lobbyId, token):
    try:
        lobby, player = auth(lobbyId, token)
    except Exception as e:
        return jsonify({
            'success': False,
            'description': e.args[0]
        })

    try:
        f = request.files['file']
        filename = '{}.jpg'.format(gen.genId())
        absPath = os.path.join(PICTURES_DIR, filename)
        f.save(absPath)
    except:
        return jsonify({'success': False})

    if lobby.newPicture(player, absPath):
        return jsonify({'success': True})
    else:
        if os.path.exists(absPath):
            os.remove(absPath)
        return jsonify({'success': False})


# --------------- SOLVE PICTURE ------------- #
@app.route('/api/solvePicture/<lobbyId>/<pictureId>/<token>', methods=['GET'])
def solvePicture(lobbyId, token):
    try:
        lobby, player = auth(lobbyId, token)
    except Exception as e:
        return jsonify({
            'success': False,
            'description': e.args[0]
        })

    for picture in lobby.pictures:
        if picture.id == pictureId:
            if lobby.solvePicture(picture, player):
                return jsonify({'success': True})
            return jsonify({'success': False})

    return jsonify({'success': False})

# --------------- GET PICTURE ------------- #
@app.route('/api/getPicture/<lobbyId>/<pictureId>/<token>', methods=['GET'])
def getPicture(lobbyId, token):
    try:
        lobby, player = auth(lobbyId, token)
    except Exception as e:
        return jsonify({
            'success': False,
            'description': e.args[0]
        })

    for picture in lobby.pictures:
        if picture.id == pictureId:
            return send_file(picture.open())
    abort(404)
            

# start flask

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='444', ssl_context=('cert.pem', 'key.pem'))