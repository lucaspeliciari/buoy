from util.vectors import *


class Vertex:
    def __init__(self, index, next_index, coord):
        self.index = index
        self.next_index = next_index
        self.coord = Vector2(coord)
        self.submerged = False
