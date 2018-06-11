import writeEC1000file as EC
from os.path import abspath
import os

hs =0.2794
w = 50
h = 12.7
s = 3 #x and y spacing

rects = []
x0 = -w / 2
y0 = h / 2
for y_ind in range(-2,3):
    y = y0 + y_ind * (h + s)
    rects.append([[x0, y], [x0 + w, y-h]])

# x = -w/2-s-h
# y = w/2
# rects.append([[x, y],[x+h, y-w]])
# x=-x-h
#
# rects.append([[x, y],[x+h, y-w]])

angles = [i*65.5 for i in range(0, 20)]
num_layers = len(angles)+1
laser_power = [75]*5

base_path = r'./3_point_test_layers_v2'
#write blank layer
save_path = abspath(base_path + '/layer' + '{0:03d}'.format(0) + '.xml')
directory = os.path.dirname(save_path)

#create directory if needed
if not os.path.exists(directory):
    os.mkdir(directory)

#save the blank layer
with open(abspath(save_path), 'w') as fillFile:
    EC.write_laser_power(fillFile, 65, 0)


for ind, i in enumerate(range(len(angles))):
    if ind % 2 == 0:
        h_or_v = 'h'
    else:
        h_or_v = 'v'
    save_path = abspath(base_path + '/layer' + '{0:03d}'.format(i + 1) + '.xml')
    with open(abspath(save_path), 'w') as f:
        for j in range(len(rects)):
            EC.write_laser_power(f, laser_power[j])
            EC.write_rect_fill(f, rects[j][0], rects[j][1], hs, h_or_v)
    # EC.plot_xml(save_path)

