import pygame

# By Willi Kappler <grandor@gmx.de>
# Licensed under GPL

class Credits:
    "Credit class created and called from the main programm"
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.black = (0, 0, 0)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.screen.fill(self.black)
            self.font.write(320, 10, "YOU WANT TO KNOW WHO", True)
            self.font.write(320, 40, "DID THIS KICK-ASS", True)
            self.font.write(320, 70, "COOL GAME. WHO THOSE", True)
            self.font.write(320, 100, "INCREDIBLE UEBER-GEEKS", True)
            self.font.write(320, 130, "ARE...", True)
            self.font.write(320, 160, "SO HERE WE GO:", True)
            self.font.write(10, 250, "CODE + SFX: WILLI KAPPLER")
            self.font.write(50, 280, "GRANDOR AT GMX.DE")
            self.font.write(10, 350, "GFX: ANTHONY CHAU")
            self.font.write(50, 380, "PYROFACTOR AT GMAIL.COM")
            self.font.write(320, 430, ".---+ ENJOY +---.", True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    return
            pygame.display.flip()

