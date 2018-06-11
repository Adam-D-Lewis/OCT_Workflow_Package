import writeEC1000file as EC
from os.path import abspath
import os
import math


w = 10
h = 10
hs = 0.2794

base_path = r'./large_XCT_cylinder'
non_symmetric_path = os.path.join(base_path, 'non_symmetric')
symmetric_path = os.path.join(base_path, 'symmetric')

#create directory if needed
if not os.path.exists(non_symmetric_path):
    os.mkdir(non_symmetric_path)

if not os.path.exists(symmetric_path):
    os.mkdir(symmetric_path)

cyl_1_layers = [1]*5
cyl_2_layers = [1]*5

for i, val in enumerate(zip(cyl_1_layers, cyl_2_layers)):
    if i % 2 == 0:
        h_v = 'h'
    else:
        h_v = 'v'
    c1, c2 = val
    save_path = abspath(non_symmetric_path + '/layer' + '{0:03d}'.format(i) + '.xml')
    with open(abspath(save_path), 'w') as f:
        EC.write_laser_power(f, 85)
        # EC.write_circ_fill(f, (16.5, 0), 30 / 2, hs, h_v)
        # EC.write_circ_fill(f, (-16.5, 0), 30 / 2, hs, h_v)
        if c1:
            EC.write_rect_fill(f, (-15/4+16.5, 3/4*15+2), (15/4+16.5, 1/4*15+2), hs, h_v)
            EC.write_rect_fill(f, (-15 / 4 - 16.5, 3 / 4 * 15 + 2), (15 / 4 - 16.5, 1 / 4 * 15 + 2), hs, h_v)
        if c2:
            EC.write_circ_fill(f, (9+16.5, 0), 4, hs, h_v)
            EC.write_circ_fill(f, (9 - 16.5, 0), 4, hs, h_v)
        if c2:
            EC.write_circ_fill(f, (-16.5,0), 1, hs, h_v)
            EC.write_circ_fill(f, (16.5-1.5, 0), 1, hs, h_v)
            EC.write_circ_fill(f, (16.5+1.5, 0), 1, hs, h_v)

    # if i >= 5:
    #     EC.plot_xml(save_path)

symmetric_layer_num = 10

for i in range(symmetric_layer_num):
    if i % 2 == 0:
        h_v = 'h'
    else:
        h_v = 'v'
    c1, c2 = val
    save_path = abspath(symmetric_path + '/layer' + '{0:03d}'.format(i) + '.xml')
    with open(abspath(save_path), 'w') as f:
        EC.write_laser_power(f, 95)
        EC.write_circ_fill(f, (16.5, 0), 30/2, hs, h_v)
        EC.write_laser_power(f, 85)
        EC.write_circ_fill(f, (-16.5, 0), 30/2, hs, h_v)
    # EC.plot_xml(save_path)
