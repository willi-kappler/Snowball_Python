import movingobj

class BoxObj(movingobj.MovingObj):
    "Class for movable boxes"
    def __init__(self, screen, level, gfx, x, y, direction):
        movingobj.MovingObj.__init__(self, screen, level, gfx, x, y)

        self.speed = 8
        self.moveCounter = 32

        self.restoreBG = self.restoreBG2

        self.animList = [(0, 10)]

        self.horizontalDirection = direction

    def move(self):
        if self.horizontalDirection == self.movingLeft:
            self.x -= self.speed
            self.countDown()

        elif self.horizontalDirection == self.movingRight:
            self.x += self.speed
            self.countDown()

    def countDown(self):
        self.moveCounter -= self.speed
        if self.moveCounter <= 0:
            if self.horizontalDirection == self.movingLeft:
                self.level.frontData[self.y/32][(self.x/32) + 1] = 0
            elif self.horizontalDirection == self.movingRight:
                self.level.frontData[self.y/32][(self.x/32) - 1] = 0
            self.level.frontData[self.y/32][self.x/32] = self.level.boxNo
            self.level.movingObj.remove(self)

