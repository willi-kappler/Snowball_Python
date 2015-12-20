import pygame
import spriteobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Player(spriteobj.SpriteObj):
    "This class implements the player interaction with the rest of the game. Some functionality is in the sprite class."
    def __init__(self, screen, level, gfx, x, y):
        spriteobj.SpriteObj.__init__(self, screen, level, gfx, x, y)

        self.black = (0,0,0)

        self.borderX = 6

        self.movingLeftAnim = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.movingRightAnim = [(10, 80), (11, 80), (12, 80), (13, 90)]
        self.turningLeftAnim = [(0, 10), (0, 10)]
        self.turningRightAnim = [(10, 10), (10, 10)]
        self.lookingLeftAnim = [(1, 10)]
        self.lookingRightAnim = [(11, 10)]
        self.fallingLeftAnim = [(6, 10)]
        self.fallingRightAnim = [(16, 10)]
        self.jumpingLeftAnim = [(5, 10)]
        self.jumpingRightAnim = [(15, 10)]
        self.stopAnim = [(0, 10)]
        self.dieAnim = [(20, 50), (28, 50), (21, 50), (22, 50), (29, 50), (23, 50)]
        self.duckingLeftAnim = [(4, 10)]
        self.duckignRightAnim = [(14, 10)]
        self.poisonLeftAnim= [(7, 80), (8, 80), (7, 80), (9, 80)]
        self.poisonRightAnim= [(17, 80), (18, 80), (17, 80), (19, 80)]
        self.climbAnim = [(24, 80), (25, 80), (24, 80), (26, 80)]
        self.turningLeftAnim = [(28, 40), (28, 40), (1, 10)]
        self.turningRightAnim = [(28, 40), (28, 40), (11, 10)]

        self.points = 0
        self.lives = 3

        self.resetStatus()

        self.name = "Player"

    def resetStatus(self):
        self.noKeyPressedTime = 0
        self.boringTime = 10000

        self.switchDone = False

        self.ducking = False
        self.dying = False
        self.keys = 0
        self.blocksMax = 12
        self.blocks = self.blocksMax

        self.transporterCycle = 0

        self.poisonedTime = 0
        self.shieldTime = 0

        self.stop()
        self.lookLeft()

    def moveLeft(self):
        if (not self.dying) and (self.poisonedTime == 0):
            if (self.horizontalMovement > 0) and (self.horizontalMovement != self.turningLeft):
                self.lastHorizontal = self.horizontalMovement
                self.horizontalMovement = self.turningLeft
                self.animList = self.turningLeftAnim
                self.animFrame = 0
            else:
                spriteobj.SpriteObj.moveLeft(self)

    def moveRight(self):
        if (not self.dying) and (self.poisonedTime == 0):
            if (self.horizontalMovement < 0) and (self.horizontalMovement != self.turningRight):
                self.lastHorizontal = self.horizontalMovement
                self.horizontalMovement = self.turningRight
                self.animList = self.turningRightAnim
                self.animFrame = 0
            else:
                spriteobj.SpriteObj.moveRight(self)

    def keyUpPress(self):
        if (not self.dying) and (not self.ducking) and (self.verticalMovement == 0) and (self.poisonedTime == 0):
            ct = self.centerTile()
            tt = self.topTile()
            if (ct == 0) and ((tt == 0) or (tt >= self.level.keyNo)):
                self.jump()
            elif (tt == self.level.ladder1) or (tt == self.level.ladder2):
                self.climbUp()

        self.switchDone = False

    def keyDownPress(self):
        if (not self.dying) and (not self.ducking) and (self.verticalMovement == 0) and (self.poisonedTime == 0):
            bt = self.bottomTile()
            if bt == self.level.transporterNo:
                self.teleport()
            elif (bt == self.level.ladder1) or (bt == self.level.ladder2):
                self.climbDown()
            else:
                self.ducking = True
                if self.horizontalMovement > 0:
                    self.animList = self.duckignRightAnim
                    self.horizontalMovement = self.lookingRight
                elif self.horizontalMovement < 0:
                    self.animList = self.duckingLeftAnim
                    self.horizontalMovement = self.lookingLeft
                self.animFrame = 0

    def keyUpRelease(self):
        if (self.verticalMovement == self.climbingUp) or (self.verticalMovement == self.climbingDown):
            self.lastVertical = self.verticalMovement
            self.verticalMovement = 0
            self.animList = [self.climbAnim[0]]
            self.animFrame = 0

    def keyDownRelease(self):
        if self.ducking:
            self.ducking = False
            if self.horizontalMovement == self.lookingRight:
                self.animList = self.lookingRightAnim
            elif self.horizontalMovement == self.lookingLeft:
                self.animList = self.lookingLeftAnim
            self.animFrame = 0
        elif (self.verticalMovement == self.climbingUp) or (self.verticalMovement == self.climbingDown):
            self.lastVertical = self.verticalMovement
            self.verticalMovement = 0
            self.animList = [self.climbAnim[0]]
            self.animFrame = 0

    def keyLeftRelease(self):
        if (not self.dying) and (self.poisonedTime == 0):
            self.switchDone = False
            if self.horizontalMovement != self.turningLeft:
                self.lookLeft()
        if (self.verticalMovement == self.climbingUp) or (self.verticalMovement == self.climbingDown):
            self.animList = self.climbAnim
            self.animFrame = 0


    def keyRightRelease(self):
        if (not self.dying) and (self.poisonedTime == 0):
            self.switchDone = False
            if self.horizontalMovement != self.turningRight:
                self.lookRight()
        if (self.verticalMovement == self.climbingUp) or (self.verticalMovement == self.climbingDown):
            self.animList = self.climbAnim
            self.animFrame = 0


    def checkBottom(self):
        if (self.verticalMovement == 0) or (self.verticalMovement == self.climbingUp) or (self.verticalMovement == self.climbingDown):
