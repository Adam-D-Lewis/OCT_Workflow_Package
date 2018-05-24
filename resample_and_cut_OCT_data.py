import numpy as np
from scipy import interpolate
from galvo_voltage_location_conversion import mm_to_volt
import mmap
from joblib import Parallel, delayed
import multiprocessing
import configparser
from save_OCT_bin_file import save_OCT_bin_file
from read_config_file import read_config_file
import time
from subtract_blankA import subtract_blankA

def resample_single_scanline(resampled_galvo, galvo_scanline, OCT_scanline):
    return interpolate.interp1d(galvo_scanline, OCT_scanline)(resampled_galvo)

def loop_func(scan_index, data_index, max_length_scan_size, galvo_data, resampled_galvo, mod_OCT_data, OCT_bin_filepath, blankA_bin_filepath=None):
    storage_index = [scan_index * max_length_scan_size, (scan_index + 1) * max_length_scan_size]
    stor_diff = storage_index[1]-storage_index[0]
    index_diff = data_index[1] - data_index[0]

    galvo_scanline = galvo_data[data_index[0] - 1:data_index[1] + 1]
    OCT_scanline = np.memmap(OCT_bin_filepath, dtype='>u2', mode='r', offset=2 * 2048 * (data_index[0] - 1), shape=(2048, index_diff + 2), order='F')
    # OCT_scanline = np.memmap(OCT_bin_filepath, dtype='>u2', mode='r', offset=2 * 2048 * (data_index[0]), shape=(2048, stor_diff+1), order='F')
    if blankA_bin_filepath is not None:
        blankA_data = np.fromfile(blankA_bin_filepath, dtype='>u2')
        if blankA_data.size > 2048:
            blankA_data = np.reshape(blankA_data, (2048, -1), 'F')
            blankA_data = np.mean(blankA_data, 1).astype('>u2')
            save_OCT_bin_file(blankA_data, blankA_bin_filepath)
    OCT_scanline = subtract_blankA(OCT_scanline, blankA_data)
    mod_OCT_data[:, storage_index[0]:storage_index[1]] = resample_single_scanline(resampled_galvo, galvo_scanline, OCT_scanline)
    # mod_OCT_data[:, storage_index[0]:storage_index[1]] = OCT_scanline[:, 1:1+stor_diff]
    return

def resample_and_cut_OCT_data(indices, galvo_data, scan_param, OCT_bin_filepath, OCT_bin_savepath, mod_OCT_parameters_savepath, num_cores=1, blankA_bin_filepath = None):
    max_length_scan_size = int(np.max(np.diff(indices)))

    #save this value as the number of A-scans per B-scan
    mod_OCT_params = configparser.ConfigParser()
    mod_OCT_params.read(mod_OCT_parameters_savepath)
    mod_OCT_params['SCAN_SETTINGS']['A-scans per B-Scan'] = str(max_length_scan_size)
    with open(mod_OCT_parameters_savepath, 'w') as configfile:
        mod_OCT_params.write(configfile)

    #resample galvo data
    left_trimd_crd = mm_to_volt(scan_param['left_crd']+scan_param['start_trim'], 'x')
    right_trimd_crd = mm_to_volt(scan_param['left_crd']+scan_param['scan_width']-scan_param['stop_trim'], 'x')
    resampled_galvo = np.linspace(left_trimd_crd, right_trimd_crd, max_length_scan_size)

    #allocate memory for modified OCT data
    num_segs = np.shape(indices)[0]
    mod_OCT_data = np.memmap(OCT_bin_savepath, dtype='>u2', mode='w+', offset=0, shape=(2048, num_segs*max_length_scan_size), order='F')

    # process in parallel
    if num_cores == 1:
        for scan_index, data_index in enumerate(indices):
            loop_func(scan_index, data_index, max_length_scan_size, galvo_data, resampled_galvo, mod_OCT_data, OCT_bin_filepath, blankA_bin_filepath)
    else:
        if multiprocessing.cpu_count() < num_cores:
            num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(
            delayed(loop_func)(scan_index, data_index, max_length_scan_size, galvo_data, resampled_galvo, mod_OCT_data, OCT_bin_filepath, blankA_bin_filepath) for scan_index, data_index in
            enumerate(indices))
