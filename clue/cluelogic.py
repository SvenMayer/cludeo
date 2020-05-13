# -*- coding: utf-8 -*-
from . import cluestatics


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