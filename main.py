import pygame
import sys
import math
from cube import Cube
from screen import Screen

FPS = 140

pygame.init()
clock = pygame.time.Clock()

cube = Cube()
screen = Screen()

while True:

    screen.screen.fill((137, 207, 240))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    screen.drawBackground()  # simply draw floors
    cube.calcDots(screen.screen)  # calculating dots with projection matrix
    cube.rotate(keys, screen)  # cube roations with arrows
    cube.moves(keys)  # check if moves where made(face moves like L R)
    screen.shadow(cube)  # draw shadow
    # get hover pressed mouse over arrows buttons
    hoverPressedArrow = screen.getArrowHoverPressed()
    # use the hover pressed to display right color button
    screen.drawButtons(hoverPressedArrow, cube)
    # get the pressed arrow as param to move the cube right
    cube.rotationMove(hoverPressedArrow)
    cube.displayFaces(screen.screen)  # display the top 3 faces of the cube
    cube.solveAnimation()  # perform solve animation if its on
    screen.extraButton()
    screen.displayCubeMap(cube)

    pygame.display.update()
    clock.tick(FPS)
