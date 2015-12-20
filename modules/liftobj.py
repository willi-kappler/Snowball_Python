import movingobj

class LiftObj(movingobj.MovingObj):
    "Class for the lift object. The trigger fot the lift is in the sprite class"
    def __init__(self, screen, level, gfx, x, y):
        movingobj.MovingObj.__init__(self, screen, level, gfx, x, y)

        self.speed = 4
        self.moveCounter = 32

        self.restoreBG = self.restoreBG1

        self.animList = [(0,10)]

    def move(self):
        self.y -= self.speed
        self.moveCounter -= self.speed
        if self.moveCounter <= 0:
            self.level.frontData[self.y/32][self.x/32] = self.level.liftNo
            self.level.movingObj.remove(self)
