# -*- coding: utf-8 -*-
import random
import time
import sys

if sys.version_info[0] > 2:
    random.seed(time.perf_counter())
else:
    random.seed(time.clock())


class IllegalMove(BaseException):
    pass


def random_integer(max_int):
    res = max_int + 1
    while res > max_int:
        res = int(random.random() * (max_int + 1))
    return res


class MovementBoard:
    HALLWAY = 1
    def __init__(self, board, special_moves):
        self.board = board
        self.special_moves = special_moves
    
    def tile_no(self, pos):
        return self.board[pos[0]][pos[1]]

    def room_no(self, pos):
        tileno = self.tile_no(pos)
        return tileno % 100

    def move_allowed(self, oldpos, newpos):
        if self.room_no(oldpos) == self.room_no(newpos):
            return True
        if self.is_door(oldpos) and self.is_door(newpos):
            return True
        return False
    
    def is_door(self, pos):
        return self.tile_no(pos) // 100 == 1
    
    def is_special_pos(self, pos):
        return pos in self.special_moves
    
    def is_hallway(self, pos):
        return self.room_no(pos) == self.HALLWAY

    def move_to(self, oldpos, newpos):
        if self.move_allowed(oldpos, newpos):
            if self.is_special_pos(newpos):
                return self.special_moves[newpos]
            return newpos
        else:
            raise(IllegalMove())
    
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
        newpos = (pos[0], pos[1]+1)
        return self.move_to(pos, newpos)
    
    def get_tile_pos(self, room):
        res = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == room:
                    res.append((row, col))
        return res


class Mob:
    def __init__(self, startpos):
        self.pos = startpos


class Gameboard:
    def __init__(self, layout, characters):
        self._layout = layout
        self._mobs = {}
        self._active_mob_name = u""
        self._start_room = 0
        self._number_of_moves_remaining = 0
        for mob_name, start_pos in characters:
            self._mobs[mob_name] = Mob(start_pos)
    
    def get_mobs_pos(self):
        return [mob.pos for mob in self._mobs.values()]
    
    def pos_occupied(self, pos):
        return pos in self.get_mobs_pos()
    
    def get_random_free_pos_in_room(self, room):
        freetiles = [tile for tile in self._layout.get_tile_pos(room)
                     if tile not in self.get_mobs_pos()]
        random_idx = random_integer(len(freetiles) - 1)
        return freetiles[random_idx]
    
    def enter_room(self, name, room):
        self._mobs[name].pos = self.get_random_free_pos_in_room(room)
    
    def get_mob(self, name):
        return self._mobs[name]
    
    def get_active_mob_name(self):
        return self._active_mob_name
    
    def set_active_mob(self, name, number_of_steps):
        self._start_room = self._layout.room_no(self._mobs[name].pos)
        self._active_mob_name = name
        self._number_of_moves_remaining = number_of_steps
    
    def execute_movement(self, pos, direction):
        mv = None
        if direction == u"up":
            mv = self._layout.up
        elif direction == u"down":
            mv = self._layout.down
        elif direction == u"left":
            mv = self._layout.left
        elif direction == u"right":
            mv = self._layout.right
        else:
            raise ValueError()
        return mv(pos)

    def move_mob(self, name, direction):
        if name != self._active_mob_name:
            return False
        mob = self._mobs[name]
        oldpos = mob.pos
        oldroom = self._layout.room_no(oldpos)
        try:
            newpos = self.execute_movement(oldpos, direction)
            newroom = self._layout.room_no(newpos)
        except IllegalMove:
            return False
        if self._layout.is_hallway(newpos) and self.pos_occupied(newpos):
            return False
        if self._layout.is_hallway(newpos):
            self.decrease_movement_counter()
            mob.pos = newpos
        elif newroom == oldroom:
            mob.pos = newpos
        elif newroom == self._start_room:
            return False
        else:
            self.enter_room(name, newroom)
            self.movement_done()
        return True
    
    def movement_done(self):
        self._active_mob_name = u""
        self._number_of_moves_remaining = 0
        self._start_room = 0
    
    def decrease_movement_counter(self):
        self._number_of_moves_remaining -= 1
        if self._number_of_moves_remaining <= 0:
            self.movement_done()
