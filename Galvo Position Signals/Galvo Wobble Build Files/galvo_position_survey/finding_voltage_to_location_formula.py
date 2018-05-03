import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
from readGalvoFiles import read_galvo_files
from filters import filter_galvo_data

#inputs
#data
#data_indices
#x_loc, y_loc

#just for now
[xGalvo, yGalvo] = read_galvo_files(r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\Galvos\Galvo Position Signals\motors_on\galvo_position_survey.2d_dbl')
xGalvo = xGalvo[150000:300000]
yGalvo = yGalvo[150000:300000]

indices = [[15000, 19000],
         [21000, 25000],
         [26000, 30000],
         [32000, 36000],
         [37000, 41000],
         [43000, 47000],
         [48000, 52000],
         [54000, 58000],
         [59000, 63000],
         [65000, 69000],
         [70000, 74000],
         [76000, 80000],
         [81000, 85000],
         [87000, 91000],
         [92000, 96000],
         [98000, 102000],
         [103000, 107000],
         [109000, 113000],
         [114000, 118000],
         [119500, 123500],
         [126000, 130000]]

x_loc = list(range(-100, 101, 10))
y_loc = list(range(-100, 101, 10))


#okay, on with the show

xGalvo = filter_galvo_data(xGalvo, 1500, 10, 50000, 0.0004, multiple=8)
yGalvo = filter_galvo_data(yGalvo, 1500, 10, 50000, 0.0004, multiple=8)

x_mean_vals = [np.mean(xGalvo[val[0]:val[1]]) for val in indices]
y_mean_vals = [np.mean(yGalvo[val[0]:val[1]]) for val in indices]

m_x,b_x = np.polyfit(x_mean_vals, x_loc, 1)
m_y,b_y = np.polyfit(y_loc, y_mean_vals, 1)


plt.figure()
plt.plot(x_loc, x_mean_vals)
plt.figure()
plt.plot(y_loc, y_mean_vals)
plt.show()
print('bye')