OBJECTS = dict((
    (u"Miss Scarlett", u"miss_scarlett.jpg"),
    (u"Mrs. Peacock", u"mrs_peacock.jpg"),
    (u"Mr. Green", u"mr_green.jpg"),
    (u"Mrs. White", u"mrs_white.jpg"),
    (u"Prof. Plum", u"prof_plum.jpg"),
    (u"Col. Mustard", u"col_mustard.jpg"),
    (u"candlestick", u"candlestick.jpg"),
    (u"dagger", u"dagger.jpg"),
    (u"lead pipe", u"pipe.jpg"),
    (u"revolver", u"revolver.jpg"),
    (u"rope", u"rope.jpg"),
    (u"wrench", u"wrench.jpg"),
    (u"study", u"study.jpg"),
    (u"hall", u"hall.jpg"),
    (u"lounge", u"lounge.jpg"),
    (u"library", u"library.jpg"),
    (u"dining room", u"dining_room.jpg"),
    (u"billard room", u"billard_room.jpg"),
    (u"conservatory", u"conservatory.jpg"),
    (u"ball room", u"ball_room.jpg"),
    (u"kitchen", u"kitchen.jpg"),
    (u"gameboard", u"gameboard.jpg")
))

MOBS = dict((
    (u"Miss Scarlett", u"miss_scarlett.png"),
    (u"Mrs. Peacock", u"mrs_peacock.png"),
    (u"Mr. Green", u"mr_green.png"),
    (u"Mrs. White", u"mrs_white.png"),
    (u"Prof. Plum", u"prof_plum.png"),
    (u"Col. Mustard", u"col_mustard.png"),
))


def get_object_media_path(object_name):
    return u"media/" + OBJECTS[object_name]


def get_mob_media_path(mob_name):
    return u"media/" + MOBS[mob_name]
