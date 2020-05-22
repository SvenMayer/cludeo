# -*- coding: utf-8 -*-
from . import cluestatics
from . import clueboard
from .misc import random_integer


class IllegalGuess(BaseException):
    pass


class IllegalCommand(BaseException):
    pass


def plausibility_check_active_playername(func):
    def wrapper(self, *args, **kwargs):
        if u"playername" in kwargs:
            playername = kwargs[u"playername"]
        else:
            playername = args[0]
        if playername != self._active_player:
            raise(IllegalCommand(
                u"Player '{0:s}' is not the active player".format(playername)))
        return func(self, *args, **kwargs)
    return wrapper


class Player:
    def __init__(self, player_name, character_name):
        self._player_name = player_name
        if character_name not in cluestatics.get_character_names():
            raise ValueError(u"Charactername {0:s} does not exist.".format(
                character_name))
        self._character_name = character_name
        self._objects = []
    
    def get_playername(self):
        return self._player_name
    
    def get_charactername(self):
        return self._character_name
    
    def set_objects(self, objects):
        all_objs = (cluestatics.get_character_names()
                    + cluestatics.get_room_names()
                    + cluestatics.get_weapon_names())
        for obj in objects:
            if obj not in all_objs:
                raise ValueError(u"'{0:s} not a valid Clue object".format(obj))
        self._objects = objects
    
    def get_objects(self):
        return self._objects
    
    def has_object(self, object):
        return object in self._objects
    

class Guess:
    def __init__(self, killer, weapon, scene, guess_order):
        if killer not in cluestatics.get_character_names():
            raise ValueError(u"'{0:s}' is not a valid clue character".format(
                killer))
        if weapon not in cluestatics.get_weapon_names():
            raise ValueError(u"'{0:s}' is not a valid clue weapon".format(
                weapon))
        if scene not in cluestatics.get_room_names():
            raise ValueError(u"'{0:s}' is not a valid clue room".format(
                scene))
        self._killer = killer
        self._weapon = weapon
        self._scene = scene
        self._guess_order = guess_order
        self._passed_players = []
        self._answer = None
    
    def get_answer(self):
        return self._answer
    
    def get_answering_player(self):
        if len(self._guess_order):
            return self._guess_order[0].get_playername()
        else:
            return u""

    def all_players_passed(self):
        return len(self._guess_order) == 0

    def register_answer(self, answer):
        if answer is None:
            self._passed_players.append(
                self._guess_order.pop(0).get_playername())
            return
        if (answer != self._killer and answer != self._weapon
                and answer != self._scene):
            raise(ValueError(u"'{0:s}' not in guessed objects.".format(
                answer
            )))
        if not self._guess_order[0].has_object(answer):
            raise(ValueError(
                u"Player '{0:s}' does not have card '{1:s}'".format(
                    self.get_answering_player(), answer
                )))
        self._answer = answer
    
    def get_passed_players(self):
        return self._passed_players


