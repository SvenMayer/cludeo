# -*- coding: utf-8 -*-
import pytest

import os
import sys
sys.path.append(os.getcwd())


import clue
from clue.cluelogic import Player, Guess, Game, IllegalGuess
from clue import cluestatics


class TestPlayer:
    def test_init(self):
        pl = Player(u"Sven", u"Miss Scarlett")
        assert(pl._player_name == u"Sven")
        assert(pl._character_name == u"Miss Scarlett")
    
    def test_wrong_character(self):
        with pytest.raises(ValueError):
            pl = Player(u"Sven", u"Mis Scarlett")
    
    def test_get_names(self):
        pl = Player(u"Sven", u"Miss Scarlett")
        assert(pl.get_playername() == u"Sven")
        assert(pl.get_charactername() == u"Miss Scarlett")
    
    def test_set_objects(self):
        pl = Player(u"Sven", u"Miss Scarlett")
        pl.set_objects([u"library", u"Mrs. Peacock"])
        assert(u"library" in pl._objects)
        assert(u"Mrs. Peacock" in pl._objects)
    
    def test_set_illegal_object(self):
        pl = Player(u"Sven", u"Miss Scarlett")
        with pytest.raises(ValueError):
            pl.set_objects([u"library", u"Mrs. Peacock", u"TestUser"])
    
    def test_set_has_object(self):
        pl = Player(u"Sven", u"Miss Scarlett")
        pl.set_objects([u"library", u"Mrs. Peacock"])
        assert(pl.has_object(u"library") == True)
        assert(pl.has_object(u"Miss Scarlett") == False)
        

class TestGuess:
    def test_init(self):
        guess_order = [1,2,3]
        gs = Guess(u"Prof. Plum", u"wrench", u"kitchen", guess_order)
        assert(gs._killer == u"Prof. Plum")
        assert(gs._weapon == u"wrench")
        assert(gs._scene == u"kitchen")
        assert(gs._guess_order is guess_order)
    
    def test_illegal_input(self):
        guess_order = [1, 2, 3]
        with pytest.raises(ValueError):
            gs = Guess(u"Prof.", u"wrench", u"kitchen", guess_order)
        with pytest.raises(ValueError):
            gs = Guess(u"Prof. Plum", u"wre", u"kitchen", guess_order)
        with pytest.raises(ValueError):
            gs = Guess(u"Prof. Plum", u"wrench", u"kit", guess_order)
    
    def test_querried_player_name(self):
        guess_order = [1,2,3]
        gs = Guess(u"Prof. Plum", u"wrench", u"kitchen", guess_order)
        assert(gs.get_answering_player() == 1)
    
    def test_register_anser(self):
        guess_order = [u"Test1", u"Test2"]
        gs = Guess(u"Prof. Plum", u"wrench", u"kitchen", guess_order)
        gs.register_answer(u"wrench")
        assert(gs._answer == u"wrench")
    
    def test_register_wrong_answer(self):
        guess_order = [u"Test1", u"Test2"]
        gs = Guess(u"Prof. Plum", u"wrench", u"kitchen", guess_order)
        with pytest.raises(ValueError):
            gs.register_answer(u"hammer")
    
    def test_register_pass_answer(self):
        guess_order = [u"Test1", u"Test2"]
        gs = Guess(u"Prof. Plum", u"wrench", u"kitchen", guess_order)
        assert(gs.get_answering_player() == u"Test1")
        gs.register_answer(None)
        assert(gs.get_answering_player() == u"Test2")
    
    def test_answer_received(self):
        guess_order = [u"Test1", u"Test2"]
        gs = Guess(u"Prof. Plum", u"wrench", u"kitchen", guess_order)
        gs.register_answer(u"kitchen")
        assert(gs.get_answer() == u"kitchen")
        assert(gs.get_answering_player() == u"Test1")

    def test_all_pass(self):
        guess_order = [u"Test1", u"Test2"]
        gs = Guess(u"Prof. Plum", u"wrench", u"kitchen", guess_order)
        gs.register_answer(None)
        gs.register_answer(None)
        assert(gs.all_players_passed() == True)


