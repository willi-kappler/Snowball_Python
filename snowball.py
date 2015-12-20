#!/usr/bin/env python

# Snowball V 0.2 - 2005.09.19
# By Willi Kappler <grandor@gmx.de>
# http://www.snowball.retrovertigo.de
#
# This game is licensed under the GPL
# See www.gnu.org for more information

import sys, pygame
sys.path.append("modules")
import editor
import font
import options
import highscore
import game
import level
import gimmick
import credits

pygame.init()

pygame.key.set_repeat(300, 30)
pygame.mouse.set_visible(0)

defaultOpt = options.Options()
defaultOpt.load()

screen = pygame.display.set_mode( (640, 480), pygame.HWSURFACE | defaultOpt.mode )
defaultOpt.screen = screen
pygame.display.set_caption("Snowball V0.2  - 2005.09.19 - By Willi Kappler")

black = (0, 0, 0)

highsc = highscore.Highscore(screen)
highsc.load()

logoGfx = pygame.image.load("gfx/logo.png")
arrowLeftGfx = pygame.image.load("gfx/arrow_left.png")
arrowRightGfx = pygame.image.load("gfx/arrow_right.png")

defaultOpt.arrowRightGfx = arrowRightGfx

soundAvailable = True
if pygame.mixer.get_init() == None:
    soundAvailable = False
    print "Could not open soundmixer! You have to play without sound..."
else:
    selectNextSnd = pygame.mixer.Sound("snd/tick.ogg")
    selectSnd = pygame.mixer.Sound("snd/beep.ogg")

    defaultOpt.selectNextSnd = selectNextSnd
    defaultOpt.selectSnd = selectSnd

arrowLeftPos = [(320 + 118, 234), (320 + 140, 274), (320 + 118, 314), (320 + 152, 354), (320 + 90, 394), (320 + 58, 434)]
arrowRightPos = [(290 - 118, 234), (290 - 140, 274), (290 - 118, 314), (290 - 152, 354), (290 - 90, 394), (290 - 58, 434)]

bigFont = font.Font(screen, "gfx/big_font.png", 24, 24)
defaultOpt.font = bigFont
highsc.font = bigFont

smallFont = font.Font(screen, "gfx/small_font.png", 12, 16)
snowballLevel = level.Level(screen, smallFont, defaultOpt)
defaultOpt.level = snowballLevel
highsc.font2 = smallFont
snowballLevel.beginLevel = defaultOpt.beginLevel
snowballLevel.maxLevel = defaultOpt.maxLevel

levelEd = editor.LevelEditor(screen, smallFont, snowballLevel)
snowball = game.Game(screen, snowballLevel, defaultOpt, highsc)

fun = gimmick.Gimmick(screen, snowballLevel)

coolGuys = credits.Credits(screen, bigFont)

selection = 0
quitGame = False

mainMenu = [(230, "PLAY GAME"), (270, "SET OPTIONS"), (310, "HIGHSCORE"), (350, "LEVEL EDITOR"), (390, "CREDITS"), (430, "QUIT")]

clock = pygame.time.Clock()

while not quitGame:
    screen.fill(black)
    screen.blit(logoGfx, (154, 32))
    screen.blit(arrowLeftGfx, arrowLeftPos[selection])
    screen.blit(arrowRightGfx, arrowRightPos[selection])

    for i in range(6):
        (y, txt) = mainMenu[i]
        if i == selection:
            bigFont.dance(320, y, txt, True)
        else:
            bigFont.write(320, y, txt, True)

    fun.go()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame = True
            elif event.key == pygame.K_UP:
                selection -= 1
                if selection == -1:
                    selection = 5
                if soundAvailable:
                    selectNextSnd.play()
            elif event.key == pygame.K_DOWN:
                selection += 1
                if selection == 6:
                    selection = 0
                if soundAvailable:
                    selectNextSnd.play()
            elif event.key == pygame.K_RETURN:
                if soundAvailable:
                    selectSnd.play()
                if selection == 0:
                    snowball.run()
                elif selection == 1:
                    defaultOpt.run()
                elif selection == 2:
                    highsc.run()
                elif selection == 3:
                    levelEd.run()
                    pygame.mouse.set_visible(0)
                elif selection == 4:
                    coolGuys.run()
                elif selection == 5:
                    quitGame = True
                fun.reset()

    clock.tick(30)
    pygame.display.flip()

defaultOpt.save()
highsc.save()
pygame.time.wait(200)

print "bye!"
sys.exit()
