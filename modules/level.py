import pygame
import playerobj
import snowballobj
import skullobj
import ghostobj
import shredderobj
import zombieobj
import firedevilobj
import spiderobj
import circsawobj

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Level:
    "The main class for the game. Graphics, sounds, etc. are managed here."
    def __init__(self, screen, font, options):
        self.screen = screen
        self.black = (0,0,0)
        self.level = 1
        self.beginLevel = 1
        self.maxLevel = 1
        self.font = font
        self.options = options
        self.lastLevel = 51
        self.backData = []
        self.frontData = []
        self.playerX = 0
        self.playerY = 0
        self.snowballX = 1
        self.snowballY = 0
        self.quitGame = False
        self.enemies = []
        self.staticObj = []
        self.movingObj = []
        self.transporters = []
        self.brick1Timers = {}
        self.brick2Timers = {}
        self.liftTimers = {}
        self.clock = pygame.time.Clock()

        self.backGfx = []
        self.loadGfx(self.backGfx, "backgrounds.png", 4, 8)

        self.frontGfx = [None]
        self.loadGfx(self.frontGfx, "walls.png", 7, 8)
        self.exitNo = 9
        self.boxNo = self.exitNo + 1
        self.spikeNo = self.boxNo + 1
        self.redOn = self.spikeNo + 3
        self.yellowOn = self.redOn + 1
        self.greenOn = self.yellowOn + 1
        self.blueOn = self.greenOn + 1
        self.cyanOn = self.blueOn + 1
        self.mangentaOn = self.cyanOn + 1
        self.switchMin = self.mangentaOn + 1
        self.switchMax = self.switchMin + 20
        self.transporterNo = self.switchMax + 1
        self.doorClosed = self.transporterNo + 1
        self.liftNo = self.doorClosed + 1
        self.liftBarNo = self.liftNo + 1
        self.brickNo = self.liftBarNo + 1
        self.brickBrokenNo = self.brickNo + 1
        self.trapClosed = self.brickBrokenNo + 1
        self.circSaw = self.trapClosed + 1
        self.invisible = self.circSaw + 1
        self.invisibleDanger = self.invisible + 1

        self.objNo = len(self.frontGfx)
        self.loadGfx(self.frontGfx, "objects.png", 3, 8)
        self.doorOpened = self.objNo
        self.redOff = self.doorOpened + 1
        self.yellowOff = self.redOff + 1
        self.greenOff = self.yellowOff + 1
        self.blueOff = self.greenOff + 1
        self.cyanOff = self.blueOff + 1
        self.mangentaOff =  self.cyanOff + 1
        self.trapNo = self.mangentaOff + 1
        self.ladder1 = self.trapNo + 1
        self.ladder2 = self.ladder1 + 1
        self.keyNo = self.ladder2 + 1
        self.heartNo = self.keyNo + 1
        self.point1 = self.heartNo + 1
        self.point2 = self.point1 + 1
        self.point3 = self.point2 + 1
        self.point4 = self.point3 + 1
        self.point5 = self.point4 + 1
        self.point6 = self.point5 + 1
        self.point7 = self.point6 + 1
        self.point8 = self.point7 + 1
        self.clockNo = self.point8 + 1
        self.redBottle = self.clockNo + 1
        self.greenBottle = self.redBottle + 1
        self.blueBottle = self.greenBottle + 1

        self.switches = [(self.redOn, self.redOff, -1, -1),(self.redOn, self.redOff, self.yellowOn, self.yellowOff),(self.redOn, self.redOff, self.greenOn, self.greenOff),(self.redOn, self.redOff, self.blueOn, self.blueOff),(self.redOn, self.redOff, self.cyanOn, self.cyanOff),(self.redOn, self.redOff, self.mangentaOn, self.mangentaOff)]
        self.switches += [(self.yellowOn, self.yellowOff, -1, -1),(self.yellowOn, self.yellowOff, self.greenOn, self.greenOff),(self.yellowOn, self.yellowOff, self.blueOn, self.blueOff),(self.yellowOn, self.yellowOff, self.cyanOn, self.cyanOff),(self.yellowOn, self.yellowOff, self.mangentaOn, self.mangentaOff)]
        self.switches += [(self.greenOn, self.greenOff, -1, -1),(self.greenOn, self.greenOff, self.blueOn, self.blueOff),(self.greenOn, self.greenOff, self.cyanOn, self.cyanOff),(self.greenOn, self.greenOff, self.mangentaOn, self.mangentaOff)]
        self.switches += [(self.blueOn, self.blueOff, -1, -1),(self.blueOn, self.blueOff, self.cyanOn, self.cyanOff),(self.blueOn, self.blueOff, self.mangentaOn, self.mangentaOff)]
        self.switches += [(self.cyanOn, self.cyanOff, -1, -1),(self.cyanOn, self.cyanOff, self.mangentaOn, self.mangentaOff)]
        self.switches += [(self.mangentaOn, self.mangentaOff, -1, -1)]

        self.playerNo = len(self.frontGfx)
        self.loadGfx(self.frontGfx, "player.png", 1, 1)

        self.snowballNo = self.playerNo + 1
        self.loadGfx(self.frontGfx, "snowball.png", 1, 1)

        self.skullNo = self.snowballNo + 1
        self.loadGfx(self.frontGfx, "skull.png", 1, 1)

        self.ghostNo = self.skullNo + 1
        self.loadGfx(self.frontGfx, "ghost.png", 1, 1)

        self.shredderNo = self.ghostNo + 1
        self.loadGfx(self.frontGfx, "shredder.png", 1, 1)

        self.zombieNo = self.shredderNo + 1
        self.loadGfx(self.frontGfx, "zombie.png", 1, 1)

        self.firedevilNo = self.zombieNo + 1
        self.loadGfx(self.frontGfx, "firedevil.png", 1, 1)

        self.enemies = []

        self.playerGfx = []
        self.loadGfx(self.playerGfx, "player.png", 3, 10)

        self.snowballGfx = []
        self.loadGfx(self.snowballGfx, "snowball.png", 1, 8)

        self.skullGfx = []
        self.loadGfx(self.skullGfx, "skull.png", 1, 9)

        self.ghostGfx = []
        self.loadGfx(self.ghostGfx, "ghost.png", 1, 10)

        self.shredderGfx = []
        self.loadGfx(self.shredderGfx, "shredder.png", 1, 9)

        self.zombieGfx = []
        self.loadGfx(self.zombieGfx, "zombie.png", 1, 9)

        self.firedevilGfx = []
        self.loadGfx(self.firedevilGfx, "firedevil.png", 1, 9)

        self.spiderGfx = []
