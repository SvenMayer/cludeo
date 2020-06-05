import eventlet
eventlet.monkey_patch()

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), u"..")))

from flask import Flask, request, session, render_template, abort, Response
from flask_socketio import SocketIO, join_room, emit, send
import json
import uuid

from clue.cluelogic import Game
import gui.guimisc as guimisc
import clue.cluestatics as cluestatics

app = Flask(__name__, template_folder = "templates")
app.config[u"SECRET_KEY"] = 'mysecret' 
#app.config[u"SESSION_COOKIE_SECURE"] = True # only send cookie for ssl connection.
app.config[u"SESSION_COOKIE_HTTPONLY"] = True
app.config[u"SESSION_COOKIE_SAMESITE"] = u"Strict"
socketio = SocketIO(app, cookie=None)
game = Game()
player = {}
comm = {}
id_rsid = {}


CERT_FILE = u"/etc/letsencrypt/live/clue-19.spdns.org/cert.pem"
KEY_FILE = u"/etc/letsencrypt/live/clue-19.spdns.org/privkey.pem"


def resolve_playername_send_update(func):
    def wrapper(*args, **kwargs):
        try:
            playername = player[request.sid]
        except KeyError:
            return
        res = func(playername, *args, **kwargs)
        send_status(True)
        return res
    return wrapper


@app.route('/')
def index():
    if "id" not in session:
        print("id created")
        session["id"] = uuid.uuid4().hex
        session.modified = True
    print(session["id"])
    return app.send_static_file(u"index.html")

@app.route('/style.css')
def stylesheet():
    return app.send_static_file(u"style.css")

@app.route("/js/cluecomm.js")
def js_files():
    data = {
        u"passcard_path": guimisc.PASSCARD_PATH,
        u"gamecards": [(itm, guimisc.get_object_media_path(itm))
                       for itm in cluestatics.get_character_names() + 
                                  cluestatics.get_room_card_names() +
                                  cluestatics.get_weapon_names()]
    }
    js = render_template(u"cluecomm.js", **data)
    return Response(js, mimetype=u"text/javascript")

@app.route("/media/<path:path>")
def media_files(path):
    return app.send_static_file("media/" + path)

@app.route("/lobby/")
def lobby():
    return app.send_static_file("lobby.html")

@app.route("/gamepanel/")
def gamepanel():
    try:
        rsid = id_rsid[session[u"id"]]
        myplayer = player[rsid]
    except KeyError:
        return abort(404)
    player_cards = [(card, guimisc.get_object_media_path(card))
                    for card in game.get_player(player[rsid]).get_objects()]
    res = render_template("game.html",
                           playername=myplayer,
                           mycards=player_cards)
    return Response(res, mimetype=u"text/html")


@app.route("/js/gameboard.js")
def gameboard_js():
    gameboard_dict = {
        u"gameboard": guimisc.get_object_media_path(u"gameboard"),
        u"mobs": [(name, guimisc.get_mob_media_path(name))
                  for name in cluestatics.get_character_names()]
    }
    js = render_template("gameboard.js", **gameboard_dict)
    return Response(js, mimetype=u"text/javascript")


@app.route(u"/guess/")
def handle_guess_panel():
    try:
        rsid = id_rsid[session[u"id"]]
        myplayer = player[rsid]
    except KeyError:
        return abort(404)
    # Check if player is currently in the guess phase
    if (game.get_active_player() != myplayer
            or game.get_active_move() != u"guess"):
        return abort(404)
    return render_template("guess.html", **get_guess_dict())


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
    #try:
    game.add_player(playerinfo[u"playername"], playerinfo[u"charactername"])
    playername = playerinfo[u"playername"]
    player[request.sid] = playername
    comm[playername] = request.sid
    #except:
    #    emit(u"game_status", u"lobby")
    #    return
    emit(u"game_status", u"waiting_to_start_game")
    emit(u"update_game_lobby", get_lobby_state(), broadcast=True)


@socketio.on(u"start_game")
def handle_start_game():
    game.start_game()
    emit(u"game_status", u"game_started", broadcast=True)


@socketio.on(u"move")
@resolve_playername_send_update
def handle_move(playername, direction):
    game.move(playername, direction)


@socketio.on(u"guess")
@resolve_playername_send_update
def handle_guess(playername, msg):
    killer, weapon, room = json.loads(msg)
    game.register_guess(playername, killer, room, weapon)


@socketio.on(u"answer")
def handle_answer(msg):
    if msg == "pass":
        answer = None
    else:
        answer = msg
    game.register_answer(answer)
    send_answer_update()
    #ToDo: register_answer needs to check playername


@socketio.on(u"answer_received")
@resolve_playername_send_update
def handle_get_answer(playername):
    game.get_answer()


@socketio.on(u"accuse")
@resolve_playername_send_update
def handel_accuseation(playername, msg):
    killer, weapon, room = json.loads(msg)
    game.register_accusation(playername, killer, weapon, room)


@socketio.on(u"refresh_gamestatus")
def handle_refresh_gamestatus():
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
    rooms = [game.get_active_room()]
    return {u"killers": killers,
            u"weapons": weapons,
            u"rooms": rooms}


def send_status(broadcast=False):
    emit(u"update_status", json.dumps(get_status()), broadcast=broadcast)


def get_status():
    mobpos = game.get_gameboard().todict()
    guess = game.get_guess()
    if guess is not None:
        guess = guess.todict()
    dice = game.get_dice()
    gamepanel = {u"mobpos": mobpos,
                 u"dice": dice,
                 u"active_player": game.get_active_player(),
                 u"active_move": game.get_active_move(),
                 u"guess": guess}
    return gamepanel


def send_answer_update():
    status = get_status()
    act_rsid = comm[status[u"active_player"]]
    emit(u"update_status", json.dumps(status), room=act_rsid)
    status[u"guess"][u"answer"] = None
    emit(u"update_status", json.dumps(status), broadcast=True, skip_sid=act_rsid)
    


if __name__ == u"__main__":
    print(u"Sven started")
    socketio.run(app, host="0.0.0.0", port=80)#, certfile=CERT_FILE, keyfile=KEY_FILE)
