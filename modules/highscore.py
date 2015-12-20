import math
import pygame

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Highscore:
    "Class for the highscore and greetings. Loads, saves and manages the highscore entries"
    def __init__(self, screen):
        self.screen = screen
        self.points = [1000, 800, 500, 100, 50]
        self.names = ["W.KAPPLER", "W.KAPPLER", "W.KAPPLER", "W.KAPPLER", "W.KAPPLER"]
        self.black = (0, 0, 0)
        self.font = None
        self.font2 = None
        self.clock = pygame.time.Clock()
        self.greets = "                                                       GREETS TO: ACHIM - ALINE - ANDI - ANJA - ANNE-CAROLE - ANTHONY - BENNI - CARLOS - CHRISTIAN - CHRISTOPH - CLUBHAUS GANG - COSMO - DANIEL - DEPOT GANG - DIMA - DOMINIK - DORO - ELI - EVA - FACE HUGGER - FARI - FAST - FELIX - FLO - FRANK - GINTI - HEINER - HENNING - JAN - JARED - JENS - JOJO - JULIA - JULIUS - KARIN - KATRIN - LISA - LUIZ - MARKUS - MASTER BLASTER - MATZE - MICHI - MILO - NICI - QARC - PIT - RALF - SABINE - SANDRA - SANDY - SCHMID SISTERS - SHANTHY - SILVERSTAR - SIMON - STEFAN - STEFFI - THOMAS - UDO - VOLKI - WALDMEISTER - YANG - ZAPHOLD - ZED - ZEROZERO"
        self.greetsPos = 0

    def load(self):
        try:
            handle = file("highscore.txt", "rt")
        except IOError:
            print "couldn't load file: highscore.txt"
            return
        for i in range(5):
            l = handle.readline().split()
            self.points[i] = int(l[0])
            self.names[i] = l[1][:10].upper()

        handle.close()

    def save(self):
        try:
            handle = file("highscore.txt", "wt")
        except IOError:
            print "couldn't save file: highscore.txt"
            return
        for i in range(5):
            handle.write(str(self.points[i]) + " " + self.names[i].upper() + "\n")

        handle.close()

    def run(self):
        dx = -math.pi
        gx = 0
        self.screen.fill(self.black)
        self.font.write(320, 20, "HIGHSCORE:", True)
        while True:
            self.screen.fill(self.black, (0, 100, 640, 32))
            self.screen.fill(self.black, (0, 160, 640, 32))
            self.screen.fill(self.black, (0, 220, 640, 32))
            self.screen.fill(self.black, (0, 280, 640, 32))
            self.screen.fill(self.black, (0, 340, 640, 32))
            self.screen.fill(self.black, (0, 400, 640, 32))
            self.screen.fill(self.black, (0, 430, 640, 40))
            y = 100
            for i in range(5):
                if divmod(i, 2)[1] == 0:
                    self.font.write(320 + (math.sin(dx)*64), y, str(i+1) + " " + self.names[i] + " " + str(self.points[i]), True)
                else:
                    self.font.write(320 - (math.sin(dx)*64), y, str(i+1) + " " + self.names[i] + " " + str(self.points[i]), True)
                y += 60
                dx = dx + 0.01
                if dx >= math.pi:
                    dx = -math.pi

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    return

            self.font2.dance(gx, 440, self.greets[self.greetsPos:self.greetsPos + 55])
            gx -= 1
            if gx == -12:
                gx = 0
                self.greetsPos += 1
                if self.greetsPos == len(self.greets):
                    self.greetsPos = 0

            self.clock.tick(30)
            pygame.display.flip()

    def check(self, playerp):
        for i in range(len(self.points)):
            if playerp > self.points[i]:
                self.points.insert(i, playerp)
                self.points.pop()
                self.names.insert(i, self.getName())
                self.names.pop()
                return

    def getName(self):
        name = "WILLI.K"
        self.screen.fill(self.black)
        self.font.write(320, 20, "CONGRATULATIONS", True)
        self.font.write(320, 60, "YOU MADE IT INTO", True)
        self.font.write(320, 100, "THE HIGHSCORE", True)
        self.font.write(320, 140, "TYPE IN YOUR NAME:", True)
        while True:
            self.screen.fill(self.black,  (0, 188, 640, 56))
            self.font.dance(320, 200, name, True)
            self.clock.tick(30)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if event.key != pygame.K_SPACE:
                            c = pygame.key.name(event.key).upper()
                            if len(name) < 10:
                                if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.:-+":
                                    name += c
        return name

