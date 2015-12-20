import random
import spriteobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Zombie(spriteobj.SpriteObj):
    "Class for the zombie: moce boxes, doesn't want to fall"
    def __init__(self, screen, level, gfx, x, y):
        spriteobj.SpriteObj.__init__(self, screen, level, gfx, x, y)

        self.movingLeftAnim = [(0, 100, 1), (1, 100, 0), (2, 100, 1), (3, 100, 0)] # special treatment for limp
        self.movingRightAnim = [(5, 100, 1), (6, 100, 0), (7, 100, 1), (8, 100, 0)]
        self.turningLeftAnim = [(4, 40), (4, 40)]
        self.turningRightAnim = [(4, 40), (4, 40)]

        self.speed = 0

        self.move = self.move3
        self.moveLeft()

        self.name = "Zombie"

    def check(self):
        if self.verticalMovement == 0:
            self.checkBottom2()
            if self.horizontalMovement == self.movingRight:
                self.speed = self.animList[self.animFrame][2]
                rt = self.rightTile()
                if rt == self.level.boxNo:
                    self.turnLeft()
                    self.moveBoxRight()
                else:
                    br = self.bottomRightTile()
                    if self.wallRight() or (br == 0) or (br >= self.level.doorOpened):
                        self.turnLeft()

            elif self.horizontalMovement == self.movingLeft:
                self.speed = self.animList[self.animFrame][2]
                lt = self.leftTile()
                if lt == self.level.boxNo:
                    self.turnRight()
                    self.moveBoxLeft()
                else:
                    bl = self.bottomLeftTile()
                    if self.wallLeft() or (bl == 0) or (bl >= self.level.doorOpened):
                        self.turnRight()
        else:
            self.checkFalling()
