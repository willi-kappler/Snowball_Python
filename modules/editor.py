import pygame

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class LevelEditor:
    "Class for the level editor. The game and the editor share the same instance of the level class"
    def __init__(self, screen, smfont, level):
        self.screen = screen
        self.black = (0, 0, 0)
        self.font = smfont
        self.level = level
        self.layer = 3
        self.leftTool = [1, 1]
        self.rightTool = [0, 0]
        self.maxTool = [len(self.level.backGfx), len(self.level.frontGfx)]
        self.frontStart = 0
        self.backStart = 0
        self.lastLevel = 1
        self.helppanel = pygame.image.load("gfx/helppanel.png")
        self.soundAvailable = True
        if pygame.mixer.get_init() == None:
            self.soundAvailable = False
        else:
            self.snd = pygame.mixer.Sound("snd/beep.ogg")

    def displayInfo(self):
        for i in range(0, 160, 4):
            self.screen.blit(self.helppanel, (0, 40), (160 - i, 0, i, 400))
            pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_h) or (event.key == pygame.K_i):
                    break

        self.level.display(self.layer)
        pygame.display.flip()


    def displayLevel(self):
        self.font.write(490, 10, "LEVEL: " + str(self.level.level))

    def displayTools(self):
        self.screen.fill(self.black, (480, 30, 180, 450))
        if self.layer == 0 or self.layer == 2:
            t = self.backStart
            y = 30
            for i in range(13):
                x = 480
                for j in range(5):
                    self.screen.blit(self.level.backGfx[t], (x, y))
                    x += 32
                    t += 1
                    if t == self.maxTool[0]:
                        t = 0
                y += 32

            self.screen.blit(self.level.backGfx[self.leftTool[0]], (576, 448))
            self.screen.blit(self.level.backGfx[self.rightTool[0]], (608, 448))
        else:
            t = self.frontStart
            y = 30
            for i in range(13):
                x = 480
                for j in range(5):
                    if t > 0:
                        self.screen.blit(self.level.frontGfx[t], (x, y))
                    x += 32
                    t += 1
                    if t == self.maxTool[1]:
                        t = 0
                y += 32

            self.screen.blit(self.level.backGfx[0], (576, 448))
            self.screen.blit(self.level.backGfx[0], (608, 448))

            t = self.leftTool[1]
            if t > 0:
                self.screen.blit(self.level.frontGfx[t], (576, 448))

            t = self.rightTool[1]
            if t > 0:
                self.screen.blit(self.level.frontGfx[t], (608, 448))

        pygame.display.flip()

    def refresh(self):
        self.screen.fill(self.black)
        self.level.display(self.layer)
        self.displayLevel()
        self.displayTools()

    def incLeftTool(self):
        if self.layer == 0 or self.layer == 2:
            self.leftTool[0] += 1
            if self.leftTool[0] == self.maxTool[0]:
                self.leftTool[0] = 0
        else:
            self.leftTool[1] += 1
            if self.leftTool[1] == self.maxTool[1]:
                self.leftTool[1] = 0

        self.displayTools()

    def incRightTool(self):
        if self.layer == 0 or self.layer == 2:
            self.rightTool[0] += 1
            if self.rightTool[0] == self.maxTool[0]:
                self.rightTool[0] = 0
        else:
            self.rightTool[1] += 1
            if self.rightTool[1] == self.maxTool[1]:
                self.rightTool[1] = 0

        self.displayTools()

    def decLeftTool(self):
        if self.layer == 0 or self.layer == 2:
            self.leftTool[0] -= 1
            if self.leftTool[0] == -1:
                self.leftTool[0] = self.maxTool[0] - 1
        else:
            self.leftTool[1] -= 1
            if self.leftTool[1] == -1:
                self.leftTool[1] = self.maxTool[1] - 1

        self.displayTools()

    def decRightTool(self):
        if self.layer == 0 or self.layer == 2:
            self.rightTool[0] -= 1
            if self.rightTool[0] == -1:
                self.rightTool[0] = self.maxTool[0] - 1
        else:
            self.rightTool[1] -= 1
            if self.rightTool[1] == -1:
                self.rightTool[1] = self.maxTool[1] - 1

        self.displayTools()

    def run(self):
        pygame.mouse.set_visible(1)
        self.level.level = self.lastLevel
        self.level.load()
        self.refresh()

        quitEditor = False
        while not quitEditor:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitEditor = True
                    self.lastLevel = self.level.level
                elif event.key == pygame.K_PLUS:
                    keys = pygame.key.get_mods()
                    if ((keys & pygame.KMOD_LSHIFT) == pygame.KMOD_LSHIFT) or ((keys & pygame.KMOD_RSHIFT) == pygame.KMOD_RSHIFT):
                        self.incRightTool()
                    else:
                        self.incLeftTool()
                elif event.key == pygame.K_MINUS:
                    keys = pygame.key.get_mods()
                    if ((keys & pygame.KMOD_LSHIFT) == pygame.KMOD_LSHIFT) or ((keys & pygame.KMOD_RSHIFT) == pygame.KMOD_RSHIFT):
                        self.decRightTool()
                    else:
                        self.decLeftTool()
                elif event.key == pygame.K_s:
                    self.level.save()
                    if self.soundAvailable:
                        self.snd.play()
                elif event.key == pygame.K_c:
                    if self.layer == 0 or self.layer == 2:
                        self.level.clear(self.layer, self.rightTool[0])
                        self.level.display(self.layer)
                    else:
                        self.level.clear(self.layer, self.rightTool[1])
                        self.level.display(self.layer)
                    pygame.display.flip()
                elif event.key == pygame.K_n:
                    self.level.next()
                    self.refresh()
                elif event.key == pygame.K_p:
                    self.level.prev()
                    self.refresh()
                elif event.key == pygame.K_1:
                    self.layer = 0
                    self.refresh()
                elif event.key == pygame.K_2:
                    self.layer = 1
                    self.refresh()
                elif event.key == pygame.K_3:
                    self.layer = 2
                    self.refresh()
                elif event.key == pygame.K_4:
                    self.layer = 3
                    self.refresh()
                elif (event.key == pygame.K_h) or (event.key == pygame.K_i):
                    self.displayInfo()
                elif event.key == pygame.K_DOWN:
                    if (self.layer == 0) or (self.layer == 2):
                        self.backStart += 5
                        if self.backStart >= self.maxTool[0]:
                            self.backStart = 0
                    else:
                        self.frontStart += 5
                        if self.frontStart >= self.maxTool[1]:
                            self.frontStart = 0
                    self.displayTools()
                elif event.key == pygame.K_UP:
                    if (self.layer == 0) or (self.layer == 2):
                        self.backStart -= 5
                        if self.backStart < 0:
                            self.backStart = 0
                    else:
                        self.frontStart -= 5
                        if self.frontStart < 0:
                            self.frontStart = 0
                    self.displayTools()

            elif (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.MOUSEMOTION):
                (mx, my) = pygame.mouse.get_pos()
                (lmb, mmb, rmb) = pygame.mouse.get_pressed()
                if mx < 480:
                    mx = mx / 32
                    my = my / 32
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        if lmb:
                            if self.layer == 0 or self.layer == 2:
                                self.leftTool[0] = self.level.backData[my][mx]
                            else:
                                self.leftTool[1] = self.level.frontData[my][mx]
                            self.displayTools()
                        elif rmb:
                            if self.layer == 0 or self.layer == 2:
                                self.rightTool[0] = self.level.backData[my][mx]
                            else:
                                self.rightTool[1] = self.level.frontData[my][mx]
                            self.displayTools()
                    else:
                        if lmb:
                            if self.layer == 0 or self.layer == 2:
                                self.level.set(self.layer, mx, my, self.leftTool[0])
                            else:
                                self.level.set(self.layer, mx, my, self.leftTool[1])
                            pygame.display.flip()

                        elif rmb:
                            if self.layer == 0 or self.layer == 2:
                                self.level.set(self.layer, mx, my, self.rightTool[0])
                            else:
                                self.level.set(self.layer, mx, my, self.rightTool[1])
                            pygame.display.flip()
                elif (my > 30) and (my < 448):
                    mx = (mx - 480) / 32
                    my = (my - 30) / 32
                    if lmb:
                        if (self.layer == 0) or (self.layer == 2):
                            t = (5 * my) + mx + self.backStart
                            if t >= self.maxTool[0]:
                                t = t - self.maxTool[0]
                            self.leftTool[0] = t
                        else:
                            t = (5 * my) + mx + self.frontStart
                            if t >= self.maxTool[1]:
                                t = t - self.maxTool[1]
                            self.leftTool[1] = t
                        self.displayTools()
                    elif rmb:
                        if (self.layer == 0) or (self.layer == 2):
                            t = (5 * my) + mx + self.backStart
                            if t >= self.maxTool[0]:
                                t = t - self.maxTool[0]
                            self.rightTool[0] = t
                        else:
                            t = (5 * my) + mx + self.frontStart
                            if t >= self.maxTool[1]:
                                t = t - self.maxTool[1]
                            self.rightTool[1] = t
                        self.displayTools()
