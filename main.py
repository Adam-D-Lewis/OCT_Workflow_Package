import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
from readGalvoFiles import readGalvoFiles
#%matplotlib notebook

import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


# Filter requirements.
order = 6
fs = 30.0       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Demonstrate the use of the filter.
# First make some data to be filtered.
T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
# plt.show()



[xGalvo, yGalvo] = readGalvoFiles(r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\AutoCutOCT\Galvo Position Signals\motors_on\10.glv')
x_butter = butter_lowpass_filter(xGalvo, 3000, 471000, 5)

plt.figure()
plt.plot(xGalvo)
plt.plot(x_butter)
plt.title('xGalvo')
plt.figure()
plt.plot(yGalvo)

#differentiate and plot
grad = np.gradient(xGalvo)
grad_butter = np.gradient(x_butter)

plt.figure()
plt.plot(grad)
plt.figure()
plt.plot(grad_butter)
# plt.plot(yGalvo)
# plt.title('yGalvo')
plt.show()

print('bye')

#
# fs = 10e3 #sampling frequency
# N = int(1e5) #number of points
# A = 1 #amplitude
# f = 1234.0 #signal frequency
# # noise_power = 0.001 * fs / 2
# t = np.arange(N) / fs #time vector
# x = A*np.sin(2*np.pi*f*t) #sampled signal
# # x += np.random.normal(scale=np.sqrt(noise_power), size=t.shape)
#
# #Compute and plot the power spectral density
# f, Pxx_den = sig.periodogram(x, fs)
# plt.semilogy(f, Pxx_den)
# plt.xlabel('frequency (Hz)')
# plt.ylabel('PSD (V**2/Hz)')
# # plt.show()
#
# #Now compute power spectrum
# wind = sig.get_window('hann', N)
# # print(window)
# f, Pxx_spec = sig.periodogram(x, fs, 'hann', scaling='spectrum')
# plt.figure()
# plt.semilogy(f, np.sqrt(Pxx_spec), label='window1')
# plt.xlabel('frequency [Hz]')
# plt.ylabel('Linear spectrum [V RMS]')
#
# # f, Pxx_spec = sig.periodogram(x, fs, sig.hann(100000, sym=False), scaling='spectrum')
# # plt.semilogy(f, np.sqrt(Pxx_spec), label='window2')
# # plt.legend()
# plt.show()