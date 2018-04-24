"""
writeRectFill(file, pt1, pt2, delta, scanDir, circCntr = [0,0], R=0):
    args:
        file
        pt1
        pt2
        delta
        scanDir - "h" (x axis) or "v" (y axis) scan lines
        supports a cicular hole with last 2 arguments
"""

from writeJmp import *
import numpy as np

def writeRectFill(file, pt1, pt2, hatch_spacing, scanDir='h'):
    f = file

    xCrd = [pt1[0], pt2[0]]
    yCrd = [pt1[1], pt2[1]]
    xCrd.sort()
    yCrd.sort()

    if scanDir == "h":
        for i, iterCrd in enumerate(np.arange(yCrd[1], yCrd[0], -hatch_spacing)):
            if i % 2 == 0:
                writeJmp(f, [xCrd[0], iterCrd])
                writeJmp(f, [xCrd[1], iterCrd])
            else:
                writeJmp(f, [xCrd[1], iterCrd])
                writeJmp(f, [xCrd[0], iterCrd])
    elif scanDir == "v":
        for i, iterCrd in enumerate(np.arange(xCrd[1], xCrd[0], -hatch_spacing)):
            if i % 2 == 0:
                writeJmp(f, [iterCrd, yCrd[1]])
                writeJmp(f, [iterCrd, yCrd[0]])
            else:
                writeJmp(f, [iterCrd, yCrd[0]])
                writeJmp(f, [iterCrd, yCrd[1]])


