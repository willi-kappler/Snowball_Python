import math
import pygame

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Font:
    "Font class. There are two fonts in the game, a small and a big one. Both are shared across all the other classes"
    def __init__(self, screen, name, width, height):
        self.screen = screen
        fontGfx = pygame.image.load(name)
        self.width = width
        self.height = height
        self.fontDict = {}
        x = 0
        for c in "ABCDEFGHIJ":
            self.fontDict[c] = pygame.Surface((self.width, self.height))
            self.fontDict[c].blit(fontGfx, (0, 0), (x, 0, self.width,self.height))
            x += self.width + 1
        x = 0
        for c in "KLMNOPQRST":
            self.fontDict[c] = pygame.Surface((self.width, self.height))
            self.fontDict[c].blit(fontGfx, (0, 0), (x, self.height + 1, self.width,self.height))
            x += self.width + 1
        x = 0
        for c in "UVWXYZ0123":
            self.fontDict[c] = pygame.Surface((self.width, self.height))
            self.fontDict[c].blit(fontGfx, (0, 0), (x,(self.height + 1) * 2, self.width, self.height))
            x += self.width + 1
        x = 0
        for c in "456789:.-+":
            self.fontDict[c] = pygame.Surface((self.width, self.height))
            self.fontDict[c].blit(fontGfx, (0, 0), (x,(self.height + 1) * 3, self.width, self.height))
            x += self.width + 1

        del fontGfx

        self.danceCycle = []
        for i in range(30):
            self.danceCycle.append(int(11.0 * math.sin(math.pi * i / 15.0)))
        self.maxIndex = len(self.danceCycle)
        self.danceIndex = 0

    def write(self, x, y, text, center = False):
        if center:
            x -= (len(text)*self.width / 2)
        for c in text:
            try:
                self.screen.blit(self.fontDict[c], (x, y))
            except KeyError:
                pass
            x += self.width

    def dance(self, x, y, text, center = False):
        if center:
            x -= (len(text)*self.width / 2)
        i = self.danceIndex
        for c in text:
            try:
                self.screen.blit(self.fontDict[c], (x, y + self.danceCycle[i]))
            except KeyError:
                pass
            x += self.width
            i += 1
            if i == self.maxIndex:
                i = 0
        self.danceIndex += 1
        if self.danceIndex == self.maxIndex:
            self.danceIndex = 0

