import random
import spriteobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Firedevil(spriteobj.SpriteObj):
    "Class for the fire devil: falls, removes ice-blocks"
    def __init__(self, screen, level, gfx, x, y):
        spriteobj.SpriteObj.__init__(self, screen, level, gfx, x, y)

        self.movingLeftAnim = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.movingRightAnim = [(5, 80), (6, 80), (7, 80), (8, 80)]

        self.turningLeftAnim = [(4, 40), (4, 40)]
        self.turningRightAnim = [(4, 40), (4, 40)]

        self.sleepingAnim = [(4, 40), (4, 40)]

        self.move = self.move4
        self.moveLeft()

        self.sleep = self.sleep1
        self.sleepMax = 6000

        self.name = "Firedevil"

    def check(self):
        if self.verticalMovement == 0:
            bt = self.bottomTile()
            if bt == 0:
                self.stop()
                self.fall()
            elif bt == 1:
                self.level.frontData[self.bottomSpotOut][self.midX] = 0
                self.screen.blit(self.level.backGfx[self.level.backData[self.bottomSpotOut][self.midX]], (self.midX*32, self.bottomSpotOut*32))
            tt = self.topTile()
            if tt == 1:
                self.level.frontData[self.topSpotOut][self.midX] = 0
                self.screen.blit(self.level.backGfx[self.level.backData[self.topSpotOut][self.midX]], (self.midX*32, self.topSpotOut*32))
        if self.horizontalMovement == self.movingRight:
            if self.rightTile() == 1:
                self.level.frontData[self.midY][self.rightSpotOut] = 0
                self.screen.blit(self.level.backGfx[self.level.backData[self.midY][self.rightSpotOut]], (self.rightSpotOut*32, self.midY*32))
                self.turnLeft()
            elif self.wallRight():
                self.turnLeft()

        elif self.horizontalMovement == self.movingLeft:
            if self.leftTile() == 1:
                self.level.frontData[self.midY][self.leftSpotOut] = 0
                self.screen.blit(self.level.backGfx[self.level.backData[self.midY][self.leftSpotOut]], (self.leftSpotOut*32, self.midY*32))
                self.turnRight()
            elif self.wallLeft():
                self.turnRight()

        elif self.verticalMovement == self.falling:
            self.checkFalling()

