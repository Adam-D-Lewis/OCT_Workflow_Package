import writeEC1000file as EC
from os.path import abspath
import os

w = 50
h = 12.7
s = 4 #x and y spacing

rects = []
x0 = -w / 2
y0 = h / 2
for y_ind in range(-1,2):
    y = y0 + y_ind * (h + s)
    rects.append([[x0, y], [x0 + w, y-h]])

x = -w/2-s-h
y = w/2
rects.append([[x, y],[x+h, y-w]])
x=-x-h

rects.append([[x, y],[x+h, y-w]])

angles = [i*65.5 for i in range(0, 20)]
num_layers = len(angles)+1
laser_power = [45, 55, 65, 75, 85]

base_path = r'./3_point_test_layers'
#write blank layer
save_path = abspath(base_path + '/layer' + '{0:03d}'.format(0) + '.xml')
directory = os.path.dirname(save_path)

#create directory if needed
if not os.path.exists(directory):
    os.mkdir(directory)

#save the blank layer
with open(abspath(save_path), 'w') as fillFile:
    EC.write_laser_power(fillFile, 65, 0)


for i in range(len(angles)):
    save_path = abspath(base_path + '/layer' + '{0:03d}'.format(i + 1) + '.xml')
    with open(abspath(save_path), 'w') as f:
        for j in range(len(rects)):
            EC.write_laser_power(f, laser_power[j])
            EC.write_rotating_square(f, angles[i], rects[j][0], rects[j][1], hs=0.2794)
    EC.plot_xml(save_path)

