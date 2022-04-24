
WIDTH = 500
HEIGHT = 500
EXHEIGHT = 800

MAPSIZE = 90  # each face 90X90 pixels

ox = 250
oy = 250

COLORS = {
    "R": (201, 45, 45),
    "O": (232, 120, 46),
    "Y": (248, 224, 65),
    "W": (255, 255, 255),
    "G": (81, 214, 63),
    "B": (62, 62, 214)
}

FACECOLORS = {  # for check purposes
    "F": "G",
    "B": "B",
    "R": "R",
    "L": "O",
    "U": "W",
    "D": "Y"
}

BUTCOLOR = [(0, 0, 0), (255, 255, 255), (180, 180, 180), (100, 100, 100)]

center = (400, 400)

# declaring dots to make a cube
dot1 = [-0.5, -0.5, 0.5]
dot2 = [-0.5, 0.5, 0.5]
dot3 = [0.5, -0.5, 0.5]
dot4 = [0.5, 0.5, 0.5]
dot5 = [-0.5, -0.5, -0.5]
dot6 = [-0.5, 0.5, -0.5]
dot7 = [0.5, -0.5, -0.5]
dot8 = [0.5, 0.5, -0.5]

dots = [dot1, dot2, dot3, dot4, dot5, dot6, dot7, dot8]

FACES = {
    "F": [["G" for i in range(3)] for j in range(3)],
    "B": [["B" for i in range(3)] for j in range(3)],
    "R": [["R" for i in range(3)] for j in range(3)],
    "L": [["O" for i in range(3)] for j in range(3)],
    "U": [["W" for i in range(3)] for j in range(3)],
    "D": [["Y" for i in range(3)] for j in range(3)],
}


"""FACES = { # for cube calibration
    "F": [["G", "W", "B"], ["W", "G", "W"], ["R", "W", "O"]],
    "B": [["G", "W", "B"], ["W", "B", "W"], ["R", "W", "O"]],
    "R": [["G", "W", "B"], ["W", "R", "W"], ["R", "W", "O"]],
    "L": [["G", "W", "B"], ["W", "O", "W"], ["R", "W", "O"]],
    "U": [["G", "W", "B"], ["W", "W", "W"], ["R", "W", "O"]],
    "D": [["G", "W", "B"], ["W", "Y", "W"], ["R", "W", "O"]]
}"""

# my own kind of dictionary what a certain move affect each face of the cube
MOVES = {
    "F": {
        "R": "l",
        "D": "u",
        "L": "r",
        "U": "d",
    },
    "F'": {
        "R": "l'",
        "U": "d'",
        "L": "r'",
        "D": "u'",
    },
    "B": {
        "U": "u",
        "L": "l",
        "D": "d",
        "R": "r"
    },
    "B'": {
        "U": "u'",
        "R": "r'",
        "D": "d'",
        "L": "l'",
    },
    "U": {
        "F": "u",
        "L": "u",
        "B": "u",
        "R": "u"
    },
    "U'": {
        "F": "u'",
        "R": "u'",
        "B": "u'",
        "L": "u'",
    },
    "D": {
        "F": "d",
        "R": "d",
        "B": "d",
        "L": "d"
    },
    "D'": {
        "F": "d'",
        "L": "d'",
        "B": "d'",
        "R": "d'",
    },
    "R": {
        "F": "r",
        "U": "r",
        "B": "l",
        "D": "r",
    },
    "R'": {
        "F": "r'",
        "D": "r'",
        "B": "l'",
        "U": "r'",
    },
    "L": {
        "F": "l",
        "D": "l",
        "B": "r",
        "U": "l"
    },
    "L'": {
        "F": "l'",
        "U": "l'",
        "B": "r'",
        "D": "l'",
    }
}

MOVESDICT = {
    "u'": [[0, 1, 1], [0, 3, 1]],
    "u": [[0, 1, 1], [2, -1, -1]],
    "d": [[2, 3, 1], [0, 3, 1]],
    "d'": [[2, 3, 1], [2, -1, -1]],
    "l": [[0, 3, 1], [0, 1, 1]],
    "l'": [[2, -1, -1], [0, 1, 1]],
    "r": [[2, -1, -1], [2, 3, 1]],
    "r'": [[0, 3, 1], [2, 3, 1]],
}


ROTATEMOVES = {
    "y": {
        "F": "R",
        "L": "F",
        "R": "B",
        "B": "L",
    },
    "-y": {
        "F": "L",
        "R": "F",
        "L": "B",
        "B": "R",
    },
    "x": {
        "F": "U",
        "U": "B",
        "D": "F",
        "B": "D",
    },
    "-x": {
        "F": "D",
        "D": "B",
        "B": "U",
        "U": "F",
    },
    "z": {
        "R": "U",
        "U": "L",
        "L": "D",
        "D": "R"
    },
    "-z": {
        "U": "R",
        "L": "U",
        "D": "L",
        "R": "D"
    },
}
