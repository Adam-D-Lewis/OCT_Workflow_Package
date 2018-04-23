import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
from readGalvoFiles import readGalvoFiles
from filters import butter_lowpass_filter
#%matplotlib notebook

import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt
import matplotlib.pyplot as plt

#custom filter
def custom_filter(data_array):
    diff_first = np.abs(np.diff(data_array)) #2-1
    diff_second = np.insert(diff_first[:-1], 0, 0)
    mx = np.logical_and(diff_first > max_real_move, diff_second > max_real_move)
    mx = np.append(mx, False)
    data_array_masked = np.ma.masked_array(data_array, mx)
    return data_array_masked

max_real_move = 8*0.0004


# [xGalvo, yGalvo] = readGalvoFiles(r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\motors_off\100.glv')
[xGalvo, yGalvo] = readGalvoFiles(r'C:\Users\Adam\PycharmProjects\galvos\Galvo Position Signals\motors_on\100.glv')
T = 20/1500
signal_freq = 1/T
fs = 50000

twoX = xGalvo[1145:2534]
butter_twoX = butter_lowpass_filter(twoX, signal_freq, fs, order=5)
butter_twoX2 = butter_lowpass_filter(twoX, signal_freq*3, fs, order=5)
butter_twoX3 = butter_lowpass_filter(twoX, signal_freq*5, fs, order=5)

plt.figure()
plt.suptitle('xGalvo')

plt.subplot(311)
plt.title('Raw vs Filtered Data')
plt.plot(twoX, label='raw')
plt.plot(butter_twoX, label='cutoff=signal freq')
plt.plot(butter_twoX2, label='cutoff=3*signal freq')
plt.plot(butter_twoX3, label='cutoff=5*signal freq')
plt.legend()


plt.subplot(312)
# plt.title('Filtered Data')
# plt.plot(xGalvo)
custom_xGalvo = custom_filter(xGalvo)
indices_orig = np.ma.masked_array(range(np.size(custom_xGalvo)))
indices = indices_orig[~custom_xGalvo.mask]
custom_xGalvo = custom_xGalvo[~custom_xGalvo.mask]

resampled_custom_xGalvo = np.interp(indices_orig, indices, custom_xGalvo)
butter_resample = butter_lowpass_filter(resampled_custom_xGalvo, signal_freq*5, fs, order=5)

plt.plot(butter_lowpass_filter(xGalvo, signal_freq*5, fs, order=5), label='butter_orig')
plt.plot(butter_resample, label='butter_resampled')
plt.plot(resampled_custom_xGalvo, label='custom_filt')
# plt.plot(butter_lowpass_filter(custom_xGalvo, signal_freq*5, fs, order=5), label='butter_custom')
plt.legend()

plt.subplot(313)
#get deriv
resample_grad = np.gradient(butter_resample)
plt.plot(resample_grad)
plt.show()


print('bye')
