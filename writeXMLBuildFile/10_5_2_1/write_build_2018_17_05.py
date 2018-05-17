import writeEC1000file as EC
from os.path import abspath
import os

base_path = r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\2018_17_05_Square_Variations\square_variations_layer_files'
#write blank layer
save_path = abspath(base_path + '/layer' + '{0:03d}'.format(0) + '.xml')
directory = os.path.dirname(save_path)

#create directory if needed
if not os.path.exists(directory):
    os.mkdir(directory)

#save the blank layer
with open(abspath(save_path), 'w') as fillFile:
    EC.write_laser_power(fillFile, 45, 0)

for i in range(1, 11):
    save_path = abspath(base_path + '/layer' + '{0:03d}'.format(i) + '.xml')

    hs = 0.2794

    # open file
    with open(abspath(save_path), 'w') as fillFile:
        if i % 2 == 0:
            h_or_v = 'h'
        else:
            h_or_v = 'v'

        # write top left rectangle
        x0 = -12.5
        y0 = 12.5
        w = 10
        h = 10
        EC.write_laser_power(fillFile, 50)
        EC.write_rect_fill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)

        # write top right rectangle
        x0 = 2.5
        y0 = 12.5
        w = 10
        h = 10
        EC.write_laser_power(fillFile, 50)
        EC.write_rect_fill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)

        # write bottom left rectangle
        x0 = -12.5
        y0 = -2.5
        w = 10
        h = 10
        EC.write_laser_power(fillFile, 25)
        EC.write_rect_fill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)

        # write bottom right rectangle
        x0 = 2.5
        y0 = -2.5
        w = 10
        h = 10
        EC.write_laser_power(fillFile, 75)
        EC.write_rect_fill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)

        # rescan top left rectangle
        x0 = -12.5
        y0 = 12.5
        w = 10
        h = 10
        EC.write_laser_power(fillFile, 25)
        EC.write_rect_fill(fillFile, [x0, y0], [x0 + w, y0 - h], hs, h_or_v)


