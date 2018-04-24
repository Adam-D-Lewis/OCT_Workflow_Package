from writeRectFill import writeRectFill
from os.path import abspath

def write_oct_ec1000_file(x0, y0, w, h, hs=0.2794):
    #xo, yo are the top, left coordinates
    #hs = hatch spacing (mm)

    #open file
    fillFile = open(abspath('./oct_ec1000_file.xml'), 'w')

    #write rectangle
    writeRectFill(fillFile, [x0, y0], [x0+w, y0-h], hs, 'h')

    #close file
    fillFile.close()

    return fillFile.name