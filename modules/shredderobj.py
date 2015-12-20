import spriteobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Shredder(spriteobj.SpriteObj):
    "Class for the shredder object: falls, can use lift, activate switch"
    def __init__(self, screen, level, gfx, x, y):
        spriteobj.SpriteObj.__init__(self, screen, level, gfx, x, y)

        self.movingLeftAnim = [(0, 80), (1, 80), (2, 80), (3, 80), (4, 80), (5, 80), (6, 80), (7, 80), (8, 80)]
        self.movingRightAnim = [(8, 80), (7, 80), (6, 80), (5, 80), (4, 80), (3, 80), (2, 80), (1, 80), (0, 80)]

        self.move = self.move3
        self.moveLeft()

        self.name = "Shredder"

    def check(self):
        if self.horizontalMovement == self.movingRight:
            rt = self.rightTile()
            if (rt >= self.level.switchMin) and (rt <= self.level.switchMax):
                self.turnLeft()
                self.level.doSwitch(rt)
            elif self.wallRight():
                self.moveLeft()

        elif self.horizontalMovement == self.movingLeft:
            lt = self.leftTile()
            if (lt >= self.level.switchMin) and (lt <= self.level.switchMax):
                self.turnRight()
                self.level.doSwitch(lt)
            elif self.wallLeft():
                self.moveRight()

        if self.verticalMovement == self.falling:
            self.checkFalling()
        elif self.verticalMovement == 0:
            self.checkBottom1()
        