#        self.loadGfx(self.spiderGfx, "spider.png", 1, x)

        self.trapGfx = []
        self.loadGfx(self.trapGfx, "trap.png", 1, 3)

        self.circsawGfx = []
        self.loadGfx(self.circsawGfx, "circsaw.png", 1, 8)

        self.gameOverGfx = pygame.image.load("gfx/gameover.png")

        self.infopanelGfx = pygame.image.load("gfx/infopanel.png")

        self.keyGfx = pygame.image.load("gfx/key.png")

        self.soundAvailable = True
        if pygame.mixer.get_init() == None:
            self.soundAvailable = False
        else:
            self.playerDieSnd = pygame.mixer.Sound("snd/player_die.ogg")
            self.exitSnd = pygame.mixer.Sound("snd/exit.ogg")
            self.laserSnd = pygame.mixer.Sound("snd/laser.ogg")
            self.transporterSnd = pygame.mixer.Sound("snd/transporter.ogg")
            self.iceblockSnd = pygame.mixer.Sound("snd/iceblock.ogg")
            self.fillSnd = self.iceblockSnd
            self.keySnd = pygame.mixer.Sound("snd/key.ogg")
            self.doorSnd = pygame.mixer.Sound("snd/door.ogg")
            self.heartSnd = pygame.mixer.Sound("snd/heart.ogg")
            self.boxSnd = pygame.mixer.Sound("snd/box.ogg")
            self.pointSnd = pygame.mixer.Sound("snd/point.ogg")
            self.noBlocksSnd = pygame.mixer.Sound("snd/tick.ogg")
            self.clockSnd = pygame.mixer.Sound("snd/clock.ogg")
            self.liftSnd = pygame.mixer.Sound("snd/lift.ogg")
            self.trapSnd = pygame.mixer.Sound("snd/trap.ogg")
            self.brickSnd = pygame.mixer.Sound("snd/brick.ogg")
            self.bottleSnd = pygame.mixer.Sound("snd/bottle.ogg")

    def loadGfx(self, gfxList, name, row, col):
        lgfx = pygame.image.load("gfx/" + name)
        y = 0
        for i in range(row):
            x = 0
            for j in range(col):
                gfx = pygame.Surface((32,32), pygame.SWSURFACE, lgfx)
                gfx.blit(lgfx, (0,0), (x,y,32,32))
                gfxList.append(gfx)
                x += 33
            y += 33

    def load(self):
        self.backData = [[0 for j in range(15)] for i in range(15)]
        self.frontData = [[0 for j in range(15)] for i in range(15)]
        self.playerX = 0
        self.playerY = 0
        self.snowballX = 1
        self.snowballY = 0
        self.frontData[0][0] = self.playerNo
        self.frontData[0][1] = self.snowballNo

        filename = "levels/level" + str(self.level) + ".txt"
        try:
            handle = file(filename, "rt")
        except IOError:
            print "could not load file: ", filename
            return

        for y in range(15):
            line = handle.readline().split()
            for x in range(15):
                t = int(line[x])
                self.backData[y][x] = t

        handle.readline()

        for y in range(15):
            line = handle.readline().split()
            for x in range(15):
                t = int(line[x])
                self.frontData[y][x] = t
                if t == self.playerNo:
                    self.playerX = x
                    self.playerY = y
                elif t == self.snowballNo:
                    self.snowballX = x
                    self.snowballY = y

        handle.close()

    def save(self):
        filename = "levels/level" + str(self.level) + ".txt"
        try:
            handle = file(filename, "wt")
        except IOError:
            print "could not save file: ", filename
            return
        for y in range(15):
            for x in range(15):
                handle.write(str(self.backData[y][x]) + " ")
            handle.write("\n")

        handle.write("\n")

        for y in range(15):
            for x in range(15):
                handle.write(str(self.frontData[y][x]) + " ")
            handle.write("\n")

        handle.close()

    def clear(self, layer, t):
        if layer == 0 or layer == 2: # change background only
            for y in range(15):
                for x in range(15):
                    self.backData[y][x] = t
        else: # change foreground only
            for y in range(15):
                for x in range(15):
                    self.frontData[y][x] = t
            self.playerX = 0
            self.playerY = 0
            self.snowballX = 1
            self.snowballY = 0
            self.frontData[0][0] = self.playerNo
            self.frontData[0][1] = self.snowballNo

    def next(self):
        self.level += 1
        if self.level == self.lastLevel:
            self.level = 1
        self.load()

    def prev(self):
        self.level -= 1
        if self.level == 0:
            self.level = self.lastLevel - 1
        self.load()

    def set(self, layer, x, y, t):
        if layer == 0: # change background, background visible
            self.backData[y][x] = t
            self.screen.blit(self.backGfx[t], (x*32,y*32))
        elif layer == 1: # change foreground, foreground visible
            self.frontData[y][x] = t
            if t == 0:
                self.screen.blit(self.backGfx[0], (x*32,y*32))
            elif t == self.playerNo:
                if (self.playerX != x) or (self.playerY != y):
                    self.frontData[self.playerY][self.playerX] = 0
                    self.screen.blit(self.backGfx[0], (self.playerX*32,self.playerY*32))
                    self.screen.blit(self.backGfx[0], (x*32,y*32))
                    self.screen.blit(self.frontGfx[t], (x*32,y*32))
                    self.playerX = x
                    self.playerY = y
            elif t == self.snowballNo:
                if (self.snowballX != x) or (self.snowballY != y):
                    self.frontData[self.snowballY][self.snowballX] = 0
                    self.screen.blit(self.backGfx[0], (self.snowballX*32,self.snowballY*32))
                    self.screen.blit(self.backGfx[0], (x*32,y*32))
                    self.screen.blit(self.frontGfx[t], (x*32,y*32))
                    self.snowballX = x
                    self.snowballY = y
            else:
                self.screen.blit(self.backGfx[0], (x*32,y*32))
                self.screen.blit(self.frontGfx[t], (x*32,y*32))
        elif layer == 2: # change background, both visible
            self.backData[y][x] = t
            u = self.frontData[y][x]
            if u == 0:
                self.screen.blit(self.backGfx[t], (x*32,y*32))
            else:
                self.screen.blit(self.backGfx[t], (x*32,y*32))
                self.screen.blit(self.frontGfx[u], (x*32,y*32))
        elif layer == 3: # change foreground, both visible
            self.frontData[y][x] = t
            if t == 0:
                self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))
            elif t == self.playerNo:
                if (self.playerX != x) or (self.playerY != y):
                    self.frontData[self.playerY][self.playerX] = 0
                    self.screen.blit(self.backGfx[self.backData[self.playerY][self.playerX]], (self.playerX*32,self.playerY*32))
                    self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))
                    self.screen.blit(self.frontGfx[t], (x*32,y*32))
                    self.playerX = x
                    self.playerY = y
            elif t == self.snowballNo:
                if (self.snowballX != x) or (self.snowballY != y):
                    self.frontData[self.snowballY][self.snowballX] = 0
                    self.screen.blit(self.backGfx[self.backData[self.snowballY][self.snowballX]], (self.snowballX*32,self.snowballY*32))
                    self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))
                    self.screen.blit(self.frontGfx[t], (x*32,y*32))
                    self.snowballX = x
                    self.snowballY = y
            else:
                self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))
                self.screen.blit(self.frontGfx[t], (x*32,y*32))

    def display(self, layer):
        if layer == 0:
            for y in range(15):
                for x in range(15):
                    self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))
        elif layer == 1:
            for y in range(15):
                for x in range(15):
                    t = self.frontData[y][x]
                    if t == 0:
                        self.screen.blit(self.backGfx[0], (x*32,y*32))
                    else:
                        self.screen.blit(self.frontGfx[t], (x*32,y*32))

        elif layer == 2 or layer == 3:
            for y in range(15):
                for x in range(15):
                    t = self.frontData[y][x]
                    if t == 0:
                        self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))
                    else:
                        self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))
                        self.screen.blit(self.frontGfx[t], (x*32,y*32))

    def displayXY(self, x, y):
        self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))
        t = self.frontData[y][x]
        if (t > 0) and (t != self.invisible) and (t != self.invisibleDanger):
            self.screen.blit(self.frontGfx[t], (x*32,y*32))

    def displayXYBG(self, x, y):
        self.screen.blit(self.backGfx[self.backData[y][x]], (x*32,y*32))

    def go(self):
        for o in self.movingObj:
            o.restoreBG()
        for e in self.enemies:
            e.restoreBG()
        self.snowball.restoreBG()
        self.player.restoreBG()

        for o in self.staticObj:
            o.go()
        for o in self.movingObj:
            o.go()
        for e in self.enemies:
            e.go()
        self.snowball.go()
        self.player.go()

    def doSwitch(self, n):
        (on1, off1, on2, off2) = self.switches[n - self.switchMin]
        for y in range(15):
            for x in range(15):
                t = self.frontData[y][x]
                if t == on1:
                    self.frontData[y][x] = off1
                    self.displayXY(x,y)
                    if self.soundAvailable:
                        self.laserSnd.play()
                elif t == off1:
                    self.frontData[y][x] = on1
                    self.displayXY(x,y)
                    if self.soundAvailable:
                        self.laserSnd.play()
                elif t == on2:
                    self.frontData[y][x] = off2
                    self.displayXY(x,y)
                    if self.soundAvailable:
                        self.laserSnd.play()
                elif t == off2:
                    self.frontData[y][x] = on2
                    self.displayXY(x,y)
                    if self.soundAvailable:
                        self.laserSnd.play()

    def checkObj(self):
        self.transporters = []
        self.staticObj = []
        self.movingObj = []
        self.brick1Timers = {}
        self.brick2Timers = {}
        self.liftTimers = {}
        for y in range(15):
            for x in range(15):
                t = self.frontData[y][x]
                if t == 1:
                    if self.player.blocks > 0:
                        self.player.blocks -= 1
                elif t == self.transporterNo:
                    self.transporters.append((x,y - 1))
                elif t == self.brickNo:
                    self.brick1Timers[(x,y)] = 0
                elif t == self.brickBrokenNo:
                    self.brick2Timers[(x,y)] = 0
                elif t == self.liftNo:
                    self.liftTimers[(x,y)] = 0
                elif t == self.circSaw:
                    self.staticObj.append(circsawobj.CircSaw(self.screen, self, self.circsawGfx, x*32, y*32))
                    self.frontData[y][x] = 0

    def createEnemies(self):
        self.enemies = []
        for y in range(15):
            for x in range(15):
                t = self.frontData[y][x]
                if t == self.skullNo:
                    self.enemies.append(skullobj.Skull(self.screen, self, self.skullGfx, x*32, y*32))
                    self.frontData[y][x] = 0
                elif t == self.ghostNo:
                    self.enemies.append(ghostobj.Ghost(self.screen, self, self.ghostGfx, x*32, y*32))
                    self.frontData[y][x] = 0
                elif t == self.shredderNo:
                    self.enemies.append(shredderobj.Shredder(self.screen, self, self.shredderGfx, x*32, y*32))
                    self.frontData[y][x] = 0
                elif t == self.zombieNo:
                    self.enemies.append(zombieobj.Zombie(self.screen, self, self.zombieGfx, x*32, y*32))
                    self.frontData[y][x] = 0
                elif t == self.firedevilNo:
                    self.enemies.append(firedevilobj.Firedevil(self.screen, self, self.firedevilGfx, x*32, y*32))
                    self.frontData[y][x] = 0

    def fancyFill(self, mode):
        x = 7
        y = 7
        dx = 1
        dy = 1
        move = 0
        direction = 0
        displayCounter = 0
        if self.soundAvailable:
            self.fillSnd.play()
        while True:
            if mode == 0:
                self.displayXY(x,y)
            else:
                self.screen.blit(self.frontGfx[mode], (x*32,y*32))

            if (x == 0) and (y == 0):
                break

            if direction == 0:
                y -= 1
                move += 1
                if move == dy:
                    direction = 1
                    dy += 1
                    move = 0
            elif direction == 1:
                x += 1
                move += 1
                if move == dx:
                    direction = 2
                    dx += 1
                    move = 0
            elif direction == 2:
                y += 1
                move += 1
                if move == dy:
                    direction = 3
                    dy += 1
                    move = 0
            elif direction == 3:
                x -= 1
                move += 1
                if move == dx:
                    direction = 0
                    dx += 1
                    move = 0

            displayCounter += 1
            if displayCounter == 6:
                self.clock.tick(30)
                pygame.display.flip()
                displayCounter = 0

    def initDisplay(self):
        self.frontData[self.playerY][self.playerX] = 0
        self.frontData[self.snowballY][self.snowballX] = 0
        self.fancyFill(2)
        self.screen.blit(self.infopanelGfx, (480,0))
        self.fancyFill(0)
        self.font.write(530, 23, str(self.level), True)
        self.player.printLives()
        self.player.printScore()
        self.player.displayBlocks()

    def createObj(self):
        self.createEnemies()
        self.player = playerobj.Player(self.screen, self, self.playerGfx, self.playerX*32, self.playerY*32)
        self.snowball = snowballobj.Snowball(self.screen, self, self.snowballGfx, self.snowballX*32, self.snowballY*32)
        self.checkObj()
        self.initDisplay()

    def setSoundVol(self):
        if self.soundAvailable:
            self.playerDieSnd.set_volume(self.options.soundVol)
            self.exitSnd.set_volume(self.options.soundVol)
            self.laserSnd.set_volume(self.options.soundVol)
            self.transporterSnd.set_volume(self.options.soundVol)
            self.iceblockSnd.set_volume(self.options.soundVol)
            self.fillSnd.set_volume(self.options.soundVol)
            self.keySnd.set_volume(self.options.soundVol)
            self.doorSnd.set_volume(self.options.soundVol)
            self.heartSnd.set_volume(self.options.soundVol)
            self.boxSnd.set_volume(self.options.soundVol)
            self.pointSnd.set_volume(self.options.soundVol)
            self.noBlocksSnd.set_volume(self.options.soundVol)
            self.clockSnd.set_volume(self.options.soundVol)
            self.liftSnd.set_volume(self.options.soundVol)
            self.trapSnd.set_volume(self.options.soundVol)
            self.brickSnd.set_volume(self.options.soundVol)
            self.bottleSnd.set_volume(self.options.soundVol)

    def setMusicVol(self):
        pass

    def restart(self):
        self.createEnemies()
        self.player.x = self.playerX * 32
        self.player.y = self.playerY * 32
        self.snowball.x = self.snowballX * 32
        self.snowball.y = self.snowballY * 32
        self.player.resetStatus()
        self.snowball.stop()
        self.snowball.moveLeft()
        self.checkObj()
        self.initDisplay()

    def exitReached(self):
        self.player.points += 10
        if self.soundAvailable:
            self.exitSnd.play()
        self.next()
        self.restart()
