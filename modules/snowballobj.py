import spriteobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Snowball(spriteobj.SpriteObj):
    "Class for the snowball"
    def __init__(self, screen, level, gfx, x, y):
        spriteobj.SpriteObj.__init__(self, screen, level, gfx, x, y)

        self.movingRightAnim = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.movingLeftAnim = [(4, 80), (5, 80), (6, 80), (7, 80)]

        self.move = self.move3
        self.moveLeft()

        self.name = "Snowball"

    def check(self):
        if self.horizontalMovement == self.movingRight:
            rt = self.rightTile()
            if rt == self.level.exitNo:
                self.level.exitReached()
                return
            elif (rt >= self.level.switchMin) and (rt <= self.level.switchMax):
                self.moveLeft()
                self.level.doSwitch(rt)
            elif self.wallRight():
                self.moveLeft()
            self.checkTrap(self.leftTile(), self.leftSpotOut)

        elif self.horizontalMovement == self.movingLeft:
            lt = self.leftTile()
            if lt == self.level.exitNo:
                self.level.exitReached()
                return
            elif (lt >= self.level.switchMin) and (lt <= self.level.switchMax):
                self.moveRight()
                self.level.doSwitch(lt)
            elif self.wallLeft():
                self.moveRight()
            self.checkTrap(self.rightTile(), self.rightSpotOut)

        if self.verticalMovement == self.falling:
            self.checkFalling()
        elif self.verticalMovement == 0:
            self.checkBottom1()
        
