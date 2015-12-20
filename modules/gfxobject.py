import pygame

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class GFXObject:
    "The base class for all graphic objects"
    def __init__(self, screen, level, gfx, x, y, animList = []):
        self.screen = screen
        self.level = level
        self.gfxList = gfx
        self.x = x
        self.y = y
        self.animList = animList # [(Frame1, Time1),(Frame2, Time2),(Frame3, Time3),(Frame4, Time4), ...]
        self.animFrame = 0
        self.timeElapsed = 0
        self.animFinished = False

    def animate(self):
        t = pygame.time.get_ticks()
        if t > self.timeElapsed + self.animList[self.animFrame][1]:
            self.timeElapsed = t
            self.animFrame += 1
            if self.animFrame == len(self.animList):
                self.animFrame = 0
                self.triggerFrameZero()
            else:
                self.triggerFrame()

    def display(self):
        self.screen.blit(self.gfxList[self.animList[self.animFrame][0]], (self.x, self.y))

    def go(self):
        self.animate()
        self.display()

    def triggerFrameZero(self):
        self.animFinished = True

    def triggerFrame(self):
        self.animFinished = False

