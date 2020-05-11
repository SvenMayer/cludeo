    # -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""
import exceptions
import random
import time


random.seed(time.clock())


class IllegalMove(exceptions.BaseException):
    pass


board = [
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   2,   2,   2,   2,   2,   2,   2,   1,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   2,   2,   2,   2,   2,   2,   2,   1,   1,   5,   3,   3,   3,   3,   5,   1,   1,   4,   4,   4,   4,   4,   4,   4,   0],
    [0,   2,   2,   2,   2,   2,   2,   2,   1,   1,   5,   3,   3,   3,   3,   5,   1,   1,   4,   4,   4,   4,   4,   4,   4,   0],
    [0, 202,   2,   2,   2,   2,   2, 102,   1,   1,   5,   3,   3,   3,   3,   5,   1,   1,   4,   4,   4,   4,   4,   4,   4,   0],
    [0,   0,   1,   1,   1,   1,   1, 101,   1, 101, 103,   3,   3,   3,   3,   5,   1,   1,   4,   4,   4,   4,   4,   4,   4,   0],
    [0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   5,   3,   3,   3,   3,   5,   1,   1, 103,   4,   4,   4,   4,   4, 204,   0],
    [0,   0,   5,   5,   5,   5,   5,   1,   1,   1,   5,   5, 103, 103,   5,   5,   1,   1, 101,   1,   1,   1,   1,   1,   0,   0],
    [0,   5,   5,   5,   5,   5,   5,   5,   1,   1,   1, 101, 101, 101,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0],
    [0,   5,   5,   5,   5,   5,   5, 105, 101,   1,   0, 106, 106, 106,   0,   1,   1,   1, 101,   1,   1,   1,   1,   1,   0,   0],
    [0,   5,   5,   5,   5,   5,   5,   5,   1,   1,   0,   6,   6,   6,   0,   1,   1,   0, 107,   0,   0,   0,   0,   0,   0,   0],
    [0,   0,   5,   5, 105,   5,   5,   1,   1,   1,   0,   6,   6,   6,   0,   1,   1,   0,   7,   7,   7,   7,   7,   7,   0,   0],
    [0,   0, 101,   1, 101,   1,   1,   1,   1,   1,   0,   6,   6,   6,   0,   1,   1,   0,   7,   7,   7,   7,   7,   7,   0,   0],
    [0,   0, 108,   0,   0,   0,   0,   1,   1,   1,   0,   0,   0,   0,   0,   1, 101, 107,   7,   7,   7,   7,   7,   7,   0,   0],
    [0,   0,   8,   8,   8,   8,   0,   1,   1,   1,   0,   0,   0,   0,   0,   1,   1,   0,   7,   7,   7,   7,   7,   7,   0,   0],
    [0,   0,   8,   8,   8,   8,   0,   1,   1,   1,   0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   0,   7,   7,   7,   0,   0],
    [0,   0,   8,   8,   8,   8, 108, 101,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   1,   1,   1, 101,   1,   1,   1,   1, 101,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0],
    [0,   0,   1,   1,   1,   1,   1,   1,   1,   0, 110,   0,   0,   0,   0, 110,   0,   1,   1,   1, 101,   1,   1,   1,   1,   0],
    [0,   1,   1,   1,   1,   1,   1,   1,   1,   0,  10,  10,  10,  10,  10,  10,   0,   1,   1,  11, 111,  11,  11,  11,   0,   0],
    [0,   0, 209,   9,   9, 109, 101,   1, 101, 110,  10,  10,  10,  10,  10,  10, 110, 101,   1,  11,  11,  11,  11,  11,   0,   0],
    [0,   9,   9,   9,   9,   9,   9,   1,   1,   0,  10,  10,  10,  10,  10,  10,   0,   1,   1,  11,  11,  11,  11,  11,   0,   0],
    [0,   9,   9,   9,   9,   9,   9,   1,   1,   0,  10,  10,  10,  10,  10,  10,   0,   1,   1,  11,  11,  11,  11,  11,   0,   0],
    [0,   9,   9,   9,   9,   9,   9,   1,   1,   0,   0,   0,  10,  10,   0,   0,   0,   1,   1,  11,  11,  11,  11,  11,   0,   0],
    [0,   9,   9,   9,   9,   9,   9,   0,   1,   1,   1,   0,  10,  10,   0,   1,   1,   1,   0, 211,  11,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
]
special_moves = {
    101: (102, 103, 104, 105, 106, 107, 108, 109, 110, 111),
    204: (209,),
    209: (204,),
    202: (211,),
    211: (202,),
        }
