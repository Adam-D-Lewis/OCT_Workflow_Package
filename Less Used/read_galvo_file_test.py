import matplotlib.pyplot as plt
from read_galvo_files import read_galvo_files
from filters import filter_galvo_data
import numpy as np


neg_galvo_file = r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\2018_17_05_Square_Variations\new_galvo_fit_equation_data\neg100neg100.2d_dbl'
pos_galvo_file = r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\2018_17_05_Square_Variations\new_galvo_fit_equation_data\pos100pos100.2d_dbl'
x_neg, y_neg, _ = read_galvo_files(neg_galvo_file, 3, 50000)
x_pos, y_pos, _ = read_galvo_files(pos_galvo_file, 3, 50000)

x_neg_filt = filter_galvo_data(x_neg, 1500, 10, fs=50000, multiple=8)
y_neg_filt = filter_galvo_data(y_neg, 1500, 10, fs=50000, multiple=8)
x_pos_filt = filter_galvo_data(x_pos, 1500, 10, fs=50000, multiple=8)
y_pos_filt = filter_galvo_data(y_pos, 1500, 10, fs=50000, multiple=8)

for x in [x_neg_filt, y_neg_filt, x_pos_filt, y_pos_filt]:
    print(np.mean(x))

x_ave_neg = np.mean(x_neg_filt)
y_ave_neg = np.mean(y_neg_filt)
x_ave_pos = np.mean(x_pos_filt)
y_ave_pos = np.mean(y_pos_filt)

print(np.polyfit([-100, 100],[x_ave_neg, x_ave_pos], 1))
print(np.polyfit([-100, 100],[y_ave_neg, y_ave_pos], 1))
