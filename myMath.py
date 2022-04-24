import math


# function to help with methods Maby seperate file
def matMul(a, b):
    """multiply mat a X vector b"""
    result = []
    if len(a[0]) != len(b):
        print("columns of b must equal to vector a ")
        return

    for i in range(len(a)):
        seg = 0
        for j in range(len(a[0])):
            seg += a[i][j] * b[j]
        result.append(seg)

    return result


def mult(v, k):
    """multiply vector v by number k"""
    result = []
    for i in range(len(v)):
        result.append(v[i]*k)
    return result


def projection(dot):
    """ recive a dot with 3 axis and return a dot with 2 axis after calculating 
    the dot projection on axis z"""
    distance = 2
    z = 1 / (distance - dot[2])

    proMat = [
        [z, 0, 0],
        [0, z, 0]
    ]
    dot = matMul(proMat, dot)
    return dot


def vecAdd(a, b):
    """ Reciving two vectors return the added vector a+b"""
    newVec = []
    for i in range(len(a)):
        newVec.append(a[i]+b[i])
    return newVec


def vecSub(a, b):
    """ Reciving two vectors return the subbed vector a-b"""
    newVec = []
    for i in range(len(a)):
        newVec.append(a[i]-b[i])
    return newVec
