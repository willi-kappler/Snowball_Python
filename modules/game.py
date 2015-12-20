import pygame

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Game:
    "This class implements the main game loop with keyboard queries"
    def __init__(self, screen, level, options, highscore):
        self.screen = screen
        self.black = (0, 0, 0)
        self.level = level
        self.options = options
        self.highscore = highscore
        self.clock = pygame.time.Clock()

    def run(self):
        self.level.level = self.level.beginLevel
        self.level.quitGame = False
        self.level.load()
        self.level.createObj()
        self.level.player.noKeyPressedTime = pygame.time.get_ticks()
        while not self.level.quitGame:
            self.level.go()
            self.clock.tick(30)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.level.quitGame = True
                elif event.type == pygame.KEYDOWN:
                    self.level.player.noKeyPressedTime = pygame.time.get_ticks()
                    if event.key == pygame.K_ESCAPE:
                        self.level.quitGame = True
                    elif event.key == self.options.jump:
                        self.level.player.keyUpPress()
                    elif event.key == self.options.duck:
                        self.level.player.keyDownPress()
                    elif event.key == self.options.left:
                        self.level.player.moveLeft()
                    elif event.key == self.options.right:
                        self.level.player.moveRight()
                    elif event.key == self.options.action:
                        self.level.player.doAction()
                    elif event.key == pygame.K_n: # next level, cheat
                        self.level.exitReached()
                    elif event.key == pygame.K_k: # self kill
                        self.level.player.die()
                elif event.type == pygame.KEYUP:
                    if event.key == self.options.jump:
                        self.level.player.keyUpRelease()
                    elif event.key == self.options.duck:
                        self.level.player.keyDownRelease()
                    elif event.key == self.options.left:
                        self.level.player.keyLeftRelease()
                    elif event.key == self.options.right:
                        self.level.player.keyRightRelease()

        if self.level.maxLevel < self.level.level:
            self.level.maxLevel = self.level.level
        self.level.beginLevel = self.level.level
        self.level.fancyFill(1)
        self.highscore.check(self.level.player.points)
