import random
import spriteobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Ghost(spriteobj.SpriteObj):
    "Class for the ghost object: moves through everything"
    def __init__(self, screen, level, gfx, x, y):
        spriteobj.SpriteObj.__init__(self, screen, level, gfx, x, y)

        self.movingUpAnim = [(9, 40), (9, 40)]
        self.movingDownAnim = [(4, 40), (4, 40)]
        self.movingLeftAnim = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.movingRightAnim = [(5, 80), (6, 80), (7, 80), (8, 80)]

        self.turningLeftAnim = [(4, 40), (4, 40)]
        self.turningRightAnim = [(4, 40), (4, 40)]

        self.moveLeft()

        self.dirCounter = 0

        self.move = self.move2
        self.stop()

        self.name = "Ghost"

    def check(self):
        self.dirCounter += 1
        if self.dirCounter > 50:
            self.stop()
            r = random.randint(0,3)
            if r == 0:
                self.moveUp()
            elif r == 1:
                self.moveDown()
            elif r == 2:
                if self.lastHorizontal != self.movingLeft:
                    self.turnLeft()
                else:
                    self.moveLeft()
            elif r == 3:
                if self.lastHorizontal != self.movingRight:
                    self.turnRight()
                else:
                    self.moveRight()
            self.dirCounter = 0

