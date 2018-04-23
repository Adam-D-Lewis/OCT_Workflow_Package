import xml.etree.ElementTree as ET
from os import path
import matplotlib.pyplot as plt
import numpy as np

#inputs when I make this a function
filepath = path.abspath(r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\Galvos\Galvo Position Signals\Galvo Wobble Build Files\wobble_10mm\wobble_10_2_pass.xml')
# tree = ET.parse(path.abspath(r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\simulateNoise\x_axis\test.xml'))
initCrd = [-5, 0]

#open xml file and parse
try:
    tree = ET.parse(filepath)
    root = tree.getroot()
except: #if it doesn't have overarching tag, then add it
    with open(filepath, 'r') as data:
        data = data.read()
        data = "<BeginJob>\n" + data + "\n</BeginJob>"
        root = ET.fromstring(data)

crd_list = [initCrd]

ec1000_commands = list(root)
for child in ec1000_commands:
    if child.tag.lower() == 'JumpAbs'.lower():
        crd = child.text.split(',')
        crd = [float(number) for number in crd]
        crd_list.append(crd)
    elif child.tag.lower() == 'MarkAbs'.lower():
        raise ValueError('This file contains a MarkAbs command')

def distance(x1,y1,x2,y2):
    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist

def calc_num_pts(dist, speed, fs):
    t = dist/speed
    numPts = t*fs
    return numPts

#separate out data x & y
x_data, y_data = np.transpose(crd_list)
speed = 1500 #mm/s
fs = 50000 #Hz
dist_vec = distance(x_data[:-1], y_data[:-1], x_data[1:], y_data[1:])
num_pts = np.round(calc_num_pts(dist_vec, speed, fs))

#make a line segment
def make_segment(x1, x2, numPts):
    seg = np.linspace(x1, x2, numPts)
    return seg

#build vector of data
long_data = []
for i in range(len(x_data)-1):
    long_data = np.append(long_data, make_segment(x_data[i], x_data[i+1], num_pts[i]))

#plot_data
plt.figure()
plt.plot(long_data)
plt.show()
print('bye')