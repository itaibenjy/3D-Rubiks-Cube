import pygame
import sys
import math
from myMath import *
from data import COLORS, ox, oy, FACECOLORS, dots, FACES, MOVES, MOVESDICT, ROTATEMOVES, BUTCOLOR
import copy


class Cube(object):

    def __init__(self):
        self.dots = dots.copy()  # dots in 3D
        self.proDots = []  # projection dots in 2D
        self.faceNames = ["F", "B", "R", "L", "U", "D"]
        self.animationTimer = 0
        self.animationDire = ""
        self.keepMoves = []
        self.keepRotSteps = []
        self.solveTimer = 0
        self.isSolve = False
        self.faces = {
            "F": [0, 1, 3, 2],
            "B": [6, 7, 5, 4],
            "R": [2, 3, 7, 6],
            "L": [4, 5, 1, 0],
            "U": [4, 0, 2, 6],
            "D": [1, 5, 7, 3],
        }
        self.facesData = copy.deepcopy(FACES)
        self.moveTimer = 0
        self.angles = [0, 0, 0]
        self.rotateMoves = {
            "F": "F",
            "B": "B",
            "R": "R",
            "L": "L",
            "U": "U",
            "D": "D",
            "F'": "F'",
            "B'": "B'",
            "R'": "R'",
            "L'": "L'",
            "U'": "U'",
            "D'": "D'",
        }
        self.rotationX(-22.0)
        self.rotationY(-22.0)

    def calcDots(self, screen):
        """ This function gets the dots and change the projectoin accoring to z
        after that display the dots with the correct offset and call display lines fucntion"""
        new_dots = []
        for i in range(len(self.dots)):
            dot = projection(self.dots[i])
            dot = mult(dot, 300)
            new_dots.append(dot)
            # pygame.draw.circle(screen, (255, 255, 255),(dot[0]+ox, dot[1]+oy), 4) optoin to show the cornter dots
        self.proDots = new_dots.copy()

    def displayLines(self, faceDots, screen):
        # show the lines between the squares in the rubicks cube
        for i in range(4):
            pygame.draw.line(screen, (100, 100, 100),
                             faceDots[i][0], faceDots[i][3], 3)
            pygame.draw.line(screen, (100, 100, 100),
                             faceDots[0][i], faceDots[3][i], 3)

    def displayFaces(self, screen):
        avgFacesZ = [0.0]*6
        maxFaces = []
        # saving all z avrage to get the 3 faces that are "infront"
        for i, (key, value) in enumerate(self.faces.items()):  # enumerate through a dictionary
            for index in value:
                # z value of dot in index location
                avgFacesZ[i] += self.dots[index][2]
            avgFacesZ[i] /= 4  # get average

        # geetting the 3 max averages of z to get the 3 faces that are in front in order
        for i in range(3):
            max_index = avgFacesZ.index(max(avgFacesZ))
            maxFaces.append(self.faceNames[max_index])
            avgFacesZ[max_index] = -10  # just so next max will ignor it

        # putting the 3 faces on screen from back to front (small polygon to largest)
        for i in range(2, -1, -1):
            newFace = []
            for indexDot in self.faces[maxFaces[i]]:
                newFace.append(
                    [self.proDots[indexDot][0] + ox, self.proDots[indexDot][1]+oy])
            self.displayFace(maxFaces[i], newFace, screen)

    def displayFace(self, face, faceDots, screen):
        mat = [
            [faceDots[0], [0, 0], [0, 0], faceDots[1]],
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            [faceDots[3], [0, 0], [0, 0], faceDots[2]]
        ]

        # Calculating the other dots in the matrix
        # Calculating method: we have dot A and B get 1/3 dot and 2/3 dot (vecAB = B-A) 1/3 => A+vecAB*(1/3)
        for i in range(2):
            for j in range(1, 3):
                mat[j][i*3] = vecAdd(mat[0][i*3],
                                     mult(vecSub(mat[3][i*3], mat[0][i*3]), j/3.0))

        for i in range(4):
            for j in range(1, 3):
                mat[i][j] = vecAdd(mat[i][0], mult(
                    vecSub(mat[i][3], mat[i][0]), j/3.0))

        # going through every matrix of 2x2 in the dot matrix to display a polygon of a certain color
        for posy in range(3):
            for posx in range(3):
                newSquare = []
                for i in range(2):
                    for j in range(2):
                        newSquare.append(mat[i+posx][j+posy])
                newSquare[2], newSquare[3] = newSquare[3], newSquare[2]
                pygame.draw.polygon(
                    screen, COLORS[self.facesData[face][posy][posx]], newSquare)

        self.displayLines(mat, screen)

    def rotationX(self, angle):
        # this method ratate all dots of the cube on the x axis by the angel using rotation matrix
        rotation_x = [
            [1, 0, 0],
            [0, math.cos(math.radians(angle)), -
             math.sin(math.radians(angle))],
            [0, math.sin(math.radians(angle)),
             math.cos(math.radians(angle))]
        ]

        for i in range(len(self.dots)):
            self.dots[i] = matMul(rotation_x, self.dots[i])
        self.angles[0] += angle

    def rotationY(self, angle):
        # this method ratate all dots of the cube on the y axis by the angel using rataition matrix
        rotation_y = [
            [math.cos(math.radians(angle)), 0, -
             math.sin(math.radians(angle))],
            [0, 1, 0],
            [math.sin(math.radians(angle)), 0,
             math.cos(math.radians(angle))]
        ]

        for i in range(len(self.dots)):
            self.dots[i] = matMul(rotation_y, self.dots[i])
        self.angles[1] += angle

    def rotationZ(self, angle):
        # this method ratate all dots of the cube on the z axis by the angel using ratation matrix
        rotation_z = [
            [math.cos(math.radians(angle)), -
             math.sin(math.radians(angle)), 0],
            [math.sin(math.radians(angle)), math.cos(
                math.radians(angle)), 0],
            [0, 0, 1],
        ]

        for i in range(len(self.dots)):
            self.dots[i] = matMul(rotation_z, self.dots[i])
        self.angles[2] += angle

    def rotate(self, keys, screen):
        # check whitch key was pressed and aplying the right rotation by calling the right function with the right angle
        if keys[pygame.K_DOWN]:
            self.rotationX(2)
            screen.freeCamera = True
        if keys[pygame.K_UP]:
            self.rotationX(-2)
            screen.freeCamera = True
        if keys[pygame.K_RIGHT]:
            self.rotationY(2)
            screen.freeCamera = True
        if keys[pygame.K_LEFT]:
            self.rotationY(-2)
            screen.freeCamera = True
        if keys[pygame.K_z]:
            self.rotationZ(2)
            screen.freeCamera = True
        if keys[pygame.K_x]:
            self.rotationZ(-2)
            screen.freeCamera = True
        if keys[pygame.K_SPACE]:
            screen.freeCamera = False
            self.autoFix()
        if keys[pygame.K_RETURN]:
            self.isSolve = True

    def autoFix(self):
        self.dots = dots.copy()
        self.facesData = copy.deepcopy(FACES)
        self.rotationX(-22)
        self.rotationY(-22)
        for key in self.rotateMoves.keys():
            self.rotateMoves[key] = key

    def fixPos(self):
        self.dots = dots.copy()
        for rot in self.keepRotSteps:
            angle = 90
            if("-" in rot):
                angle = -angle
            if("x" in rot):
                self.rotationX(angle)
            else:
                self.rotationY(angle)
        self.rotationX(-22)
        self.rotationY(-22)

    def moves(self, keys):
        self.moveTimer -= 1
        if self.moveTimer < 0:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                if keys[pygame.K_f]:
                    self.move("F'")
                if keys[pygame.K_b]:
                    self.move("B'")
                if keys[pygame.K_r]:
                    self.move("R'")
                if keys[pygame.K_l]:
                    self.move("L'")
                if keys[pygame.K_u]:
                    self.move("U'")
                if keys[pygame.K_d]:
                    self.move("D'")
            else:
                if keys[pygame.K_f]:
                    self.move("F")
                if keys[pygame.K_b]:
                    self.move("B")
                if keys[pygame.K_r]:
                    self.move("R")
                if keys[pygame.K_l]:
                    self.move("L")
                if keys[pygame.K_u]:
                    self.move("U")
                if keys[pygame.K_d]:
                    self.move("D")

    def move(self, move):
        move = self.rotateMoves[move]
        self.keepMoves.append(move)
        self.moveTimer = 20
        # defaut color change with the fucntion lastMove
        colorArr = ["R", "R", "R"]
        for (key, value) in MOVES[move].items():
            colorArr = self.partMove(key[:1], value, colorArr)
        # first move key is the FACE of the first face we need to change
        firstMoveKey = list(MOVES[move])[0]
        self.lastMove(firstMoveKey, MOVES[move][firstMoveKey], colorArr)
        if "'" in move:
            self.faceRotateCCW(move[:1])
        else:
            self.faceRotateCW(move)

    def partMove(self, face, move, colorArr):
        newColorArr = []
        r1 = MOVESDICT[move][0]
        r2 = MOVESDICT[move][1]
        colorIndex = 0
        for i in range(r1[0], r1[1], r1[2]):
            for j in range(r2[0], r2[1], r2[2]):
                newColorArr.append(self.facesData[face][i][j])
                self.facesData[face][i][j] = colorArr[colorIndex]
                colorIndex += 1
        return newColorArr

    def lastMove(self, face, move, colorArr):
        r1 = MOVESDICT[move][0]
        r2 = MOVESDICT[move][1]
        colorIndex = 0
        for i in range(r1[0], r1[1], r1[2]):
            for j in range(r2[0], r2[1], r2[2]):
                self.facesData[face][i][j] = colorArr[colorIndex]
                colorIndex += 1

    def faceRotateCW(self, face):
        """ Take the matrix data of colors to the specified face and rotate it clockwise
        by reading each column from the last to first and making it a row
        mat(a,b,c) reverse column a is now first row and so on"""
        faceMat = self.facesData[face]
        newMat = []
        for j in range(3):
            newMat.append([])
            for i in range(2, -1, -1):
                newMat[j].append(faceMat[i][j])
        self.facesData[face] = newMat

    def faceRotateCCW(self, face):
        """ Take the matrix data of colors to the specified face and rotate it counter clockwise
        by reading each column from the last column to first and making it a row
        mat(a,b,c) c transpose is now first row and so on"""
        faceMat = self.facesData[face]
        newMat = []
        for j in range(2, -1, -1):
            newMat.append([])
            for i in range(3):
                newMat[-1].append(faceMat[i][j])
        self.facesData[face] = newMat

    def rotationMove(self, buttonPressed):
        for key, value in buttonPressed.items():
            if value == BUTCOLOR[3]:
                if(key == "U"):
                    rot = "-x"
                if(key == "D"):
                    rot = "x"
                if(key == "R"):
                    rot = "y"
                if(key == "L"):
                    rot = "-y"
                if (self.animationTimer <= 0):
                    self.animationTimer = 50
                    self.animationDire = rot
                    self.keepRotSteps.append(rot)
                    newRotMov = self.rotateMoves.copy()
                    if "y" in rot:
                        rot = "-y" if rot == "y" else "y"
                    for (a, b) in ROTATEMOVES[rot].items():
                        newRotMov[a] = self.rotateMoves[b]
                        newRotMov[a+"'"] = self.rotateMoves[b+"'"]
                    self.rotateMoves = newRotMov.copy()
        if (self.animationTimer > 0):
            self.turnAnimation()

    def turnAnimation(self):

        angle = 90/50.0
        self.rotationY(22.0)
        self.rotationX(22.0)
        if("-" not in self.animationDire):
            angle = -angle
        if("x" in self.animationDire):
            self.rotationX(angle)
        else:
            self.rotationY(angle)

        self.rotationX(-22.0)
        self.rotationY(-22.0)

        self.animationTimer -= 1

    def solveAnimation(self):
        if self.isSolve:
            self.solveTimer -= 1
            if self.solveTimer <= 0:
                self.solveTimer = 20
                if len(self.keepMoves) != 0:
                    move = self.keepMoves.pop(-1)
                else:
                    self.isSolve = False
                    return
                if "'" in move:
                    newMove = move.replace("'", "")
                else:
                    newMove = move+"'"
                colorArr = ["R", "R", "R"]
                for (key, value) in MOVES[newMove].items():
                    colorArr = self.partMove(key[:1], value, colorArr)
                # first move key is the FACE of the first face we need to change
                firstMoveKey = list(MOVES[newMove])[0]
                self.lastMove(
                    firstMoveKey, MOVES[newMove][firstMoveKey], colorArr)
                if "'" in newMove:
                    self.faceRotateCCW(newMove[:1])
                else:
                    self.faceRotateCW(newMove)