class Game:
    def __init__(self):
        layout = cluestatics.BOARD
        connected = cluestatics.CONNECTED_TILES
        board = clueboard.MovementBoard(layout, connected)
        mobs = [(itm[0], itm[1]) for itm in cluestatics.CHARACTERS]
        self._gameboard = clueboard.Gameboard(board, mobs)
        self._player = []
        self._inactive_players = []
        self._dice = (0, 0)
        self._active_move = u""
        self._last_move = u""
        self._active_player = u""
        self._guess = None
        self._gameobjects = None
        self._winning_player = u""
    
    def get_available_characters(self):
        playing_characters = [itm.get_charactername() for itm in self._player]
        return [name for name in cluestatics.get_character_names()
                if name not in playing_characters]

    def add_player(self, playername, charactername):
        if charactername not in self.get_available_characters():
            raise ValueError(u"Character '{0:s}' not allowed or already taken.".format(
                charactername
            ))
        if playername in self.get_players():
            raise ValueError(u"Player name '{0:s}' already taken".format(
                playername
            ))
        self._player.append(Player(playername, charactername))
    
    def start_game(self):
        self._active_player = self._player[0].get_playername()
        self.deal_object_cards()
        self.prepare_move()

    def roll_dice(self):
        self._dice = (random_integer(5) + 1, random_integer(5) + 1)
    
    def prepare_move(self):
        self._active_move = u"move"
        self.roll_dice()
        self.set_number_of_moves_for_active_player(
            self._dice[0] + self._dice[1])
    
    @plausibility_check_active_playername
    def move(self, playername, direction):
        res = self._gameboard.move_mob(
            self.get_active_mob(),
            direction)
        if self._gameboard.get_active_mob_name() == u"":
            self.next_step()
        return res

    def get_active_mob(self):
        return self.get_player_character(self._active_player)
    
    def set_number_of_moves_for_active_player(self, no):
        self._gameboard.set_active_mob(self.get_active_mob(), no)
    
    def get_player_character(self, playername):
        return [itm.get_charactername() for itm in self._player
                if itm.get_playername() == playername][0]
    
    def get_active_room(self):
        room_no = self._gameboard.get_room_no(self.get_active_mob())
        return [rm[0] for rm in cluestatics.ROOMS
                if rm[1] == room_no][0]

    @plausibility_check_active_playername
    def register_guess(self, playername, killer, room, weapon):
        if self.get_active_room() == u"hallway":
            raise(IllegalGuess(
                u"Player is in the hallway and cannot register a guess."))
        if self._active_move != u"guess":
            raise(IllegalGuess(
                u"Active phase is '{0:s}'; no guesses accepted.".format(
                    self._active_move
                )))
        if self.get_active_room() != room:
            raise(IllegalGuess(
                u"Player is in room '{0:s}' cannot register a guess in room '{1:s}'".format(
                    self.get_active_room(), room
                )))
        player = self.get_players()
        idx = player.index(self._active_player)
        order = self._player[:idx] + self._player[idx+1:]
        self._guess = Guess(killer, weapon, room, order)
        self.next_step()
    
    def register_answer(self, answer):
        if self._active_move != u"answer":
            raise(IllegalCommand())
        self._guess.register_answer(answer)
        if (self._guess.get_answer() is not None
                or self._guess.all_players_passed()):
            self.next_step()
 
    def next_step(self):
        if (self._active_move == u"move" 
                and not self._gameboard.is_in_hallway(self.get_active_mob())):
            self._active_move = u"guess"
        elif self._active_move == u"guess":
            self._active_move = u"answer"
        elif self._active_move == u"answer":
            self._active_move = u"read_answer"
        else:
            self._active_move = u"move"
            self._active_player = self.get_next_player()
            self.prepare_move()
    
    def get_next_player(self):
        idx = self.get_players().index(self._active_player)
        for i in range(1, len(self._player) + 1):
            idx_new = (idx + i) % len(self._player)
            new_player = self._player[idx_new].get_playername()
            if new_player not in self._inactive_players:
                break
        return new_player
    
    def get_answer(self):
        answer = self._guess.get_answer()
        self._guess = None
        self.next_step()
        return answer
    
    def get_passed_players(self):
        return self._guess.get_passed_players()
    
    def deactivate_player(self, playername):
        if playername not in self.get_active_players():
            raise(ValueError(u"Player '{0:s}' does not exist".format(
                playername)))
        self._inactive_players.append(playername)

    def get_players(self):
        return [itm.get_playername() for itm in self._player]
    
    def get_active_players(self):
        return [itm.get_playername() for itm in self._player
                if itm.get_playername() not in self._inactive_players]
    
    def deal_object_cards(self):
        characters = cluestatics.get_character_names()
        weapons = cluestatics.get_weapon_names()
        rooms = cluestatics.get_room_card_names()
        idx_killer = random_integer(len(characters) - 1)
        idx_weapon = random_integer(len(weapons) - 1)
        idx_room = random_integer(len(rooms) - 1)
        self._gameobjects = (
            characters.pop(idx_killer),
            weapons.pop(idx_weapon),
            rooms.pop(idx_room),
        )
        remaining_cards = characters + weapons + rooms
        for i, p in enumerate(self._player[::-1]):
            to_deal = len(remaining_cards) // (len(self._player) - i)
            cards = []
            for i in range(to_deal):
                cards.append(remaining_cards.pop(
                    random_integer(len(remaining_cards) - 1)))
            p.set_objects(cards)

    @plausibility_check_active_playername
    def register_accusation(self, playername, killer, weapon, room):
        if (killer, weapon, room) == self._gameobjects:
            self._winning_player = self._active_player
        else:
            self.deactivate_player(playername)
    
    def get_winning_player(self):
        return self._winning_player
    
    def gameover(self):
        return self.get_winning_player() != u""