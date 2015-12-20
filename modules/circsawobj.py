import staticfgobj

class CircSaw(staticfgobj.StaticFG):
    "Class for the circular saw object"
    def __init__(self, screen, level, gfx, x, y):
        staticfgobj.StaticFG.__init__(self, screen, level, gfx, x, y)

        self.animList = [(0, 1000), (1, 120), (2, 120), (3, 120), (4, 120), (5, 120), (6, 120), (7, 120)]

    def triggerFrameZero(self):
        self.level.frontData[self.sy][self.sx] = 0

    def triggerFrame(self):
        self.level.frontData[self.sy][self.sx] = self.level.invisibleDanger
