# -*- coding: utf-8 -*-
from . import cluestatics
from . import clueboard
from .misc import random_integer


class IllegalGuess(BaseException):
    pass


class IllegalCommand(BaseException):
    pass


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
        self._answer = None
    
    def get_answer(self):
        return self._answer
    
    def get_answering_player(self):
        return self._guess_order[0]

    def all_players_passed(self):
        return len(self._guess_order) == 0

    def register_answer(self, answer):
        if answer is None:
            self._guess_order.pop(0)
            return
        if (answer != self._killer and answer != self._weapon
                and answer != self._scene):
            raise(ValueError(u"'{0:s}' not in guessed objects.".format(
                answer
            )))
        self._answer = answer


class Game:
    def __init__(self):
        layout = cluestatics.BOARD
        connected = cluestatics.CONNECTED_TILES
        board = clueboard.MovementBoard(layout, connected)
        mobs = [(itm[0], itm[1]) for itm in cluestatics.CHARACTERS]
        self._gameboard = clueboard.Gameboard(board, mobs)
        self._player = []
        self._dice = (0, 0)
        self._active_move = u""
        self._last_move = u""
        self._active_player = u""
        self._guess = None
    
    def get_available_characters(self):
        playing_characters = [itm[1] for itm in self._player]
        return [name for name in cluestatics.get_character_names()
                if name not in playing_characters]

    def add_player(self, playername, charactername):
        if charactername not in self.get_available_characters():
            raise ValueError(u"Character '{0:s}' not allowed or already taken.".format(
                charactername
            ))
        if playername in [itm[0] for itm in self._player]:
            raise ValueError(u"Player name '{0:s}' already taken".format(
                playername
            ))
        self._player.append((playername, charactername))
    
    def start_game(self):
        self._active_player = self._player[0][0]
        self.prepare_move()

    def roll_dice(self):
        self._dice = (random_integer(5) + 1, random_integer(5) + 1)
    
    def prepare_move(self):
        self._active_move = u"move"
        self.roll_dice()
        self.set_number_of_moves_for_active_player(
            self._dice[0] + self._dice[1])
    
    def move(self, playername, direction):
        if playername != self._active_player:
            return False
        res = self._gameboard.move_mob(
            self.get_active_mob(),
            direction)
        if self._gameboard.get_active_mob_name() == u"":
            self.finish_movement()
        return res

    def get_active_mob(self):
        return self.get_player_character(self._active_player)
    
    def set_number_of_moves_for_active_player(self, no):
        self._gameboard.set_active_mob(self.get_active_mob(), no)
    
    def get_player_character(self, playername):
        return [itm[1] for itm in self._player
                if itm[0] == playername][0]
    
    def finish_movement(self):
        self.finish_move()
    
    def finish_guess(self):
        self.finish_move()

    def finish_move(self):
        self._last_move = self._active_move
        self._active_move = u""
    
    def prepare_guess(self):
        if self._gameboard.is_in_hallway(self.get_active_mob()):
            self.finish_guess()
    
    def get_active_room(self):
        room_no = self._gameboard.get_room_no(self.get_active_mob())
        return [rm[0] for rm in cluestatics.ROOMS
                if rm[1] == room_no][0]

    def register_guess(self, playername, killer, room, weapon):
        if playername != self._active_player:
            raise(IllegalGuess(u"Player '{0:s}' is not active.".format(
                playername)))
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
        player = [itm[0] for itm in self._player]
        idx = player.index(self._active_player)
        order = player[:idx] + player[idx+1:]
        self._guess = Guess(killer, weapon, room, order)
        
    def prepare_answer(self):
        self._active_move = u"answer"
        
    def register_answer(self, answer):
        if self._active_move != u"answer":
            raise(IllegalCommand())
        self._guess.register_answer(answer)

