import numpy as np
from scipy import interpolate
from galvo_voltage_location_conversion import mm_to_volt
from joblib import Parallel, delayed
import multiprocessing

def resample_single_scanline(resampled_galvo, galvo_scanline, OCT_scanline):
    try:
        return interpolate.interp1d(galvo_scanline, OCT_scanline)(resampled_galvo)
    except:
        print('ouch')
# OCT_data = np.zeros((2048, 2))
# OCT_data[:, 1] = 1
# galvo_scanline = np.asarray([0, 1])
# resampled_galvo = np.asarray([0, 0.5, 1])
#
# answer = resample_single_scanline(resampled_galvo, galvo_scanline, OCT_data)
# print('bye')

def loop_func(scan_index, data_index, max_length_scan_size, galvo_data, OCT_data, resampled_galvo, mod_OCT_data):
    start_data_index = data_index[0]
    storage_index = [scan_index * max_length_scan_size, (scan_index + 1) * max_length_scan_size]

    galvo_scanline = galvo_data[data_index[0] - 1:data_index[1] + 1]
    OCT_scanline = OCT_data[:, data_index[0] - 1:data_index[1] + 1]
    diff = np.diff(galvo_scanline)

    # I might be able to do this without calculating diff and checking these condiditions (first scanline should be left to right (decreasing signal if voltage)
    if np.all(diff < 0):
        galvo_scanline = galvo_scanline[::-1]
        OCT_scanline = OCT_scanline[:, ::-1]
    elif np.all(diff > 0):
        pass
    else:
        raise ('galvo_scanline is not strictly increasing or decreasing')

    thing = resample_single_scanline(resampled_galvo, galvo_scanline, OCT_scanline)
    mod_OCT_data[:, storage_index[0]:storage_index[1]] = thing
    return

def resample_and_cut_OCT_data(indices, galvo_data, OCT_data, scan_param):

    max_length_scan_size = int(np.max(np.diff(indices)))
    print('max_length_scan_size is: ' + str(max_length_scan_size))

    #resample galvo data
    left_trimd_crd = mm_to_volt(scan_param['left_crd']+scan_param['start_trim'], 'x')
    right_trimd_crd = mm_to_volt(scan_param['left_crd']+scan_param['scan_width']-scan_param['stop_trim'], 'x')
    resampled_galvo = np.linspace(left_trimd_crd, right_trimd_crd, max_length_scan_size)

    #allocate memory for modified OCT data
    num_segs = np.shape(indices)[0]
    mod_OCT_data = np.zeros((2048, num_segs*max_length_scan_size), dtype='>u2')

    #process in parallel
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(loop_func)(scan_index, data_index, max_length_scan_size, galvo_data, OCT_data, resampled_galvo, mod_OCT_data) for scan_index, data_index in enumerate(indices))

    # for scan_index, data_index in enumerate(indices):
    #     start_data_index = data_index[0]
    #     storage_index = [scan_index*max_length_scan_size, (scan_index+1)*max_length_scan_size]
    #
    #     galvo_scanline = galvo_data[data_index[0]-1:data_index[1]+1]
    #     OCT_scanline = OCT_data[:, data_index[0]-1:data_index[1]+1]
    #     diff = np.diff(galvo_scanline)
    #
    #     #I might be able to do this without calculating diff and checking these condiditions (first scanline should be left to right (decreasing signal if voltage)
    #     if np.all(diff < 0):
    #         galvo_scanline = galvo_scanline[::-1]
    #         OCT_scanline = OCT_scanline[:,::-1]
    #     elif np.all(diff > 0):
    #         pass
    #     else:
    #         raise('galvo_scanline is not strictly increasing or decreasing')
    #
    #     thing = resample_single_scanline(resampled_galvo, galvo_scanline, OCT_scanline)
    #     mod_OCT_data[:, storage_index[0]:storage_index[1]] = thing
    return mod_OCT_data