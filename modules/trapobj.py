import staticfgobj

class TrapObj(staticfgobj.StaticFG):
    "Class for the trap"
    def __init__(self, screen, level, gfx, x, y):
        staticfgobj.StaticFG.__init__(self, screen, level, gfx, x, y)

        self.animList = [(0,80), (1,80), (2,80)]

    def triggerFrameZero(self):
        self.level.frontData[self.sy][self.sx] = self.level.trapClosed
        self.level.staticObj.remove(self)
        self.display = self.displayLast

    def displayLast(self):
        self.level.displayXY(self.sx, self.sy)
