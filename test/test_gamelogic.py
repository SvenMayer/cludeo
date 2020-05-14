# -*- coding: utf-8 -*-
import pytest

import os
import sys
sys.path.append(os.getcwd())


import clue
from clue.cluelogic import Player, Guess


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
        assert(gs.get_querried_player_name() == 1)