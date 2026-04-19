from enum import Enum, Flag
import types


globals = types.SimpleNamespace()
globals.gameSize = 32

pressed = set()

def key_down(e):
    pressed.add(e.keysym)
def key_up(e):
    pressed.discard(e.keysym)

def is_pressed(key): return key in pressed


class SpriteType(Enum):
    EMPTY = 0
    PACMAN = 1
    GHOST = 2
    PILL = 3
    WALL = 4
    DOT = 5

class Direction(Flag):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8
    UPRIGHT = UP | RIGHT
    UPLEFT = UP | LEFT
    DOWNRIGHT = DOWN | RIGHT
    DOWNLEFT = DOWN | LEFT

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

