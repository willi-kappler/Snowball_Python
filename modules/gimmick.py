import random
import pygame
import gfxobject

class Gimmick:
    "Class for the funny gimmicks. Note that it doesn't use any of the gfxobject classes"
    def __init__(self, screen, level):
        self.screen = screen
        self.level = level
        self.tux = gfxobject.GFXObject(screen, level, level.playerGfx, 0, 0)
        self.firedevil = gfxobject.GFXObject(screen, level, level.firedevilGfx, 0, 0)
        self.ghost = gfxobject.GFXObject(screen, level, level.ghostGfx, 0, 0)
        self.skull = gfxobject.GFXObject(screen, level, level.skullGfx, 0, 0)
        self.zombie = gfxobject.GFXObject(screen, level, level.zombieGfx, 0, 0)

        self.doSequence = [None, self.seq1, self.seq2, self.seq3, self.seq4]
        self.prepareSequence = [None, self.prepareSeq1, self.prepareSeq2, self.prepareSeq3, self.prepareSeq4]

        self.sequence = 0

        self.time = 0

    def prepareSeq1(self):
        self.tux.x = -32
        self.tux.y = 416
        self.tux.animList1 = [(10, 80), (11, 80), (12, 80), (13, 80)]
        self.tux.animList2 = [(14,80)]
        self.tux.animList = self.tux.animList1
        self.tux.animFrame = 0
        self.tux.mode = 0
        self.tux.step = 20

        self.firedevil.x = -96
        self.firedevil.y = 416
        self.firedevil.animList = [(5, 80), (6, 80), (7, 80), (8, 80)]
        self.firedevil.animFrame = 0
        self.firedevil.mode = 0

        self.ground = [1,0,0,0,0,0,0]

    def prepareSeq2(self):
        self.skull.x = 512
        self.skull.y = 416
        self.skull.animList1 = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.skull.animList2 = [(5, 80), (6, 80), (7, 80), (8, 80)]
        self.skull.animList = self.skull.animList1
        self.skull.animFrame = 0
        self.skull.mode = 0
        self.skull.step = 40

        self.ghost.x = 640
        self.ghost.y = 416
        self.ghost.animList1 = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.ghost.animList2 = [(5, 80), (6, 80), (7, 80), (8, 80)]
        self.ghost.animList = self.ghost.animList1
        self.ghost.animFrame = 0
        self.ghost.mode = 0

        self.ground = []
        self.ground.append([self.level.greenBottle, self.level.doorClosed, 0, 0, 0, 0])
        self.ground.append([2, 2, 2, 2, 2, 2])

    def prepareSeq3(self):
        self.skull.x = 544
        self.skull.y = 416
        self.skull.animList1 = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.skull.animList2 = [(5, 80), (6, 80), (7, 80), (8, 80)]
        self.skull.animList = self.skull.animList1
        self.skull.animFrame = 0
        self.skull.mode = 0

        self.zombie.x = 0
        self.zombie.y = 416
        self.zombie.animList1 = [(0, 80), (1, 80), (2, 80), (3, 80)]
        self.zombie.animList2 = [(5, 80), (6, 80), (7, 80), (8, 80)]
        self.zombie.animList = self.zombie.animList2
        self.zombie.animFrame = 0
        self.zombie.mode = 0

        self.leftGround = []
        self.leftGround.append([1, 1, 1, self.level.spikeNo + 2, 0])
        self.leftGround.append([0, 0, 0, self.level.doorOpened + 1, self.level.heartNo + 1])
        self.leftGround.append([2, 2, 2, self.level.spikeNo + 1, 2])

        self.ground = []
        self.ground.append([0, 0, self.level.switchMin])
        self.ground.append([2, 2, 2])

    def prepareSeq4(self):
        pass

    def seq1(self): # tux and firedevil
        if self.tux.mode == 0:
            self.tux.x += 2
            self.tux.step -= 1
            if self.tux.step == 0:
                self.tux.mode = 1
                self.tux.animList = self.tux.animList2
                self.tux.animFrame = 0
                self.tux.step = 8
                self.ground[(self.tux.x / 32) + 1] = 1 # put blocks on ground
                self.firedevil.mode = 1
                if self.firedevil.x > 32:
                    self.ground[(self.firedevil.x / 32) - 1] = 0 # take blocks from ground
            if self.tux.x > 160:
                self.tux.mode = 2
                self.firedevil.mode = 1
                self.tux.animList = [(0, 80)] # turn around
                self.tux.animFrame = 0
                self.tux.step = 32 # and wait
                self.firedevil.animList = [(5, 80)]
                self.firedevil.animFrame = 0
        elif self.tux.mode == 1:
            self.tux.step -= 1 # wait and bow
            if self.tux.step == 0:
                self.tux.mode = 0
                self.tux.animList = self.tux.animList1 # move on
                self.tux.animFrame = 0
                self.tux.step = 16
                self.firedevil.mode = 0
        elif self.tux.mode == 2:
            self.tux.step -= 1 # wait
            if self.tux.step == 0:
                self.tux.mode = 3
                self.tux.step = 32
        elif self.tux.mode == 3:
            self.screen.blit(self.level.frontGfx[self.level.heartNo], (140, 400)) # show heart
            self.tux.step -= 1 # and wait
            if self.tux.step == 0:
                self.tux.mode = 4
                self.tux.animList = [(0, 80), (1, 80), (2, 80), (3, 80)]
                self.tux.animFrame = 0
                self.firedevil.mode = 2
                self.firedevil.animList = [(0, 80), (1, 80), (2, 80), (3, 80)]
                self.firedevil.animFrame = 0
        elif self.tux.mode == 4:
            self.tux.x -= 6 # you know what you want.... go and get it!
            if self.tux.x > 0:
                self.ground[(self.tux.x / 32) + 1] = 0 # remove blocks
            else:
                self.sequence = 0
                self.time = pygame.time.get_ticks()

        self.tux.go()

        if self.firedevil.mode == 0:
            self.firedevil.x += 2
        elif self.firedevil.mode == 2:
            self.firedevil.x -= 6 # run for your life!
            if self.firedevil.x > 32:
                self.ground[(self.firedevil.x / 32) - 1] = 1 # put blocks

        self.firedevil.go()

        for i in range(6):
            if self.ground[i] == 1:
                self.screen.blit(self.level.frontGfx[1], (i*32, 448))

    def seq2(self): # skull and ghost
        for i in range(6):
            if self.ground[0][i] > 0:
                self.screen.blit(self.level.frontGfx[self.ground[0][i]], (448 + (i*32), 416))
            if self.ground[1][i] > 0:
                self.screen.blit(self.level.frontGfx[self.ground[1][i]], (448 + (i*32), 448))

        if self.skull.mode == 1:
            self.skull.step -= 1 # wait in front of the door
            if self.skull.step == 0:
                self.skull.mode = 2
                self.skull.animList = self.skull.animList2 # turn around
                self.skull.animFrame = 0
        elif self.skull.mode == 2:
            self.skull.x += 2 # move to ghost
            if self.skull.x >= 580:
                self.skull.mode = 3
                self.skull.step = 40
        elif self.skull.mode == 3:
            self.skull.step -= 1 # babble a lot of stuff meaningless stuff to ghost
            if self.skull.step == 0:
                self.skull.mode = 0 # wait
                self.skull.animList = [(1, 80)] # turn around
                self.skull.animFrame = 0
                self.ghost.mode = 2
        elif self.skull.mode == 4:
            self.skull.step -= 1 # babble to ghost again...
            if self.skull.step == 0:
                self.skull.mode = 0 # wait
                self.skull.animList = [(1, 80)]
                self.skull.animFrame = 0
                self.ghost.mode = 4
                self.ghost.animList = self.ghost.animList1
                self.ghost.animFrame = 0
        elif self.skull.mode == 5:
            self.skull.x -= 2
            if self.skull.x <= 540:
                self.ground[0][3] = 0
                self.skull.mode = 0

        self.skull.go()

        if self.ghost.mode == 0:
            self.ghost.x -= 2 # sneek in
            if self.ghost.x <= 608:
                self.ghost.mode = 1
                self.skull.mode = 1
        elif self.ghost.mode == 2:
            self.ghost.x -= 2 # move to door
            if self.ghost.x <= 512:
                self.ghost.mode = 3 # wait
                self.skull.step = 30
        elif self.ghost.mode == 3:
            self.skull.step -= 1
            if self.skull.step == 0:
                self.ghost.mode = 1 # wait
                self.ghost.animList = self.ghost.animList2 # turn around
                self.ghost.animFrame = 0
                self.skull.step = 30
                self.skull.mode = 4
                self.skull.animList = self.skull.animList1
                self.skull.animFrame = 0
        elif self.ghost.mode == 4:
            self.ghost.x -= 2
            if self.ghost.x <= 448:
                self.ghost.mode = 5
                self.skull.step = 30
        elif self.ghost.mode == 5:
            self.skull.step -= 1
            if self.skull.step == 0:
                self.ground[0][0] = 0
                self.ghost.mode = 6
                self.ghost.animList = self.ghost.animList2
                self.ghost.animFrame = 0
                self.skull.animList = self.skull.animList1
                self.skull.animFrame = 0
        elif self.ghost.mode == 6:
            self.ghost.x += 2
            if self.ghost.x >= 548:
                self.ground[0][3] = self.level.greenBottle
                self.ghost.mode = 7
                self.skull.mode = 5
        elif self.ghost.mode == 7:
            self.ghost.x += 2
            if self.ghost.x >= 640:
                self.sequence = 0
                self.time = pygame.time.get_ticks()

        self.ghost.go()

    def seq3(self): # zombie and skull
        for i in range(5):
            if self.leftGround[0][i] > 0:
                self.screen.blit(self.level.frontGfx[self.leftGround[0][i]],  (i*32, 384))
            if self.leftGround[1][i] > 0:
                self.screen.blit(self.level.frontGfx[self.leftGround[1][i]], (i*32, 416))
            if self.leftGround[2][i] > 0:
                self.screen.blit(self.level.frontGfx[self.leftGround[2][i]], (i*32, 448))

        for i in range(3):
            if self.ground[0][i] > 0:
                self.screen.blit(self.level.frontGfx[self.ground[0][i]], (544 + (i*32), 416))
            if self.ground[1][i] > 0:
                self.screen.blit(self.level.frontGfx[self.ground[1][i]], (544 + (i*32), 448))

        if self.skull.mode == 1: # fast! got to the switch! the stupid zombie is comming...
            self.skull.x += 2
            if self.skull.x >= 580:
                self.skull.mode = 2
                self.skull.animList = self.skull.animList1
                self.skull.animFrame = 0
                self.leftGround[1][3] = self.level.redOn
        if self.skull.mode == 2: # go back and enjoy the show
            self.skull.x -= 2
            if self.skull.x <= 544:
                self.skull.mode = 0 # wait
        if self.skull.mode == 3: # one more time...
            self.skull.x += 2
            if self.skull.x >= 580:
                self.skull.mode = 2
                self.skull.animList = self.skull.animList1
                self.skull.animFrame = 0
                self.leftGround[1][3] = self.level.doorOpened + 1

        self.skull.go()

        if self.zombie.mode == 0: # nice shiny coin! zombie want coin! zombie must have coin!
            self.zombie.x += 1
            if self.zombie.x == 32:
                self.skull.mode = 1
                self.skull.animList = self.skull.animList2
                self.skull.animFrame = 0
            elif self.zombie.x == 64:
                self.zombie.mode = 1
                self.zombie.animList = self.zombie.animList1
                self.zombie.animFrame = 0
        elif self.zombie.mode == 1: # arrgh! turn around and move back... zombie no coin...
            self.zombie.x -= 1
            if self.zombie.x == 32:
                self.skull.mode = 3
                self.skull.animList = self.skull.animList2
                self.skull.animFrame = 0
            elif self.zombie.x == 0:
                self.zombie.mode = 2
                self.zombie.animList = self.zombie.animList2
                self.zombie.animFrame = 0
        elif self.zombie.mode == 2: # coin there again! zombie want coin!
            self.zombie.x += 1
            if self.zombie.x == 32:
                self.skull.mode = 1
                self.skull.animList = self.skull.animList2
                self.skull.animFrame = 0
            elif self.zombie.x == 64:
                self.zombie.mode = 3
                self.zombie.animList = self.zombie.animList1
                self.zombie.animFrame = 0
        elif self.zombie.mode == 3: # zombie go home... zombie no want play...
            self.zombie.x -= 1
            if self.zombie.x == 32:
                self.zombie.mode = 4
                self.zombie.animList = [(5, 80)]
                self.zombie.animFrame = 0
                self.zombie.step = 30
        elif self.zombie.mode == 4: # coin ?? coin ?? no coin....
            self.zombie.step -= 1
            if self.zombie.step == 0:
                self.zombie.mode = 5
                self.zombie.animList = self.zombie.animList1
                self.zombie.animFrame = 0
        elif self.zombie.mode == 5: # zombie away...
            self.zombie.x -= 1
            if self.zombie.x == -16:
                self.sequence = 0
                self.time = pygame.time.get_ticks()

        self.zombie.go()

    def seq4(self):
        pass

    def reset(self):
        self.sequence = 0
        self.time = pygame.time.get_ticks()

    def go(self):
        if self.sequence == 0:
            if pygame.time.get_ticks() > self.time + 5000:
                self.time = pygame.time.get_ticks()
                self.sequence = random.randint(0, 3)
                if self.sequence > 0:
                    self.prepareSequence[self.sequence]()
        else:
            self.doSequence[self.sequence]()

