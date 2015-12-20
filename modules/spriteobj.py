import random
import pygame
import movingobj
import boxobj
import liftobj
import trapobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class SpriteObj(movingobj.MovingObj):
    "The main class for the player, snowball and all the enemies"
    def __init__(self, screen, level, gfx, x, y):
        movingobj.MovingObj.__init__(self, screen, level, gfx, x, y)

        self.speed = 2

        self.restoreBG = self.restoreBG1

        self.sleeping = False
        self.jumpCounter = 18

        self.stopAnim = [(0, 10), (0, 10)]
        self.movingUpAnim = self.stopAnim
        self.movingDownAnim = self.stopAnim
        self.movingLeftAnim = self.stopAnim
        self.movingRightAnim = self.stopAnim
        self.turningLeftAnim = self.stopAnim
        self.turningRightAnim = self.stopAnim
        self.lookingLeftAnim = self.stopAnim
        self.lookingRightAnim = self.stopAnim
        self.fallingLeftAnim = self.stopAnim
        self.fallingRightAnim = self.stopAnim
        self.jumpingLeftAnim = self.stopAnim
        self.jumpingRightAnim = self.stopAnim
        self.sleepingAnim = self.stopAnim
        self.climbAnim = self.stopAnim

        self.sleepTime = 0
        self.sleepMax = 0
        self.transporterCycle = 0
        self.liftCounter = 0

        self.soundAvailable = True
        if pygame.mixer.get_init() == None:
            self.soundAvailable = False

    def moveUp(self):
        if self.verticalMovement != self.movingUp:
            self.lastVertical = self.verticalMovement
            self.verticalMovement = self.movingUp
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = 0
            self.animList = self.movingUpAnim
            self.animFrame = 0

    def moveDown(self):
        if self.verticalMovement != self.movingDown:
            self.lastVertical = self.verticalMovement
            self.verticalMovement = self.movingDown
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = 0
            self.animList = self.movingDownAnim
            self.animFrame = 0

    def moveLeft(self):
        if self.horizontalMovement != self.movingLeft:
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = self.movingLeft
            if self.verticalMovement == self.jumping:
                self.animList = self.jumpingLeftAnim
            elif self.verticalMovement == self.falling:
                self.animList = self.fallingLeftAnim
            else:
                self.animList = self.movingLeftAnim
            self.animFrame = 0

    def moveRight(self):
        if self.horizontalMovement != self.movingRight:
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = self.movingRight
            if self.verticalMovement == self.jumping:
                self.animList = self.jumpingRightAnim
            elif self.verticalMovement == self.falling:
                self.animList = self.fallingRightAnim
            else:
                self.animList = self.movingRightAnim
            self.animFrame = 0

    def turnLeft(self):
        if self.horizontalMovement != self.turningLeft:
            self.animFinished = False
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = self.turningLeft
            self.animList = self.turningLeftAnim
            self.animFrame = 0

    def turnRight(self):
        if self.horizontalMovement != self.turningRight:
            self.animFinished = False
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = self.turningRight
            self.animList = self.turningRightAnim
            self.animFrame = 0

    def lookLeft(self):
        if self.horizontalMovement != self.lookingLeft:
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = self.lookingLeft
            self.animList = self.lookingLeftAnim
            self.animFrame = 0

    def lookRight(self):
        if self.horizontalMovement != self.lookingRight:
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = self.lookingRight
            self.animList = self.lookingRightAnim
            self.animFrame = 0

    def fall(self):
        if self.verticalMovement != self.falling:
            self.lastVertical = self.verticalMovement
            self.verticalMovement = self.falling
            if (self.horizontalMovement < 0) or (self.lastHorizontal < 0):
                self.animList = self.fallingLeftAnim
            if (self.horizontalMovement > 0) or (self.lastHorizontal > 0):
                self.animList = self.fallingRightAnim
            self.animFrame = 0

    def jump(self):
        if self.verticalMovement != self.jumping:
            self.lastVertical = self.verticalMovement
            self.verticalMovement = self.jumping
            if (self.horizontalMovement < 0) or (self.lastHorizontal < 0):
                self.animList = self.jumpingLeftAnim
            if (self.horizontalMovement > 0) or (self.lastHorizontal > 0):
                self.animList = self.jumpingRightAnim
            self.animFrame = 0
            self.jumpCounter = 18

    def stop(self):
        if (self.horizontalMovement != 0) or (self.verticalMovement != 0):
            self.lastHorizontal = self.horizontalMovement
            self.lastVertical = self.verticalMovement
            self.horizontalMovement = 0
            self.verticalMovement = 0
            self.animList = self.stopAnim
            self.animFrame = 0

    def stopFalling(self):
        self.lastVertical = self.falling
        self.verticalMovement = 0

    def stopLift(self):
        self.lastVertical = self.usingLift
        self.verticalMovement = 0

    def climbUp(self):
        if self.verticalMovement != self.climbingUp:
            self.lastVertical = self.verticalMovement
            self.verticalMovement = self.climbingUp
            self.animList = self.climbAnim
            self.animFrame = 0

    def climbDown(self):
        if self.verticalMovement != self.climbingDown:
            self.lastVertical = self.verticalMovement
            self.verticalMovement = self.climbingDown
            self.animList = self.climbAnim
            self.animFrame = 0

    def resetHorizontalMovement(self):
        if self.horizontalMovement == self.movingLeft:
            self.animList = self.movingLeftAnim
            self.animFrame = 0
        elif self.horizontalMovement == self.lookingLeft:
            self.animList = self.lookingLeftAnim
            self.animFrame = 0
        elif self.horizontalMovement == self.movingRight:
            self.animList = self.movingRightAnim
            self.animFrame = 0
        elif self.horizontalMovement == self.lookingRight:
            self.animList = self.lookingRightAnim
            self.animFrame = 0

    def sleep(self):
        pass

    def sleep1(self):
        if not self.sleeping:
            self.lastHorizontal = self.horizontalMovement
            self.horizontalMovement = 0
            self.sleeping = True
            self.animList = self.sleepingAnim
            self.animFrame = 0
            self.sleepTime = pygame.time.get_ticks()

    def move1(self): # all sprites
        if self.horizontalMovement == self.movingRight:
            if self.x < 448 - self.speed:
                self.x += self.speed
            else:
                self.x = 448
                self.turnLeft()

        elif self.horizontalMovement == self.movingLeft:
            if self.x > self.speed:
                self.x -= self.speed
            else:
                self.x = 0
                self.turnRight()

        elif self.horizontalMovement == self.turningLeft:
            if self.animFinished:
                self.moveLeft()

        elif self.horizontalMovement == self.turningRight:
            if self.animFinished:
                self.moveRight()

    def move2(self): # ghost movement
        if self.verticalMovement == self.movingUp:
            if self.y > self.speed:
                self.y -= self.speed
            else:
                self.y = 0
                self.moveDown()

        elif self.verticalMovement == self.movingDown:
            if self.y < 448 - self.speed:
                self.y += self.speed
            else:
                self.y = 448
                self.moveUp()

        self.move1()

    def move3(self): # shredder, snowball movement
        if self.verticalMovement == self.falling:
            if self.y < 444:
                self.y += 4
            else:
                self.y = 448
                self.lastVertical = self.falling
                self.verticalMovement = 0
                if self.lastHorizontal < 0:
                    self.moveLeft()
                elif self.lastHorizontal > 0:
                    self.moveRight()

        elif self.verticalMovement == self.usingLift:
            if self.y > 0:
                self.y -= 4
                self.liftCounter -= 4
                if self.liftCounter <= 0:
                    self.lastVertical = self.usingLift
                    self.verticalMovement = 0
                    self.y = (self.y / 32) * 32 # sane y coordinate
                    if self.lastHorizontal < 0:
                        self.moveLeft()
                    elif self.lastHorizontal > 0:
                        self.moveRight()
            else:
                self.y = 0
                self.lastVertical = self.usingLift
                self.verticalMovement = 0
                self.y = (self.y / 32) * 32 # sane y coordinate
                if self.lastHorizontal < 0:
                    self.moveLeft()
                elif self.lastHorizontal > 0:
                    self.moveRight()
        self.move1()

    def move4(self): # skull, spider, firedevil, zombie movement
        if self.sleeping:
            if pygame.time.get_ticks() > self.sleepTime + self.sleepMax:
                self.sleeping = False
                if self.lastHorizontal < 0:
                    self.moveLeft()
                elif self.lastHorizontal > 0:
                    self.moveRight()
        self.move3()

    def checkFalling(self):
        if self.wallDown():
            self.y = (self.y / 32) * 32 # sane y coordinate
            self.lastVertical = self.falling
            self.verticalMovement = 0
            if self.lastHorizontal < 0:
                self.moveLeft()
            elif self.lastHorizontal > 0:
                self.moveRight()

    def teleport(self):
        (nx, ny) = self.level.transporters[self.transporterCycle]
        for i in range(len(self.level.transporters)):
            t = self.level.frontData[ny][nx]
            if ((t == 0) or (t >= self.level.doorOpened)) and ((nx != self.midX) or (ny != self.midY)):
                break
            self.transporterCycle += 1
            if self.transporterCycle == len(self.level.transporters):
                self.transporterCycle = 0
            (nx, ny) = self.level.transporters[self.transporterCycle]

        self.restoreBG()
        self.x = nx * 32
        self.y = ny * 32
        self.transporterCycle += 1
        if self.transporterCycle == len(self.level.transporters):
            self.transporterCycle = 0
        if self.soundAvailable:
            self.level.transporterSnd.play()

    def moveBoxLeft(self):
        bllt = self.bottomLeftLeftTile()
        if (self.leftLeftTile() == 0) and ((bllt > 0) and (bllt < self.level.keyNo)):
            if self.midX > 2:
                if (self.midY == self.level.snowball.midY) and (self.midX - 2 == self.level.snowball.midX):
                    return
                if (self.midY == self.level.player.midY) and (self.midX - 2 == self.level.player.midX):
                    return
                for e in self.level.enemies:
                    if (self.midY == e.midY) and (self.midX - 2 == e.midX):
                        return
            self.level.frontData[self.midY][self.leftSpotOut] = self.level.invisible
            self.level.frontData[self.midY][self.leftSpotOut - 1] = self.level.invisible
            self.level.movingObj.append(boxobj.BoxObj(self.screen, self.level, [self.level.frontGfx[self.level.boxNo]], self.leftSpotOut * 32, self.midY * 32, self.movingLeft))
            if self.soundAvailable:
                self.level.boxSnd.play()

    def moveBoxRight(self):
        brrt = self.bottomRightRightTile()
        if (self.rightRightTile() == 0) and ((brrt > 0) and (brrt < self.level.keyNo)):
            if self.midX <= 12:
                if (self.midY == self.level.snowball.midY) and (self.midX + 2 == self.level.snowball.midX):
                    return
                if (self.midY == self.level.player.midY) and (self.midX + 2 == self.level.player.midX):
                    return
                for e in self.level.enemies:
                    if (self.midY == e.midY) and (self.midX + 2 == e.midX):
                        return
            self.level.frontData[self.midY][self.rightSpotOut] = self.level.invisible
            self.level.frontData[self.midY][self.rightSpotOut + 1] = self.level.invisible
            self.level.movingObj.append(boxobj.BoxObj(self.screen, self.level, [self.level.frontGfx[self.level.boxNo]], self.rightSpotOut * 32, self.midY * 32, self.movingRight))
            if self.soundAvailable:
                self.level.boxSnd.play()

    def checkBottom1(self):
        bt = self.bottomTile()
        if (bt == self.level.liftNo):
            self.useLift()
        elif bt == self.level.brickNo:
            self.breakBrick1()
        elif bt == self.level.brickBrokenNo:
            self.breakBrick2()
        elif not self.wallDown():
            self.stop()
            self.fall()

    def checkBottom2(self):
        if not self.wallDown():
            self.stop()
            self.fall()

    def checkTrap(self, tile, x):
        if (tile == self.level.trapNo) and (self.centerTile() != self.level.trapNo):
            self.level.frontData[self.midY][x] = self.level.invisible
            self.level.staticObj.append(trapobj.TrapObj(self.screen, self.level, self.level.trapGfx, x * 32, self.midY * 32))
            if self.soundAvailable:
                self.level.trapSnd.play()

    def breakBrick1(self):
        x = self.midX
        y = self.bottomSpotOut
        bt = self.level.brick1Timers[(x,y)]
        if bt >= 50:
            self.level.brick2Timers[(x,y)] = 0
            self.level.frontData[y][x] = self.level.brickBrokenNo
            self.level.displayXY(x, y)
            if self.soundAvailable:
                self.level.brickSnd.play()
        else:
            self.level.brick1Timers[(x,y)] = bt + 1

    def breakBrick2(self):
        x = self.midX
        y = self.bottomSpotOut
        bt = self.level.brick2Timers[(x,y)]
        if bt >= 50:
            self.level.frontData[y][x] = 0
            self.level.displayXY(x, y)
            if self.soundAvailable:
                self.level.brickSnd.play()
        else:
            self.level.brick2Timers[(x,y)] = bt + 1

    def useLift(self, stoping = True):
        tt = self.topTile()
        if ((tt == 0) or (tt >= self.level.keyNo)):
            x = self.midX
            y = self.bottomSpotOut
            lt = self.level.liftTimers[(x,y)]
            t = pygame.time.get_ticks()
            if  t > lt + 4000:
                if self != self.level.player:
                    if (self.midX == self.level.player.midX) and (self.midY == self.level.player.midY):
                        self.level.player.liftCounter = 32
                        self.level.player.verticalMovement = self.usingLift
                if self != self.level.snowball:
                    if (self.midX == self.level.snowball.midX) and (self.midY == self.level.snowball.midY):
                        self.level.snowball.liftCounter = 32
                        self.level.snowball.stop()
                        self.level.snowball.verticalMovement = self.usingLift
                for e in self.level.enemies:
                    if self != e:
                        if (self.midX == e.midX) and (self.midY == e.midY):
                            e.liftCounter = 32
                            e.stop()
                            e.verticalMovement = self.usingLift
                            print e

                self.level.liftTimers[(x,y - 1)] = t
                del self.level.liftTimers[(x,y)]
                self.liftCounter = 32
                if stoping:
                    self.stop()
                self.verticalMovement = self.usingLift
                self.level.frontData[y][x] = self.level.liftBarNo
                self.level.movingObj.append(liftobj.LiftObj(self.screen, self.level, [self.level.frontGfx[self.level.liftNo]], x * 32, y * 32))
                if self.soundAvailable:
                    self.level.liftSnd.play()


