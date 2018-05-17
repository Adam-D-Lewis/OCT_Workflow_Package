from writeRectFill import writeRectFill #need to get the old one of these
from os.path import abspath
import os

layers_10 = range(0, 10)
layers_5 = range(5, 10)
layers_2 = range(8, 10)
layers_1 = range(9, 10)

for i in range(10):
    save_path = abspath('./10_5_2_1/layer' + '{0:03d}'.format(i) +'.xml')
    directory = os.path.dirname(save_path)
    hs = 0.2794

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    # open file
    with open(abspath(save_path), 'w') as fillFile:
        if i % 2 == 0:
            h_or_v = 'h'
        else:
            h_or_v = 'v'

        if i in layers_10:
            # write rectangle
            x0 = -12.5
            y0 = 12.5
            w = 10
            h = 10
            writeRectFill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)

        if i in layers_5:
            x0 = 2.5
            y0 = 12.5
            w = 10
            h = 10
            writeRectFill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)

        if i in layers_2:
            x0 = -12.5
            y0 = -2.5
            w = 10
            h = 10
            writeRectFill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)

        if i in layers_1:
            x0 = 2.5
            y0 = -2.5
            w = 10
            h = 10
            writeRectFill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)


