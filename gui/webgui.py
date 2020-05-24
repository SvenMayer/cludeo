import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), u"..")))

from flask import Flask, request
from flask_socketio import SocketIO, join_room, emit, send
import json

from clue.cluelogic import Game


app = Flask(__name__, template_folder = "templates")
socketio = SocketIO(app)
game = Game()
player = {}


@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route("/js/<path:path>")
def js_files(path):
    return app.send_static_file(path)

# Websockets
@socketio.on(u"joined")
def handle_joined():
    emit(u"game_status", u"lobby")
    emit(u"refresh_game_lobby", get_lobby_state())

@socketio.on(u"join_game")
def handle_join_game(msg):
    playerinfo = json.loads(msg)
    try:
        game.add_player(playerinfo[u"playername"], playerinfo[u"charactername"])
        player[request.sid] = playerinfo[u"playername"]
    except:
        emit(u"game_status", u"lobby")
        return
    print(player)
    emit(u"game_status", u"waiting_to_start_game")
    emit(u"refresh_game_lobby", get_lobby_state(), broadcast=True)

@socketio.on(u"start_game")
def handle_start_game():
    game.start_game()

def get_lobby_state():
    joined_players = [[pl, game.get_player_character(pl)] for pl in game.get_players()]
    lobby_info = {
        u"joind_players": joined_players,
        u"available_characters": game.get_available_characters(),
    }
    return json.dumps(lobby_info)

if __name__ == u"__main__":
    print(u"Sven started")
    socketio.run(app, debug=True)