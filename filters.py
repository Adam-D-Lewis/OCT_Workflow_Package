from scipy.signal import butter, lfilter, freqz, filtfilt
import numpy as np

def butter_lowpass(cutoff, fs, order=5): #don't import this one
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def single_point_freq_filter(data_array, single_point_change_threshold):
    diff_first = np.abs(np.diff(data_array)) #2-1
    diff_second = np.insert(diff_first[:-1], 0, 0)
    mx = np.logical_and(diff_first > single_point_change_threshold, diff_second > single_point_change_threshold)
    mx = np.append(mx, False)
    data_array_masked = np.ma.masked_array(data_array, mx)
    return data_array_masked

def interpolate_masked_data_array(ma_data_array):
    ma_data_array = single_point_freq_filter(ma_data_array)
    indices_orig = np.ma.masked_array(range(np.size(ma_data_array)))
    indices = indices_orig[~ma_data_array.mask]
    ma_data_array = ma_data_array[~ma_data_array.mask]
    ma_data_array = np.interp(indices_orig, indices, ma_data_array)
    return ma_data_array

def filter_galvo_data(ma_data_array, galvo_speed, scanline_length_mm, fs=50000, single_point_change_threshold=0.0004, multiple=8):

    # 1
    threshold = single_point_change_threshold * multiple  # I can calculate the single_point_change threshold once I have a mm_voltage conversion function, delete 2nd to last param
    ma_data_array = single_point_freq_filter(ma_data_array, threshold) # single point filter

    # 2
    ma_data_array = interpolate_masked_data_array(ma_data_array) # interpolate masked data array

    # 3
    T = 2*scanline_length_mm / galvo_speed
    signal_freq = 1 / T
    cutoff_freq = 5*signal_freq

    ma_data_array = butter_lowpass_filter(ma_data_array, cutoff_freq, fs, 5)
    return ma_data_array