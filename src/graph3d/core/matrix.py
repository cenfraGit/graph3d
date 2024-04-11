import numpy as np
from math import cos, sin, tan, pi

"""
Matrices used in several program functions.
"""

def getIdentity():
    return np.array([ [1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1] ], dtype=np.float32)

def getTranslation(x, y, z):
    return np.array([ [1, 0, 0, x],
                      [0, 1, 0, y],
                      [0, 0, 1, z],
                      [0, 0, 0, 1] ], dtype=np.float32)

def getRotationX(angle):
    c = cos(angle)
    s = sin(angle)
    return np.array([ [1, 0,  0, 0],
                      [0, c, -s, 0],
                      [0, s,  c, 0],
                      [0, 0,  0, 1] ], dtype=np.float32)

def getRotationY(angle):
    c = cos(angle)
    s = sin(angle)
    return np.array([ [c,  0, s, 0],
                      [0,  1, 0, 0],
                      [-s, 0, c, 0],
                      [0,  0, 0, 1] ], dtype=np.float32)

def getRotationZ(angle):
    c = cos(angle)
    s = sin(angle)
    return np.array([ [c, -s, 0, 0],
                      [s,  c, 0, 0],
                      [0,  0, 1, 0],
                      [0,  0, 0, 1] ], dtype=np.float32)

def getScale(s):
    return np.array([ [s, 0, 0, 0],
                      [0, s, 0, 0],
                      [0, 0, s, 0],
                      [0, 0, 0, 1] ], dtype=np.float32)

def getPerspective(fov=60, aspectRatio=1, near=0.1, far=1000):
    a = fov * pi/180.0
    d = 1.0 / tan(a/2)
    r = aspectRatio
    b = (far + near) / (near - far)
    c = 2*far*near / (near - far)
    return np.array([ [d/r, 0,  0, 0],
                      [0,   d,  0, 0],
                      [0,   0,  b, c],
                      [0,   0, -1, 0] ], dtype=np.float32)