START_POS = [(1, 8), (1, 17), (6, 1), (19, 1), (26, 10), (26, 15), (8, 25), (18, 25)]


class GameBoard:
    def __init__(self, board, special_moves):
        self.board = board
        self.special_moves = special_moves
    
    def tile_no(self, pos):
        return self.board[pos[0]][pos[1]]

    def room_no(self, pos):
        tileno = self.tile_no(pos)
        return tileno % 100

    def move_allowed(self, oldpos, newpos):
        oldtile = self.tile_no(oldpos)
        newtile = self.tile_no(newpos)
        if oldtile == newtile:
            return True
        if (oldtile in self.special_moves.keys()
                and self.special_moves[oldtile] == newtile):
            return True
        return False

    def move_to(self, oldpos, newpos):
        if self.move_allowed(oldpos, newpos):
            return self.room_no(newpos), newpos
        else:
            raise(IllegalMove)
    
    def up(self, pos):
        newpos = (pos[0]-1, pos[1])
        return self.move_to(pos, newpos)
    
    def down(self, pos):
        newpos = (pos[0]+1, pos[1])
        return self.move_to(pos, newpos)
    
    def left(self, pos):
        newpos = (pos[0], pos[1]-1)
        return self.move_to(pos, newpos)
    
    def right(self, pos):
        newpos = (pos[0]-1, pos[1]+1)
        return self.move_to(pos, newpos)
    
    def special_move(self, pos):
        tileno = self.tile_no(pos)
        if tileno not in self.special_moves.keys():
            raise(IllegalMove())
        newtile = self.special_moves[tileno]
        for row in len(self.board):
            try:
                col = self.board[row].index(newtile)
                pos = row, col
                newroom = self.room_no(pos)
                return newroom, pos
            except ValueError:
                continue
        raise(IllegalMove())


class Player:
    def __init__(self, gameboard, name, startpos):
        self._pos = startpos
        self._gameboard = gameboard
        self._room = 1
        self._lastroom = 1
        self.name = name
        self._number_of_steps = 0
    
    def set_number_of_steps(self, number_of_steps):
        self._number_of_steps = number_of_steps
    
    def check_entered_room(self):
        if self._room != 1 and self._lastroom != self._room:
            self._number_of_steps = 0
    
    def get_number_of_steps(self):
        return self._number_of_steps
    
    def up(self):
        if self._number_of_steps <= 0:
            return False
        try:
            self._room, self._pos = self._gameboard.up(self._pos)
        except IllegalMove:
            return False
        self._number_of_steps -= 1
        self.check_entered_room()
        return True
    
    def down(self):
        if self._number_of_steps <= 0:
            return False
        try:
            self._room, self._pos = self._gameboard.down(self._pos)
        except IllegalMove:
            return False
        self._number_of_steps -= 1
        self.check_entered_room()
        return True
    
    def left(self):
        if self._number_of_steps <= 0:
            return False
        try:
            self._room, self._pos = self._gameboard.left(self._pos)
        except IllegalMove:
            return False
        self._number_of_steps -= 1
        self.check_entered_room()
        return True
    
    def right(self):
        if self._number_of_steps <= 0:
            return False
        try:
            self._room, self._pos = self._gameboard.right(self._pos)
        except IllegalMove:
            return False
        self._number_of_steps -= 1
        self.check_entered_room()
        return True

    def special(self):
        if self._number_of_steps <= 0:
            return False
        try:
            self._room, self._pos = self._gameboard.special_move(self._pos)
        except IllegalMove:
            return False
        self._number_of_steps -= 1
        self.check_entered_room()
        return True
    
    def get_pos(self):
        return self._pos


class RandomInteger:
    @staticmethod
    def generate(max_int):
        res = max_int + 1 
        while res > max_int:
            res = int(random.random() * max_int)
        return res


class Object:
    def __init__(self, name):
        if name in self.fulllist:
            self._name = name
        else:
            raise(ValueError())
    
    def get(self):
        return self._name
    

class Person(Object):
    fulllist = (u"Mrs. White", 
                u"Reverend Green",
                u"Mrs. Peacock",
                u"Prof. Plum",
                u"Miss Scarlett",
                u"Colonel Mustard",)
    def __init__(self, name):
        Object.__init__(self, name)


