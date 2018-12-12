from ctypes import cdll, c_float
lib = cdll.LoadLibrary('./HeuristicComp/bin/libgame.so')


class Game(object):
    def __init__(self, north, south, depth=4):
        depth = 4
        north = (c_float * 10)(*north)
        south = (c_float * 10)(*south)
        self.obj = lib.Game_new(depth, north, south)

    def run(self):
        return lib.Game_run(self.obj)
