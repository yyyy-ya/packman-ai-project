
from GameObject import GameObject
from GameDefs import Pos

from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals, is_pressed


class PacMan(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)



    def human_control(self):
 
        direction = Direction.NONE
        if is_pressed('Up'):
               direction |= Direction.UP  
        if is_pressed('Down'):
               direction |=  Direction.DOWN 
        if is_pressed('Left'):
               direction |=  Direction.LEFT 
        if is_pressed('Right'):
               direction |=  Direction.RIGHT  
        return direction
        
    def move(self):
        return self.human_control()


