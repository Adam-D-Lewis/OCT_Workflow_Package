from writeRectFill import writeRectFill
from writePause import writePause
from os.path import abspath


def write_oct_ec1000_file(filepath, x0, y0, w, h, start_delay=0.4, hs=0.2794, galvo_speed=1500):
    #  xo, yo are the top, left coordinates
    #  w, h are width and height(mm)
    #  hs = hatch spacing (mm)
    #  start_delay will wait a short time so the OCT has time to arm itself (s)
    #  galvo_speed is how fast the galvos move (mm/s)

    #open file
    fillFile = open(abspath(filepath), 'w')

    #set galvo speed and write initial delay
    # writeSpeed(fillFile, galvo_speed) #need to create this, and make sure it works

    #write the delay command
    writePause(fillFile, start_delay)

    #write rectangle
    writeRectFill(fillFile, [x0, y0], [x0+w, y0-h], hs, 'h')

    #close file
    fillFile.close()

    return fillFile.name