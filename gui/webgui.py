import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), u"..")))

from flask import Flask, request, session, render_template, abort
from flask_socketio import SocketIO, join_room, emit, send
import json
import uuid

from clue.cluelogic import Game
import gui.guimisc as guimisc
import clue.cluestatics as cluestatics

app = Flask(__name__, template_folder = "templates")
app.config['SECRET_KEY'] = 'mysecret' 
socketio = SocketIO(app)
game = Game()
player = {}
comm = {}
id_rsid = {}


def resolve_playername_send_update(func):
    def wrapper(msg):
        playername = player[request.sid]
        res = func(playername, msg)
        send_status()
        return res()
    return wrapper


@app.route('/')
def index():
    if "id" not in session:
        print("id created")
        session["id"] = uuid.uuid4().hex
        session.modified = True
    print(session["id"])
    return app.send_static_file("index.html")

@app.route('/<path:path>')
def mainpage(path):
    if "id" not in session:
        print("id created")
        session["id"] = uuid.uuid4().hex
        session.modified = True
    print(session["id"])
    return app.send_static_file(path)

@app.route("/js/<path:path>")
def js_files(path):
    return app.send_static_file(path)

@app.route("/media/<path:path>")
def media_files(path):
    return app.send_static_file("media/" + path)

@app.route("/lobby/")
def lobby():
    return app.send_static_file("lobby.xml")

@app.route("/gamepanel/")
def gamepanel():
    try:
        rsid = id_rsid[session[u"id"]]
        myplayer = player[rsid]
    except KeyError:
        return abort(404)
    player_cards = [(card, guimisc.get_object_media_path(card))
                    for card in game.get_player(player[rsid]).get_objects()]
    return render_template("game.xml", playername=myplayer,
                           mycards=player_cards)

@app.route(u"/guess/")
def handle_guess():
    try:
        rsid = id_rsid[session[u"id"]]
        myplayer = player[rsid]
    except KeyError:
        return abort(404)
    return render_template("guess.xml", **get_guess_dict())


# Websockets
@socketio.on(u"joined")
def handle_joined():
    if session["id"] in id_rsid:
        old_rsid = id_rsid[session["id"]]
        if old_rsid in player:
            player[request.sid] = player[old_rsid]
            comm[player.pop(old_rsid)] = request.sid
    id_rsid[session["id"]] = request.sid
    if request.sid not in player:
        emit(u"game_status", u"lobby")
    else:
        emit(u"game_status", u"waiting_to_start_game")
    
@socketio.on(u"refresh_game_lobby")
def handle_refresh_game_lobby():
    emit(u"update_game_lobby", get_lobby_state())

@socketio.on(u"join_game")
def handle_join_game(msg):
    playerinfo = json.loads(msg)
    try:
        game.add_player(playerinfo[u"playername"], playerinfo[u"charactername"])
        playername = playerinfo[u"playername"]
        player[request.sid] = playername
        comm[playername] = request.sid
    except:
        emit(u"game_status", u"lobby")
        return
    emit(u"game_status", u"waiting_to_start_game")
    emit(u"update_game_lobby", get_lobby_state(), broadcast=True)

@socketio.on(u"start_game")
def handle_start_game():
    game.start_game()
    emit(u"game_started", broadcast=True)


@socketio.on(u"move")
@resolve_playername_send_update
def handle_move(playername, direction):
    game.move(playername, direction)


@socketio.on(u"guess")
@resolve_playername_send_update
def handle_guess(playername, msg):
    killer, weapon, room = json.loads(msg)
    game.register_guess(playername, killer, weapon, room)

@socketio.on(u"answer")
@resolve_playername_send_update
def handle_answer(playername, msg):
    game.register_answer(playername, json.loads(msg))

@socketio.on(u"accuse")
@resolve_playername_send_update
def handel_accuseation(playername, msg):
    killer, weapon, room = json.loads(msg)
    game.register_accusation(playername, killer, weapon, room)

@socketio.on(u"refresh_gamestatus")
def handle_refresh_gamestatus(msg):
    send_status()

def get_lobby_state():
    joined_players = [[pl, game.get_player_character(pl)] for pl in game.get_players()]
    lobby_info = {
        u"joind_players": joined_players,
        u"available_characters": game.get_available_characters(),
    }
    return json.dumps(lobby_info)


def get_guess_dict():
    killers = cluestatics.get_character_names()
    weapons = cluestatics.get_weapon_names()
    rooms = game.get_active_room()
    return {u"killers": killers,
            u"weapons": weapons,
            u"rooms": rooms}


def send_status(broadcast=False):
    mobpos = game.get_gameboard.todict()
    guess = game.get_guess()
    if guess is not None:
        guess = guess.todict()
    dice = game.get_dice()
    gamepanel = {u"mobpos": mobpos,
                 u"dice": dice,
                 u"active_player": game.get_active_player(),
                 u"active_move": game.get_active_move(),
                 u"guess": guess}
    emit(u"update_status", json.dumps(gamepanel), broadcast=broadcast)


if __name__ == u"__main__":
    print(u"Sven started")
    socketio.run(app, debug=True)