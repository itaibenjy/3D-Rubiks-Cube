import pygame
from data import ox, oy, WIDTH, HEIGHT, EXHEIGHT, BUTCOLOR, MAPSIZE, COLORS
from pprint import pprint


class Screen(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.arrowButton = self.getArrowButtons()
        self.freeCamera = False
        self.showMap = False
        self.showButtTimer = 0

    def drawBackground(self):
        self.screen.fill((137, 207, 240))
        floorHeight = (HEIGHT/3)*2
        pygame.draw.polygon(self.screen, (66, 178, 231), [
                            [-1, floorHeight], [WIDTH+1, floorHeight], [WIDTH+1, HEIGHT+1], [-1, HEIGHT+1]])

    def shadow(self, cube):
        for (key, value) in cube.faces.items():
            newface = []
            for inx in value:
                newface.append(
                    [(cube.proDots[inx][0] + ox), (cube.proDots[inx][1]*0.15 + oy) + 200])
            pygame.draw.polygon(self.screen, (25, 141, 195), newface)

    def getArrowButtons(self):
        arrowDict = {}
        arrowDict["U"] = [[WIDTH/2-30, 40], [WIDTH/2, 20], [WIDTH/2+30, 40]]
        arrowDict["D"] = [[WIDTH/2-30, HEIGHT-40],
                          [WIDTH/2, HEIGHT-20], [WIDTH/2+30, HEIGHT-40]]
        arrowDict["L"] = [[40, HEIGHT/2+30], [20, HEIGHT/2], [40, HEIGHT/2-30]]
        arrowDict["R"] = [[WIDTH - 40, HEIGHT/2+30],
                          [WIDTH - 20, HEIGHT/2], [WIDTH - 40, HEIGHT/2-30]]
        return arrowDict

    def drawButtons(self, hoverPressedColors, cube):
        if self.freeCamera:
            self.drawFocus(cube)
            return
        hoverPressedColors = self.getArrowHoverPressed()
        for (key, cord) in self.arrowButton.items():
            for j in range(2):  # 2 colors
                for i in range(2):  # 2 lines for arrow
                    pygame.draw.circle(
                        self.screen, BUTCOLOR[0] if j == 0 else hoverPressedColors[key], cord[i*2], (10-j*5)/2)
                    pygame.draw.line(
                        self.screen, BUTCOLOR[0] if j == 0 else hoverPressedColors[key], cord[i], cord[i+1], 10-j*5)

    def getArrowHoverPressed(self):
        # checking to see if mouse is hovering over arrow hard coded
        newColors = {
            "U": BUTCOLOR[1],
            "D": BUTCOLOR[1],
            "L": BUTCOLOR[1],
            "R": BUTCOLOR[1]
        }
        x, y = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()[0]
        for key, value in self.arrowButton.items():
            if key == "U":
                if(x >= value[0][0] and x <= value[2][0] and y >= value[1][1] and y <= value[0][1]):
                    newColors[key] = (BUTCOLOR[3] if press else BUTCOLOR[2])
            if key == "D":
                if(x >= value[0][0] and x <= value[2][0] and y <= value[1][1] and y >= value[0][1]):
                    newColors[key] = (BUTCOLOR[3] if press else BUTCOLOR[2])
            if key == "L":
                if(x >= value[1][0] and x <= value[0][0] and y <= value[0][1] and y >= value[2][1]):
                    newColors[key] = (BUTCOLOR[3] if press else BUTCOLOR[2])
            if key == "R":
                if(x >= value[0][0] and x <= value[1][0] and y <= value[0][1] and y >= value[2][1]):
                    newColors[key] = (BUTCOLOR[3] if press else BUTCOLOR[2])
        return newColors

    def drawFocus(self, cube):
        dot = [WIDTH - 50, 50]
        x, y = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()[0]
        color = BUTCOLOR[1]
        if(x <= WIDTH-16 and x >= WIDTH-82 and y <= 82 and y >= 16):
            if(press):
                cube.fixPos()
                color = BUTCOLOR[3]
                self.freeCamera = False
            else:
                color = BUTCOLOR[2]
        pygame.draw.circle(self.screen, BUTCOLOR[0], dot, 32, 10)
        pygame.draw.circle(self.screen, color, dot, 30, 5)
        pygame.draw.circle(self.screen, BUTCOLOR[0], dot, 7.5)
        pygame.draw.circle(self.screen, color, dot, 5)

    def extraButton(self):
        self.showButtTimer -= 1
        cords = [[25, HEIGHT-40], [25, HEIGHT-10],
                 [10, HEIGHT-25], [40, HEIGHT-25]]
        colors = [BUTCOLOR[0], BUTCOLOR[1]]
        x, y = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()[0]
        if(x >= 10 and x <= 40 and y >= HEIGHT-40 and y <= HEIGHT-10):
            if(press):
                colors[1] = BUTCOLOR[3]
                if self.showButtTimer <= 0:
                    self.showButtTimer = 20
                    if not self.showMap:
                        self.showMap = True
                        self.screen = pygame.display.set_mode(
                            (WIDTH, EXHEIGHT))
                    else:
                        self.showMap = False
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            else:
                colors[1] = BUTCOLOR[2]
        if not self.showMap:
            for i in range(2):
                for j in range(2):
                    pygame.draw.circle(self.screen, colors[i], [
                                       cords[j+2][0]+1, cords[j+2][1]], 3-i*2)
                    pygame.draw.line(
                        self.screen, colors[i], cords[j], cords[j+1], 6-i*4)
                pygame.draw.circle(self.screen, colors[i], [
                                   cords[0][0]+1, cords[0][1]], 3-i*2)
                pygame.draw.line(
                    self.screen, colors[i], cords[1], cords[3], 6-i*3)
        else:
            for i in range(2):
                for j in range(2):
                    pygame.draw.circle(self.screen, colors[i], [
                                       cords[j+2][0]+1, cords[j+2][1]], 3-i*2)
                    pygame.draw.line(
                        self.screen, colors[i], cords[0], cords[j+1], 6-i*4)
                pygame.draw.circle(self.screen, colors[i], [
                                   cords[1][0]+1, cords[1][1]], 3-i*2)
                pygame.draw.line(
                    self.screen, colors[i], cords[0], cords[3], 6-i*3)

    def displayCubeMap(self, cube):
        if not self.showMap:
            return
        ms = MAPSIZE
        line = ms/3
        sh = HEIGHT+15  # start hight
        sw = 65  # start width
        swtb = 70+ms  # start width top bottom faces
        gap = 5

        self.drawMapFace(swtb, sh-gap, cube.facesData["U"])
        self.drawMapFace(swtb, sh+gap+ms*2,
                         cube.facesData["D"])
        faces = ["L", "F", "R", "B"]
        for i in range(4):
            self.drawMapFace(sw+i*(ms+gap), sh+ms,
                             cube.facesData[faces[i]])

        for i in range(4):
            # top face
            pygame.draw.line(self.screen, (0, 0, 0), [
                             swtb, sh + i*(line)-gap], [swtb+ms, sh + i*(line)-gap], 3)
            pygame.draw.line(self.screen, (0, 0, 0), [
                             swtb + (line)*i, sh-gap], [swtb+(line)*i, sh+ms-gap], 3)

            # bottom face
            pygame.draw.line(self.screen, (0, 0, 0), [
                             swtb, sh+(2*ms) + i*(line)+gap], [swtb+ms, sh+(2*ms) + i*(line)+gap], 3)
            pygame.draw.line(self.screen, (0, 0, 0), [
                             swtb + (line)*i, sh+(2*ms)+gap], [swtb+(line)*i, sh+(3*ms)+gap], 3)

            for j in range(4):
                # midle lines of 4 faces
                pygame.draw.line(self.screen, (0, 0, 0), [
                                 sw+j*(ms+gap), sh+ms+i*line], [sw+ms+j*(ms+gap), sh+ms+i*line], 3)

                pygame.draw.line(self.screen, (0, 0, 0), [
                                 sw+i*line+j*(ms+gap), sh+ms], [sw+i*line+j*(ms+gap), sh+2*ms], 3)

    def drawMapFace(self, x, y, face):
        # get a 3*3 matrix face of colors symbols "G" "B" and display them from cord x,y
        cs = MAPSIZE / 3  # cell size
        for line in range(3):
            for column in range(3):
                polyCords = [[x+column*cs, y+line*cs], [x+(column+1)*cs, y+line*cs], [x+(
                    column+1)*cs, y+(line+1)*cs], [x+column*cs, y+(line+1)*cs]]
                pygame.draw.polygon(
                    self.screen, COLORS[face[line][column]], polyCords)
