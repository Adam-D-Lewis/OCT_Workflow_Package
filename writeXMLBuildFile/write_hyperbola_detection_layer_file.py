import writeEC1000file as EC
from os.path import abspath
import os
import math


hs = 0.2794

base_path = r'./build_surface_survey_build_files'
num_layers = 5

#create directory if needed
if not os.path.exists(base_path):
    os.mkdir(base_path)

save_path = abspath(base_path + '/layer' + '{0:03d}'.format(0) + '.xml')
with open(abspath(save_path), 'w') as f:
    EC.write_pause(f, 0.1)

for i, val in enumerate(range(num_layers)):
    if i % 2 == 0:
        h_or_v = 'h'
    else:
        h_or_v = 'v'
    save_path = abspath(base_path + '/layer' + '{0:03d}'.format(i+1) + '.xml')
    with open(abspath(save_path), 'w') as f:
        EC.write_laser_power(f, 75)
        EC.write_rect_fill(f, [-80, 65], [70, -70], hs, h_or_v)
        EC.write_jmp(f, [0, 0])
        # EC.plot_xml(save_path)