#        if (self.verticalMovement != self.falling) and (self.verticalMovement != self.jumping) and (self.verticalMovement != self.usingLift):
            bt = self.bottomTile()
            if  (bt == self.level.spikeNo) and (self.shieldTime == 0):
                self.die()
            elif bt == self.level.brickNo:
                self.breakBrick1()
            elif bt == self.level.brickBrokenNo:
                self.breakBrick2()
            elif bt == self.level.liftNo:
                self.useLift(False)
            elif not self.wallDown():
                if (bt != self.level.ladder1) and (bt != self.level.ladder2):
                    self.fall()

    def stopFalling(self):
        self.lastVertical = self.falling
        self.verticalMovement = 0
        if self.poisonedTime == 0:
            self.resetHorizontalMovement()
        else:
            if (self.horizontalMovement > 0) or (self.lastHorizontal > 0):
                self.animList = self.poisonLeftAnim
            elif (self.horizontalMovement < 0) or (self.lastHorizontal < 0):
                self.animList = self.poisonRightAnim
            self.animFrame = 0

    def stopLift(self):
        self.lastVertical = self.usingLift
        self.verticalMovement = 0
        if self.poisonedTime == 0:
            self.resetHorizontalMovement()

    def stopClimbing(self):
        self.lastVertical = self.climbingUp
        self.verticalMovement = 0
        self.y = self.midY * 32 # sane y coordinate
        self.animList = [self.climbAnim[0]]
        self.animFrame = 0

    def move(self):
        if self.dying:
            if self.y < 444:
                self.y += 4
            else:
                self.lives -= 1
                if self.lives == 0:
                    self.screen.blit(self.level.gameOverGfx, (80,120))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    while True:
                        evt = pygame.event.wait()
                        if evt.type == pygame.KEYDOWN:
                            break
                    self.level.quitGame = True
                else:
                    self.level.load()
                    self.level.restart()

        else:
            if self.shieldTime > 0:
                self.shieldTime -= 1
                self.screen.blit(self.gfxList[27], (self.x, self.y))
            elif self.poisonedTime > 0:
                self.poisonedTime -= 1
                if self.poisonedTime == 0:
                    if self.lastHorizontal > 0:
                        self.lookRight()
                    elif self.lastHorizontal < 0:
                        self.lookLeft()

            if self.horizontalMovement == self.movingRight:
                if self.x < 448 - self.speed:
                    rt = self.rightTile()
                    if rt == self.level.boxNo:
                        self.moveBoxRight()
                    elif not self.checkObject(rt, self.rightSpotOut, self.midY):
                        if not self.wallRight():
                            self.x += self.speed
                    self.checkTrap(self.leftTile(), self.leftSpotOut)
                else:
                    self.x = 448

            elif self.horizontalMovement == self.movingLeft:
                if self.x > self.speed:
                    lt = self.leftTile()
                    if lt == self.level.boxNo:
                        self.moveBoxLeft()
                    elif not self.checkObject(lt, self.leftSpotOut, self.midY):
                        if not self.wallLeft():
                            self.x -= self.speed
                    self.checkTrap(self.rightTile(), self.rightSpotOut)
                else:
                    self.x = 0

            elif self.horizontalMovement == self.turningLeft:
                if self.animFrame >= 2:
                    self.lookLeft()

            elif self.horizontalMovement == self.turningRight:
                if self.animFrame >= 2:
                    self.lookRight()

            if self.verticalMovement == self.falling:
                if self.y < 444:
                    if not self.checkObject(self.bottomTile(), self.midX, self.bottomSpotOut):
                        if self.wallDown():
                            self.y = (self.y / 32) * 32 # sane y coordinate
                            self.stopFalling()
                        else:
                            self.y += 4
                else:
                    self.y = 448
                    self.stopFalling()

            elif self.verticalMovement == self.jumping:
                if self.y > 0:
                    self.y -= 2
                else:
                    self.fall()
                if self.jumpCounter > 0:
                    self.jumpCounter -= 1
                else:
                    self.fall()
                if not self.checkObject(self.topTile(), self.midX, self.topSpotOut):
                    if self.wallUp():
                        self.fall()

            elif self.verticalMovement == self.usingLift:
                if self.y > 0:
                    self.y -= 4
                    self.liftCounter -= 4
                    if self.liftCounter <= 0:
                        self.y = (self.y / 32) * 32 # sane y coordinate
                        self.stopLift()
                else:
                    self.y = 0
                    self.stopLift()

            elif self.verticalMovement == self.climbingUp:
                if self.wallUp():
                    self.stopClimbing()
                else:
                    ct = self.topTile()
                    if (ct == self.level.ladder1) or (ct == self.level.ladder2):
                        self.y -= 2
            elif self.verticalMovement == self.climbingDown:
                if self.wallDown():
                    self.stopClimbing()
                else:
                    ct = self.centerTile()
                    if (ct == self.level.ladder1) or (ct == self.level.ladder2):
                        self.y += 2
    def check(self):
        if (not self.dying):
            if self.shieldTime == 0:
                for e in self.level.enemies:
                    dx = self.x - e.x
                    dy = self.y - e.y
                    if (dx > -30) and (dx < 30) and (dy > -30) and (dy < 30):
                        self.die()
                if self.centerTile() == self.level.invisibleDanger:
                    self.die()
            self.checkBottom()

    def die(self):
        if not self.dying:
            self.dying = True
            self.keys = 0
            if self.soundAvailable:
                self.level.playerDieSnd.play()
            self.animList = self.dieAnim
            self.animFrame = 0

    def doAction(self):
        if self.horizontalMovement > 0:
            x = ((self.x + 22) / 32) + 1
            if self.ducking:
                y = (self.y / 32) + 1
            else:
                y = self.y / 32
            if (x <= 14) and (y <= 14):
                self.setIceblock(x, y)
        elif self.horizontalMovement < 0:
            x = ((self.x + 9) / 32) - 1
            if self.ducking:
                y = (self.y / 32) + 1
            else:
                y = self.y / 32
            if (x >= 0) and (y <= 14):
                self.setIceblock(x, y)

    def setIceblock(self, x, y):
        if y > 0:
            if self.level.frontData[y-1][x] == self.level.boxNo:
                if self.soundAvailable:
                    self.level.noBlocksSnd.play()
                return

        if (self.level.snowball.midX == x) and (self.level.snowball.midY == y):
            if self.soundAvailable:
                self.level.noBlocksSnd.play()
            return

        for e in self.level.enemies:
            if (e.midX == x) and (e.midY == y):
                if self.soundAvailable:
                    self.level.noBlocksSnd.play()
                return

        t = self.level.frontData[y][x]
        if t == 0:
            if self.blocks > 0:
                self.blocks -= 1
                self.level.frontData[y][x] = 1
                self.screen.blit(self.level.frontGfx[1], (x*32,y*32))
                if self.soundAvailable:
                    self.level.iceblockSnd.play()
                self.displayBlocks()
            elif self.soundAvailable:
                    self.level.noBlocksSnd.play()
        elif t == 1:
            if self.blocks < self.blocksMax:
                self.blocks += 1
                self.level.frontData[y][x] = 0
                self.screen.blit(self.level.backGfx[self.level.backData[y][x]], (x*32,y*32))
                if self.soundAvailable:
                    self.level.iceblockSnd.play()
                self.displayBlocks()
            elif self.soundAvailable:
                    self.level.noBlocksSnd.play()

    def displayBlocks(self):
        x = 496
        y = 140
        self.screen.blit(self.level.infopanelGfx, (491,137), (11,137,137,137))
        for i in range(self.blocks):
            self.screen.blit(self.level.frontGfx[1], (x,y))
            x += 33
            if x >= 626:
                x = 496
                y += 33

    def printLives(self):
        self.screen.blit(self.level.infopanelGfx, (587,23), (107,23,38,16))
        self.level.font.write(606, 23, str(self.lives), True)

    def printScore(self):
        self.screen.blit(self.level.infopanelGfx, (520,59), (40,59,98,16))
        self.level.font.write(569, 59, str(self.points), True)

    def checkObject(self, t, x, y):
        if (t >= self.level.switchMin) and (t <= self.level.switchMax):
            if not self.switchDone:
                self.level.doSwitch(t)
                self.switchDone = True
            return False
        elif t == self.level.doorClosed:
            self.openDoor(x, y)
        elif t == self.level.keyNo:
            self.newKey(x, y)
        elif t == self.level.heartNo:
            self.newLife(x, y)
        elif t == self.level.point1:
            self.incPoints(x, y, 10)
        elif t == self.level.point2:
            self.incPoints(x, y, 20)
        elif t == self.level.point3:
            self.incPoints(x, y, 30)
        elif t == self.level.point4:
            self.incPoints(x, y, 40)
        elif t == self.level.point5:
            self.incPoints(x, y, 50)
        elif t == self.level.point6:
            self.incPoints(x, y, 60)
        elif t == self.level.point7:
            self.incPoints(x, y, 70)
        elif t == self.level.point8:
            self.incPoints(x, y, 80)
        elif t == self.level.clockNo:
            self.getClock(x, y)
        elif t == self.level.redBottle:
            self.getRedBottle(x, y)
        elif t == self.level.greenBottle:
            self.getGreenBottle(x, y)
        elif t == self.level.blueBottle:
            self.getBlueBottle(x, y)
        else:
            return False
        return True

    def newLife(self, x, y):
        self.lives += 1
        self.level.frontData[y][x] = 0
        self.printLives()
        if self.soundAvailable:
            self.level.heartSnd.play()

    def incPoints(self, x, y, p):
        self.level.frontData[y][x] = 0
        self.points += p
        self.printScore()
        if self.soundAvailable:
            self.level.pointSnd.play()

    def newKey(self, x, y):
        if self.keys < 4:
            self.keys += 1
            self.level.frontData[y][x] = 0
            self.screen.blit(self.level.keyGfx, (489 + (self.keys*24), 107))
            if self.soundAvailable:
                self.level.keySnd.play()

    def openDoor(self, x, y):
        if self.keys > 0:
            self.screen.blit(self.level.infopanelGfx, (489 + (self.keys*24), 107), (33,107,20,20))
            self.keys -= 1
            self.level.frontData[y][x] = self.level.doorOpened
            if self.soundAvailable:
                self.level.doorSnd.play()

    def getClock(self, x, y):
        self.level.frontData[y][x] = 0
        if self.soundAvailable:
            self.level.clockSnd.play()
        for e in self.level.enemies:
            e.sleep()

    def getRedBottle(self, x, y):
        self.level.frontData[y][x] = 0
        self.shieldTime = 200
        if self.soundAvailable:
            self.level.bottleSnd.play()
 
    def getGreenBottle(self, x, y):
        self.level.frontData[y][x] = 0
        if self.shieldTime == 0:
            self.poisonedTime = 100
            if (self.horizontalMovement > 0) or (self.lastHorizontal > 0):
                self.animList = self.poisonLeftAnim
            elif (self.horizontalMovement < 0) or (self.lastHorizontal < 0):
                self.animList = self.poisonRightAnim
            self.animFrame = 0
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = 0
        if self.soundAvailable:
            self.level.bottleSnd.play()
 
    def getBlueBottle(self, x, y):
        self.level.frontData[y][x] = 0
        self.blocksMax = 16
        self.blocks += 4
        if self.blocks > self.blocksMax:
            self.blocks = self.blocksMax
        self.displayBlocks()
        if self.soundAvailable:
            self.level.bottleSnd.play()
 
