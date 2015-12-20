import pygame

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Options:
    "This class loads, saves and manages all the options"
    def __init__(self):
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.jump = pygame.K_UP
        self.duck = pygame.K_DOWN
        self.action = pygame.K_SPACE
        self.mode = 0
        self.soundVol = 1.0
        self.musicVol = 1.0
        self.screen = None
        self.black = (0,0,0)
        self.font = None
        self.arrowRightGfx = None
        self.selectNextSnd = None
        self.selectSnd = None
        self.optionText = ["MOVE LEFT:", "MOVE RIGHT:", "JUMP:", "DUCK:", "ACTION:", "FULLSCREEN:", "SOUND VOL: 1.0", "MUSIC VOL: 1.0", "START LEVEL: 1", "BACK TO MAINMENU"]
        self.level = None
        self.clock = pygame.time.Clock()
        self.soundAvailable = True
        if pygame.mixer.get_init() == None:
            self.soundAvailable = False

    def run(self):
        self.beginLevel = self.level.beginLevel
        self.maxLevel = self.level.maxLevel
        self.optionText[8] = "START LEVEL: %d" % self.beginLevel
        selection = 0
        quitOpt = False
        if self.soundAvailable:
            self.testSound = self.level.exitSnd
        while not quitOpt:
            self.screen.fill(self.black)
            self.font.write(320, 10, "OPTIONS:", True)
            y = 70
            for i in range(10):
                self.font.write(50, y, self.optionText[i])
                y += 34
            self.screen.blit(self.arrowRightGfx, (10, 74 + (selection*34)))

            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                quitOpt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitOpt = True
                elif event.key == pygame.K_UP:
                    selection -= 1
                    if selection == -1:
                        selection = 9
                    if self.soundAvailable:
                        self.selectNextSnd.play()
                elif event.key == pygame.K_DOWN:
                    selection += 1
                    if selection == 10:
                        selection = 0
                    if self.soundAvailable:
                        self.selectNextSnd.play()
                elif event.key == pygame.K_RETURN:
                    if self.soundAvailable:
                        self.selectSnd.play()
                    if selection == 0:
                        self.showSingleOpt(0)
                        k = self.checkForKey()
                        if k != 0:
                            self.left = k
                            self.optionText[0] = "MOVE LEFT: " + pygame.key.name(self.left).upper()
                        if self.soundAvailable:
                            self.selectSnd.play()
                    elif selection == 1:
                        self.showSingleOpt(1)
                        k = self.checkForKey()
                        if k != 0:
                            self.right = k
                            self.optionText[1] = "MOVE RIGHT: " + pygame.key.name(self.right).upper()
                        if self.soundAvailable:
                            self.selectSnd.play()
                    elif selection == 2:
                        self.showSingleOpt(2)
                        k = self.checkForKey()
                        if k != 0:
                            self.jump = k
                            self.optionText[2] = "JUMP: " + pygame.key.name(self.jump).upper()
                        if self.soundAvailable:
                            self.selectSnd.play()
                    elif selection == 3:
                        self.showSingleOpt(3)
                        k = self.checkForKey()
                        if k != 0:
                            self.duck = k
                            self.optionText[3] = "DUCK: " + pygame.key.name(self.duck).upper()
                        if self.soundAvailable:
                            self.selectSnd.play()
                    elif selection == 4:
                        self.showSingleOpt(4)
                        k = self.checkForKey()
                        if k != 0:
                            self.action = k
                            self.optionText[4] = "ACTION: " + pygame.key.name(self.action).upper()
                        if self.soundAvailable:
                            self.selectSnd.play()
                    elif selection == 5:
                        if self.soundAvailable:
                            self.selectSnd.play()
                        if self.mode != 0:
                            self.mode = 0
                            self.optionText[5] = "FULLSCREEN: OFF"
                        else:
                            self.mode = pygame.FULLSCREEN
                            self.optionText[5] = "FULLSCREEN: ON"
                        pygame.display.set_mode( (640,480), pygame.HWSURFACE | self.mode )
                    elif selection == 6:
                        if self.soundAvailable:
                            self.showSingleOpt(6)
                            while True:
                                k = self.checkForKey()
                                if (k == pygame.K_LEFT) or (k == pygame.K_DOWN):
                                    self.soundVol -= 0.1
                                    if self.soundVol < 0.0:
                                        self.soundVol = 0.0
                                    self.optionText[6] = "SOUND VOL: %3.1f" % self.soundVol
                                    self.showSingleOpt(6)
                                    self.testSound.set_volume(self.soundVol)
                                    self.testSound.play()
                                elif (k == pygame.K_RIGHT) or (k == pygame.K_UP):
                                    self.soundVol += 0.1
                                    if self.soundVol > 1.0:
                                        self.soundVol = 1.0
                                    self.optionText[6] = "SOUND VOL: %3.1f" % self.soundVol
                                    self.showSingleOpt(6)
                                    self.testSound.set_volume(self.soundVol)
                                    self.testSound.play()
                                elif (k == 0) or (k == pygame.K_RETURN):
                                    self.selectSnd.play()
                                    self.level.setSoundVol()
                                    break
                    elif selection == 7:
                        if self.soundAvailable:
                            self.showSingleOpt(7)
                            while True:
                                k = self.checkForKey()
                                if (k == pygame.K_LEFT) or (k == pygame.K_DOWN):
                                    self.musicVol -= 0.1
                                    if self.musicVol < 0.0:
                                        self.musicVol = 0.0
                                    self.optionText[7] = "MUSIC VOL: %3.1f" % self.musicVol
                                    self.showSingleOpt(7)
                                    self.testSound.set_volume(self.musicVol)
                                    self.testSound.play()
                                elif (k == pygame.K_RIGHT) or (k == pygame.K_UP):
                                    self.musicVol += 0.1
                                    if self.musicVol > 1.0:
                                        self.musicVol = 1.0
                                    self.optionText[7] = "MUSIC VOL: %3.1f" % self.musicVol
                                    self.showSingleOpt(7)
                                    self.testSound.set_volume(self.musicVol)
                                    self.testSound.play()
                                elif (k == 0) or (k == pygame.K_RETURN):
                                    self.selectSnd.play()
                                    self.level.setMusicVol()
                                    break
                    elif selection == 8:
                        self.showSingleOpt(8)
                        while True:
                            k = self.checkForKey()
                            if (k == pygame.K_LEFT) or (k == pygame.K_DOWN):
                                if self.beginLevel > 1:
                                    self.beginLevel -= 1
                                self.optionText[8] = "START LEVEL: %d" % self.beginLevel
                                self.showSingleOpt(8)
                            elif (k == pygame.K_RIGHT) or (k == pygame.K_UP):
                                if self.beginLevel < self.maxLevel:
                                    self.beginLevel += 1
                                self.optionText[8] = "START LEVEL: %d" % self.beginLevel
                                self.showSingleOpt(8)
                            elif (k == 0) or (k == pygame.K_RETURN):
                                self.level.maxLevel = self.maxLevel
                                self.level.beginLevel = self.beginLevel
                                if self.soundAvailable:
                                    self.selectSnd.play()
                                break
                    elif selection == 9:
                        quitOpt = True

            self.clock.tick(30)
            pygame.display.flip()

    def load(self):
        try:
            handle = file("options.txt", "rt")
        except IOError:
            print "couldn't load file: options.txt"
            return

        self.left = int(handle.readline()[5:])
        self.optionText[0] = "MOVE LEFT: " + pygame.key.name(self.left).upper()
        self.right = int(handle.readline()[6:])
        self.optionText[1] = "MOVE RIGHT: " + pygame.key.name(self.right).upper()
        self.jump = int(handle.readline()[5:])
        self.optionText[2] = "JUMP: " + pygame.key.name(self.jump).upper()
        self.duck = int(handle.readline()[5:])
        self.optionText[3] = "DUCK: " + pygame.key.name(self.duck).upper()
        self.action = int(handle.readline()[7:])
        self.optionText[4] = "ACTION: " + pygame.key.name(self.action).upper()
        mode = handle.readline()[11:]
        if "on" in mode:
            self.mode = pygame.FULLSCREEN
            self.optionText[5] = "FULLSCREEN: ON"
        else:
            self.mode = 0
            self.optionText[5] = "FULLSCREEN: OFF"
        self.soundVol = float(handle.readline()[10:])
        self.optionText[6] = "SOUND VOL: %3.1f" % self.soundVol
        self.musicVol = float(handle.readline()[10:])
        self.optionText[7] = "MUSIC VOL: %3.1f" % self.musicVol
        self.beginLevel = int(handle.readline()[12:])
        self.optionText[8] = "START LEVEL: %d" % self.beginLevel
        self.maxLevel = int(handle.readline()[11:])
        handle.close()

    def save(self):
        try:
            handle = file("options.txt", "wt")
        except IOError:
            print "couldn't save file: options.txt"
            return
        handle.write("left: " + str(self.left) + "\n")
        handle.write("right: " + str(self.right) + "\n")
        handle.write("jump: " + str(self.jump) + "\n")
        handle.write("duck: " + str(self.duck) + "\n")
        handle.write("action: " + str(self.action) + "\n")
        if self.mode != 0:
            handle.write("fullscreen: on\n")
        else:
            handle.write("fullscreen: off\n")
        handle.write("sound vol: " + str(self.soundVol) + "\n")
        handle.write("music vol: " + str(self.musicVol) + "\n")
        handle.write("start level: " + str(self.beginLevel) + "\n")
        handle.write("max level: " + str(self.maxLevel) + "\n")
        handle.close()

    def checkForKey(self):
        while True:
            evt = pygame.event.wait()
            if evt.type == pygame.KEYDOWN:
                if evt.key != pygame.K_ESCAPE:
                    return evt.key
                return 0
        return 0

    def showSingleOpt(self, n):
        y = 70 + (n*34)
        self.screen.fill(self.black, (50,y,590,32))
        self.font.write(86, y, self.optionText[n])
        pygame.display.flip()

