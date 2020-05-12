import pytest

import os
import sys
sys.path.append(os.getcwd())


import clue
from clue.clue import MovementBoard, Mob
from clue.clue import IllegalMove


class TestMovementBoard:
    _board_layout = [
        [0,   0, 0, 0,   0,   0,   0, 0],
        [0,   2, 2, 2,   2,   1,   1, 0],
        [0,   2, 2, 2, 102, 101,   1, 0],
        [0,   2, 2, 2,   2,   1,   1, 0],
        [0,   0, 0, 0,   0,   0,   0, 0],
    ]
    _specials = {}
    
    def test_movement(self):
        gb = MovementBoard(self._board_layout, self._specials)
        start_pos = (2, 2)
        assert(gb.up(start_pos) == (1, 2))
        assert(gb.left(start_pos) == (2, 1))
        assert(gb.down(start_pos) == (3, 2))
        assert(gb.right(start_pos) == (2, 3))
    
    def test_leave_through_wall(self):
        gb = MovementBoard(self._board_layout, self._specials)
        start_pos = (1, 4)
        with pytest.raises(IllegalMove):
            gb.right(start_pos)
        with pytest.raises(IllegalMove):
            gb.up(start_pos)
    
    def test_door(self):
        gb = MovementBoard(self._board_layout, self._specials)
        start_pos_rm2 = (2, 4)
        start_pos_rm1 = (2, 5)
        assert(gb.right(start_pos_rm2) == (2, 5))
        assert(gb.left(start_pos_rm1) == (2, 4))
        assert(gb.right((2, 3)) == (2, 4))
    
    def test_special_tile(self):
        gb = MovementBoard(self._board_layout, {(1, 6): (3, 1), (3, 1): (1, 6)})
        assert(gb.right((1, 5)) == (3, 1))
        assert(gb.down((2, 1)) == (1, 6))
    
    def test_get_tile_list(self):
        gb = MovementBoard(self._board_layout, {})
        tilelist = gb.get_tile_pos(1)
        assert(len(tilelist) == 5)
        assert((1, 5) in tilelist)
        assert((1, 6) in tilelist)
        assert((2, 6) in tilelist)
        assert((3, 6) in tilelist)
        assert((3, 5) in tilelist)


class TestMob:
    def test_set_get_pos(self):
        mob = Mob(None, (0, 0))
        mob.set_position((1, 2))
        assert(mob.get_position() == (1, 2))


#class TestGameBoard:
#    def test_gameboard(self):
