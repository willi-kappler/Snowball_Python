import gfxobject

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class StaticFG(gfxobject.GFXObject):
    "Class for not-moving objects like trap or circular saw"
    def __init__(self, screen, level, gfx, x, y):
        gfxobject.GFXObject.__init__(self, screen, level, gfx, x, y)

        self.sx = x / 32
        self.sy = y / 32

    def display(self):
        self.screen.blit(self.level.backGfx[self.level.backData[self.sy][self.sx]], (self.x, self.y))
        self.screen.blit(self.gfxList[self.animList[self.animFrame][0]], (self.x, self.y))

    def check(self):
        pass

    def go(self):
        self.animate()
        self.display()
