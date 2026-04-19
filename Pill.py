from GameObject import GameObject
from GameDefs import SpriteType


class Pill(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PILL)
        self.pillEaten = False

    def eaten(self):
        self.pillEaten = True
        self.hide()

    def isActive(self):
        return not self.pillEaten
