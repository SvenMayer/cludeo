# -*- coding: utf-8 -*-
from . import cluestatics


class Player:
    def __init__(self, player_name, character_name):
        self._player_name = player_name
        if character_name not in cluestatics.get_character_names():
            raise ValueError(u"Charactername {0:s} does not exist.".format(
                character_name))
        self._character_name = character_name
    
    def get_playername(self):
        return self._player_name
    
    def get_charactername(self):
        return self._character_name
    