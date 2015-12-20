import spriteobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Spider(spriteobj.SpriteObj):
    "The spider is not fully implemented yet"
    def __init__(self, screen, level, gfx, x, y):
        spriteobj.SpriteObj.__init__(self, screen, level, gfx, x, y)

        self.movingLeftAnim = [(0, 80), (1, 80), (2, 80), (1, 80)]
        self.movingRightAnim = [(3, 80), (4, 80), (5, 80), (4, 80)]
        self.turningLeftAnim = [(6, 10), (6, 10)]
        self.turningRightAnim = [(6, 10), (6, 10)]
        self.sleepingAnim = [(6, 10), (6, 10)]

        self.sleep = self.sleep1
        self.sleepMax = 10000

        self.move = self.move4
        self.moveLeft()

        self.name = "Spider"

    def check(self):
        if self.horizontalMovement == self.movingRight:
            br = self.bottomRightTile()
            if self.wallRight() or (br == 0) or (br >= self.level.keyNo):
                self.turnLeft()

        elif self.horizontalMovement == self.movingLeft:
            bl = self.bottomLeftTile()
            if self.wallLeft() or (bl == 0) or (bl >= self.level.keyNo):
                self.turnRight()
