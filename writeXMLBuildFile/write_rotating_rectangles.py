import writeEC1000file as EC
from os.path import abspath
import os

w = 10
h = 10

rects = []
rects.append([[-12.5, 12.5], [-12.5+w, 12.5-h]])
rects.append([[2.5, 12.5], [2.5+w, 12.5-h]])
rects.append([[-12.5, -2.5], [-12.5+w, -2.5-h]])
rects.append([[2.5, -2.5], [2.5+w, -2.5-h]])

angles = []
angles.append([180, 270]*5)
angles.append([180, 270, 0, 90]*2+[180, 270])
angles.append([i*65.5 for i in range(0, 10)])
angles.append([i*36 for i in range(0, 10)])

base_path = r'./rotating_rects_layers'
#write blank layer
save_path = abspath(base_path + '/layer' + '{0:03d}'.format(0) + '.xml')
directory = os.path.dirname(save_path)

#create directory if needed
if not os.path.exists(directory):
    os.mkdir(directory)

#save the blank layer
with open(abspath(save_path), 'w') as fillFile:
    EC.write_laser_power(fillFile, 45, 0)

for i in range(len(angles[0])):
    save_path = abspath(base_path + '/layer' + '{0:03d}'.format(i + 1) + '.xml')
    with open(abspath(save_path), 'w') as f:
        EC.write_laser_power(f, 75)
        for j in range(len(rects)):
                EC.write_rotating_square(f, angles[j][i], rects[j][0], rects[j][1], hs=0.2794)
                EC.write_comment(f, "Finished Rectangle")
                if j == 2:
                    print(angles[j][i])
    EC.plot_xml(save_path)

