import pytest

import os
import sys
sys.path.append(os.getcwd())


import clue
from clue.clue import MovementBoard, Mob, Gameboard
from clue.clue import IllegalMove


TEST_BOARD = [
        [0,   0, 0, 0,   0,   0,   0, 0],
        [0,   2, 2, 2,   2,   1, 201, 0],
        [0,   2, 2, 2, 102, 101,   1, 0],
        [0, 202, 2, 2,   2,   1,   1, 0],
        [0,   0, 0, 0,   0,   0,   0, 0],
    ]
class TestMovementBoard:
    _board_layout = TEST_BOARD
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
        assert(len(tilelist) == 4)
        assert((1, 5) in tilelist)
        assert((2, 6) in tilelist)
        assert((3, 6) in tilelist)
        assert((3, 5) in tilelist)
    
    def test_check_hallway(self):
        gb = MovementBoard(self._board_layout, {})
        assert(gb.is_hallway((1, 5)) == True)
        assert(gb.is_hallway((1, 6)) == True)
        assert(gb.is_hallway((1, 2)) == False)


class TestMob:
    def test_set_get_pos(self):
        mob = Mob((0, 0))
        mob.pos = (1, 2)
        assert(mob.pos == (1, 2))

class TestGameBoard:
    _characters = ((u"Mob1", (1, 5)), (u"Mob2", (1, 3)))
    _testboard = MovementBoard(TEST_BOARD, {})
    
    def test_get_positions(self):
        gb = Gameboard(self._testboard, self._characters)
        for name, pos in self._characters:
            assert(pos in gb.get_mobs_pos())
        
    def test_space_occupied(self):
        gb = Gameboard(self._testboard, self._characters)
        assert(gb.pos_occupied((0, 0)) == False)
        for name, pos in self._characters:
            assert(gb.pos_occupied(pos) == True)
    
    def test_get_random_pos(self):
        gb = Gameboard(self._testboard, self._characters)
        unoccupied_ones = [(2, 6), (3, 5), (3, 6)]
        res = set()
        for i in range(100):
            res.add(gb.get_random_free_pos_in_room(1))
        assert((1, 5) not in res)
        for tile in unoccupied_ones:
            assert(tile in res)

    def test_enter_room(self):
        gb = Gameboard(self._testboard, self._characters)
        unoccupied_ones = [(2, 6), (3, 5), (3, 6)]
        gb.enter_room(u"Mob2", 1)
        assert(gb.get_mob(u"Mob2").pos in unoccupied_ones)
    
    def test_set_move(self):
        gb = Gameboard(self._testboard, self._characters)
        assert(gb._active_mob is None)
        assert(gb._number_of_moves_remaining == 0)
        gb.set_active_mob(u"Mob1", 10)
        assert(gb._active_mob == u"Mob1")
        assert(gb._number_of_moves_remaining == 10)
    
    def test_move_illegal_player(self):
        gb = Gameboard(self._testboard, self._characters)
        gb.set_active_mob(u"Mob1", 10)
        assert(gb.move_mob(u"Mob2", u"down") == False)

    def test_move_through_door(self):
        gb = Gameboard(self._testboard, self._characters)
        gb.set_active_mob(u"Mob2", 10)
        mob = gb.get_mob(u"Mob2")
        assert(gb.move_mob(u"Mob2", u"down") == True)
        assert(gb.move_mob(u"Mob2", u"left") == True)
        assert(gb.move_mob(u"Mob2", u"left") == True)
    
    def test_finish_movement(self):
        gb = Gameboard(self._testboard, self._characters)
        gb.set_active_mob(u"Mob2", 3)
        gb.movement_done()
        assert(gb._active_mob is None)
        assert(gb._number_of_moves_remaining == 0)
        assert(len(gb._rooms_visited) == 0)
    
    def test_decrease_movement_ctr(self):
        gb = Gameboard(self._testboard, self._characters)
        gb.set_active_mob(u"Mob2", 2)
        gb.decrease_movement_counter()
        assert(gb._number_of_moves_remaining == 1)
        gb.decrease_movement_counter()
        assert(gb._active_mob is None)
        assert(gb._number_of_moves_remaining == 0)
    
    def test_execute_move(self):
        class Fake:
            def up(self, dummy):
                self.up_set = True
            def down(self, dummy):
                self.down_set = True
            def left(self, dummy):
                self.left_set = True
            def right(self, dummy):
                self.right_set = True
        fb = Fake()
        gb = Gameboard(fb, [])
        gb.execute_movement((0, 0), u"up")
        assert(fb.up_set == True)
        fb = Fake()
        gb = Gameboard(fb, [])
        gb.execute_movement((0, 0), u"down")
        assert(fb.down_set == True)
        fb = Fake()
        gb = Gameboard(fb, [])
        gb.execute_movement((0, 0), u"left")
        assert(fb.left_set == True)
        fb = Fake()
        gb = Gameboard(fb, [])
        gb.execute_movement((0, 0), u"right")
        assert(fb.right_set == True)