class TestGame:
    def test_init(self):
        g = Game()
        assert(hasattr(g, "_gameboard"))
        assert(hasattr(g, "_player"))
        assert(g._player == [])
    
    def test_get_available_mobs(self):
        g = Game()
        for itm in clue.cluestatics.get_character_names():
            assert(itm in g.get_available_characters())
        for itm in g.get_available_characters():
            assert(itm in clue.cluestatics.get_character_names())
    
    def test_add_player(self):
        g = Game()
        with pytest.raises(ValueError):
            g.add_player(u"TestPlayer1", "Mr. None")
        g.add_player(u"TestPlayer", u"Mrs. White")
        assert(u"Mrs. White" not in g.get_available_characters())
        with pytest.raises(ValueError):
            g.add_player(u"TestPlayer", u"Mr. Green")
    
    def test_start_game(self):
        g = Game()
        g.add_player(u"Test1", u"Mrs. White")
        g.add_player(u"Test2", u"Mr. Green")
        g.start_game()
        assert(g._active_player == u"Test1")
        assert(g._active_move == u"move")
    
    def test_roll_die(self):
        g = Game()
        g.roll_dice()
        assert(g._dice[0] in range(1, 7))
        assert(g._dice[1] in range(1, 7))
    
    def test_prepare_move(self):
        g = Game()
        g.add_player(u"Test1", u"Col. Mustard")
        g._active_player = u"Test1"
        g.prepare_move()
        assert(g._active_move == u"move")
        assert(g._dice[0] in range(1, 7))
        assert(g._dice[1] in range(1, 7))
    
    def test_move(self):
        g = Game()
        g.add_player(u"Test1", u"Prof. Plum")
        g.add_player(u"Test2", u"Miss Scarlett")
        assert(g.move(u"Test1", u"right") == False)
        g.start_game()
        assert(g.move(u"Test2", u"up") == False)
        assert(g.move(u"Test1", u"right") == True)
    
    def test_get_player_mob(self):
        g = Game()
        g.add_player(u"Test1", u"Prof. Plum")
        g.add_player(u"Test2", u"Miss Scarlett")
        assert(g.get_player_character(u"Test1") == u"Prof. Plum")
        assert(g.get_player_character(u"Test2") == u"Miss Scarlett")
    
    def test_finish_movement_onboard(self):
        g = Game()
        g.add_player(u"Test1", u"Prof. Plum")
        g.add_player(u"Test2", u"Miss Scarlett")
        g.start_game()
        g.set_number_of_moves_for_active_player(2)
        assert(g._active_move == u"move")
        assert(g.move(u"Test1", u"right") == True)
        assert(g.move(u"Test1", u"right") == True)
        assert(g.move(u"Test1", u"right") == False)
        assert(g._active_move == u"")
    
    def test_finish_movement(self):
        g = Game()
        g.finish_movement()
        assert(g._active_move == u"")
    
    def test_finish_guess(self):
        g = Game()
        g._active_move = u"guess"
        g.finish_guess()
        assert(g._active_move == u"")
    
    def test_prepare_guess_in_hall(self):
        g = Game()
        g.add_player(u"Test1", u"Prof. Plum")
        g._active_player = u"Test1"
        g._active_move = u"guess"
        g.prepare_guess()
        assert(g._active_move == u"")

    def test_prepare_guess_in_room(self):
        g = Game()
        g.add_player(u"Test2", u"Miss Scarlett")
        g._active_player = u"Test2"
        g._active_move = u"guess"
        g._gameboard.enter_room(u"Miss Scarlett", 2)
        g.prepare_guess()
        assert(g._active_move == u"guess")

    def test_get_room_active_mob(self):
        g = Game()
        g.add_player(u"Test2", u"Miss Scarlett")
        g._active_player = u"Test2"
        g._gameboard.enter_room(u"Miss Scarlett", 4)
        assert(g.get_active_room() == u"lounge")
    
    def test_register_guess_wrong_player(self):
        g = Game()
        g._active_move = u"guess"
        g._active_player = u"Test2"
        with pytest.raises(IllegalGuess):
            g.register_guess(u"Test1", u"Mr. Green", u"study", u"candlestick")
    

    def test_register_guess_in_hall(self):
        g = Game()
        g.add_player(u"Test2", u"Miss Scarlett")
        g._active_move = u"guess"
        g._active_player = u"Test2"
        with pytest.raises(IllegalGuess):
            g.register_guess(u"Test2", u"Mr. Green", u"study", u"candlestick")
    
    
    def test_register_guess_wrong_move(self):
        g = Game()
        g.add_player(u"Test2", u"Miss Scarlett")
        g._gameboard.enter_room(u"Miss Scarlett", 2)
        g._active_player = u"Test2"
        g._active_move = u"move"
        with pytest.raises(IllegalGuess):
            g.register_guess(u"Test2", u"Mr. Green", u"study", u"candlestick")
    
    def test_register_guess_wrong_room(self):
        g = Game()
        g.add_player(u"Test2", u"Miss Scarlett")
        g._active_player = u"Test2"
        g._gameboard.enter_room(u"Miss Scarlett", 2)
        g._active_move = u"guess"
        with pytest.raises(IllegalGuess):
            g.register_guess(u"Test2", u"Mr. Green", u"lounge", u"candlestick")

    def test_register_good_guess(self):
        g = Game()
        g.add_player(u"Test2", u"Miss Scarlett")
        g._active_player = u"Test2"
        g._gameboard.enter_room(u"Miss Scarlett", 2)
        g._active_move = u"guess"
        g.register_guess(u"Test2", u"Mr. Green", u"study", u"candlestick")

    
        
            
    