class Weapon(Object):
    fulllist = (u"dagger",
                u"candle stick",
                u"pipe",
                u"pistol",
                u"rope",
                u"crowbar",
                u"poison",)
    def __init__(self, name):
        Object.__init__(self, name)


class Room(Object):
    fulllist = (u"library",)
    def __init__(self, name):
        Object.__init__(self, name)


class Guess:
    def __init__(self, person_name=None, weapon_name=None, room_name=None):
        if person_name is not None:
            self._person = Person(person_name)
        else:
            self._person = None
        if weapon_name is not None:
            self._weapon = Weapon(weapon_name)
        else:
            self._weapon = None
        if room_name is not None:
            self._room = Room()
        else:
            self._room is None
        self._response = None
        
        self._querry_list = []
        self._querry_idx = -1
    
    def set_querry_list(self, querry_list):
        self._querry_id = 0
        self._querry_list = []
        
    def set_response(self, resp_name):
        try:
            self._response = Person(resp_name)
        except ValueError:
            self._response = Weapon(resp_name)
    
    def get_response(self):
        return self._response

    def get(self):
        if self._room is None or self._weapon is None or self._person is None:
            return None
        return {u"person": self._person.get(),
                u"weapon": self._weapon.get(),
                u"room": self._room.get()}


class Game:
    def __init__(self):
        self._gameboard = GameBoard(board, special_moves)
        self._availablestart_pos = [itm for itm in START_POS]
        self._players = {}
        self._play_order = []
        self._active_player = -1
        self._play_step = u""  # roll, move, guess, show
        self._die_values = (RandomInteger.generate(5) + 1,
                            RandomInteger.generate(5) + 1)
        self._guess = Guess()
    
    def _get_random_startpos(self):
        idx_sp = RandomInteger(len(self._availablestart_pos) - 1)
        return self._availablestart_pos.pop(idx_sp)

    def roll_die(self, player_name):
        if player_name != self.active_player_name():
            return False
        if self._play_step != u"roll":
            return False
        self._die_values = (RandomInteger.generate(5) + 1,
                            RandomInteger.generate(5) + 1)
        self.get_active_player().set_number_of_steps(
                self._die_values[0] + self._die_values[0])
        self.finish_step()
        return True
    
    def register_guess(self, player_name, room, weapon, person):
        if player_name != self.active_player_name():
            return False
        if self._play_step != u"guess":
            return False
        self._guess = Guess(person, weapon, room)
        self.finish_step()
        return True

    def start_game(self):
        self._play_order = self._players.keys()
        self._active_player = RandomInteger.generate(len(self._play_order) - 1)
        self._play_step = u"roll"
        
    def add_player(self, name):
        if self._active_player != -1:
            return False
        if len(self._availablestart_pos) == 0:
            return False
        self._players[name] = Player(
                self._gameboard, name, self._get_random_startpos())
        return True
    
    def active_player_name(self):
        return self._play_order[self._active_player]
    
    def get_active_player(self):
        return self._players[self.active_player_name()]

    def move_player(self, player_name, direction):
        if player_name != self.active_player_name():
            return False
        active_player = self.get_active_player()
        if direction == u"up":
            return active_player.up()
        elif direction == u"down":
            return active_player.down()
        elif direction == u"left":
            return active_player.left()
        elif direction == u"right":
            return active_player.right()
        elif direction == u"special":
            return active_player.special()
        else:
            return False
        if active_player.get_number_of_steps() <= 0:
            self.finish_step()
    
    def next_player(self):
        self._active_player += 1
        self._active_player %= len(self._play_order)
    
    def finish_step(self):
        active_player = self.get_active_player()
        if self._play_step == u"roll":
            self._play_step = u"move"
        elif self._play_step == u"move":
            active_player.set_number_of_steps(0)
            self._play_step = u"guess"
        elif self._play_step == u"guess":
            self._play_step = u"show"
        elif self._play_step == u"show":
            self._play_step = u"roll"
            self.next_player()
    
    def get_player_positions(self):
        return dict([(key, value.get_pos())
                     for key, value in self._players.iteritems()])
    
    def get_status(self):
        return {
            "step": self._play_step,
            "positions": self.get_player_positions(),
            "die": self._die_values,
            "guess": self._guess.get()}
    