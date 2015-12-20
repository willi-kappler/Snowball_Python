import spriteobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Skull(spriteobj.SpriteObj):
    "Class for the skull object: activate switch, doesn't want to fall."
    def __init__(self, screen, level, gfx, x, y):
        spriteobj.SpriteObj.__init__(self, screen, level, gfx, x, y)

        self.movingLeftAnim = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.movingRightAnim = [(5, 80), (6, 80), (7, 80), (8, 80)]
        self.turningLeftAnim = [(4, 40), (4, 40)]
        self.turningRightAnim = [(4, 40), (4, 40)]
        self.sleepingAnim = [(4, 10), (4, 10)]

        self.sleep = self.sleep1
        self.sleepMax = 10000

        self.move = self.move4
        self.moveLeft()

        self.name = "Skull"

    def check(self):
        if self.verticalMovement == 0:
            self.checkBottom2()
            if self.horizontalMovement == self.movingRight:
                rt = self.rightTile()
                if (rt >= self.level.switchMin) and (rt <= self.level.switchMax):
                    self.turnLeft()
                    self.level.doSwitch(rt)
                else:
                    br = self.bottomRightTile()
                    if self.wallRight() or (br == 0) or (br >= self.level.doorOpened):
                        self.turnLeft()

            elif self.horizontalMovement == self.movingLeft:
                lt = self.leftTile()
                if (lt >= self.level.switchMin) and (lt <= self.level.switchMax):
                    self.turnRight()
                    self.level.doSwitch(lt)
                else:
                    bl = self.bottomLeftTile()
                    if self.wallLeft() or (bl == 0) or (bl >= self.level.doorOpened):
                        self.turnRight()
        elif self.verticalMovement == self.falling:
            self.checkFalling()
