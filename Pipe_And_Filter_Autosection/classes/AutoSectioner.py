from typing import List, Union, Dict
from os import path
import os
import shutil
from collections import defaultdict
import copy
import numpy as np
from Pipe_And_Filter_Autosection.classes.OCTData import OCTData
from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
from Pipe_And_Filter_Autosection.classes.OCTParameters import OCTParameters as OCT_P
from Pipe_And_Filter_Autosection.classes.ModOCT import ModOCT
from Pipe_And_Filter_Autosection.classes.OCTEC1000 import OCTEC1000
from Pipe_And_Filter_Autosection.classes.ModOCTParameters import ModOCTParameters
import numpy as np
from scipy import interpolate
import mmap
from joblib import Parallel, delayed
import multiprocessing
import configparser
from save_OCT_bin_file import save_OCT_bin_file
from read_config_file import read_config_file
import time
from subtract_blankA import subtract_blankA

class AutoSectioner:
    """

    Args:
        
    Todo:
        Make a method to return all the datasets that have already been cut
    """

    @property
    def alg_name(self):
        """y galvo location data"""
        return self._alg_name

    def _fast_section(self, num_cores=4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None, mod_OCT: ModOCT = None,
                      OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None):
        #run left to right algorithm
        self._one_dir_only(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc, OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                           mod_OCT_param=mod_OCT_param, blankA=blankA, l_to_r=True)

    def __init__(self):
        super().__init__()

    def autosection_data(self, alg_name: str = 'fast_section', num_cores = 4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None,
                         mod_OCT: ModOCT = None, OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None):
        self._alg_name = alg_name
        if alg_name == 'fast_section':
            self._fast_section()
        if alg_name == 'interp_section':
            self._interp_section(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc, OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                                 mod_OCT_param=mod_OCT_param, blankA=blankA)
        if alg_name == 'left_to_right_only':
            self._one_dir_only(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc, OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                              mod_OCT_param=mod_OCT_param, blankA=blankA, l_to_r=True)
        if alg_name == 'right_to_left_only':
            self._one_dir_only(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc, OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                               mod_OCT_param=mod_OCT_param, blankA=blankA, l_to_r=False)
        if alg_name == 'both_dir':
            self._both_dir(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc, OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                               mod_OCT_param=mod_OCT_param, blankA=blankA)

    @staticmethod
    def _crop_to_shortest(num_cores=4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None, mod_OCT: ModOCT = None,
                      OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None):
        def loop_func(scan_index, data_index, galvo_data, mod_OCT: ModOCT, OCT_data: OCTData, blankA: OCTData=None, progress_update=False):
            if progress_update == True:
                if scan_index % 100 == 0:
                    print('scan_index is {} of {}.'.format(scan_index, galvo_data.num_scanlines))

            storage_index = [scan_index * galvo_data.max_indices_per_scanline, (scan_index + 1) * galvo_data.max_indices_per_scanline]

            if scan_index % 2 == 0:
                mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = np.memmap(OCT_data.file_path, dtype='>u2', mode='r',
                                                                                    offset=int(mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_index[0] - 1)),
                                                                                    shape=(mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline), order='F')
            else:
                mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = np.fliplr(np.memmap(OCT_data.file_path, dtype='>u2', mode='r',
                                                                                       offset=int(mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (
                                                                                                   data_index[0] - 1)),
                                                                                       shape=(mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline),
                                                                                       order='F'))
        # save this value as the number of A-scans per B-scan
        mod_OCT_param.write_to_file('A-Scans per B-Scan', galvo_data.max_indices_per_scanline)
        mod_OCT_param.write_to_file('B-Scans', galvo_data.num_scanlines)

        # allocate memory for modified OCT data
        mod_OCT.allocate_memory_for_sectioned_data(mod_OCT_param)

        # calculate indices
        galvo_data.sectioned_indices_list = np.asarray(galvo_data.sectioned_indices_list, dtype=np.uint64)
        galvo_data.sectioned_indices_list[::2, 1] = np.asarray(galvo_data.sectioned_indices_list)[::2, 0] + galvo_data.max_indices_per_scanline
        galvo_data.sectioned_indices_list[1::2, 0] = np.asarray(galvo_data.sectioned_indices_list)[1::2, 1] - galvo_data.max_indices_per_scanline
        if multiprocessing.cpu_count() < num_cores:
            num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(
            delayed(loop_func)(scan_index, data_index, galvo_data, mod_OCT, raw_OCT, blankA, progress_update=True) for scan_index, data_index in
            enumerate(galvo_data.sectioned_indices_list))

    @staticmethod
    def _both_dir(num_cores=4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None, mod_OCT: ModOCT = None,
                      OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None):
        def loop_func(scan_index, data_index, galvo_data, mod_OCT: ModOCT, OCT_data: OCTData, blankA: OCTData=None, progress_update=False):
            if progress_update == True:
                if scan_index % 100 == 0:
                    print('scan_index is {} of {}.'.format(scan_index, galvo_data.num_scanlines))

            storage_index = [scan_index * galvo_data.max_indices_per_scanline, (scan_index + 1) * galvo_data.max_indices_per_scanline]

            if scan_index % 2 == 0:
                mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = np.memmap(OCT_data.file_path, dtype='>u2', mode='r',
                                                                                    offset=int(mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_index[0] - 1)),
                                                                                    shape=(mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline), order='F')
            else:
                mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = np.fliplr(np.memmap(OCT_data.file_path, dtype='>u2', mode='r',
                                                                                       offset=int(mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (
                                                                                                   data_index[0] - 1)),
                                                                                       shape=(mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline),
                                                                                       order='F'))
        # save this value as the number of A-scans per B-scan
        mod_OCT_param.write_to_file('A-Scans per B-Scan', galvo_data.max_indices_per_scanline)
        mod_OCT_param.write_to_file('B-Scans', galvo_data.num_scanlines)

        # allocate memory for modified OCT data
        mod_OCT.allocate_memory_for_sectioned_data(mod_OCT_param)

        # calculate indices
        galvo_data.sectioned_indices_list = np.asarray(galvo_data.sectioned_indices_list, dtype=np.uint64)
        galvo_data.sectioned_indices_list[::2, 1] = np.asarray(galvo_data.sectioned_indices_list)[::2, 0] + galvo_data.max_indices_per_scanline
        galvo_data.sectioned_indices_list[1::2, 0] = np.asarray(galvo_data.sectioned_indices_list)[1::2, 1] - galvo_data.max_indices_per_scanline
        if multiprocessing.cpu_count() < num_cores:
            num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(
            delayed(loop_func)(scan_index, data_index, galvo_data, mod_OCT, raw_OCT, blankA, progress_update=True) for scan_index, data_index in
            enumerate(galvo_data.sectioned_indices_list))

    @staticmethod
    def _one_dir_only(num_cores=4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None, mod_OCT: ModOCT = None,
                      OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None, l_to_r=False):

        def loop_func(scan_index, data_index, galvo_data, mod_OCT: ModOCT, OCT_data: OCTData, blankA: OCTData=None, progress_update=False):
            if progress_update == True:
                if scan_index % 100 == 0:
                    print('scan_index is {} of {}.'.format(scan_index, galvo_data.ltor_scanlines))

            storage_index = [scan_index * galvo_data.max_indices_per_scanline, (scan_index + 1) * galvo_data.max_indices_per_scanline]
            if l_to_r:
                mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = np.memmap(OCT_data.file_path, dtype='>u2', mode='r',
                                                                                offset=int(mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_index[0] - 1)),
                                                                                shape=(mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline), order='F')
            else:
                mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = np.fliplr(np.memmap(OCT_data.file_path, dtype='>u2', mode='r',
                                                                                       offset=int(mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (
                                                                                                   data_index[0] - 1)),
                                                                                       shape=(mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline),
                                                                                       order='F'))

        # save this value as the number of A-scans per B-scan
        mod_OCT_param.write_to_file('A-Scans per B-Scan', galvo_data.max_indices_per_scanline)
        mod_OCT_param.write_to_file('B-Scans', galvo_data.calc_num_left_to_right_scanlines())

        # allocate memory for modified OCT data
        mod_OCT.allocate_memory_for_sectioned_data(mod_OCT_param)

        # calculate indices
        if l_to_r:
            galvo_data.sectioned_indices_list = np.asarray(galvo_data.sectioned_indices_list[::2], dtype=np.uint64)
            galvo_data.sectioned_indices_list[:, 1] = np.asarray(galvo_data.sectioned_indices_list)[:, 0] + galvo_data.max_indices_per_scanline
        elif l_to_r==False:
            galvo_data.sectioned_indices_list = np.asarray(galvo_data.sectioned_indices_list[1::2], dtype=np.uint64)
            galvo_data.sectioned_indices_list[:, 0] = np.asarray(galvo_data.sectioned_indices_list)[:, 1] - galvo_data.max_indices_per_scanline
            # galvo_data._sectioned_indices_list[:, 0], galvo_data._sectioned_indices_list[:, 1] = galvo_data._sectioned_indices_list[:, 1], galvo_data._sectioned_indices_list[:, 0]
        if multiprocessing.cpu_count() < num_cores:
            num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(
            delayed(loop_func)(scan_index, data_index, galvo_data, mod_OCT, raw_OCT, blankA, progress_update=True) for scan_index, data_index in enumerate(galvo_data.sectioned_indices_list))

    def _right_to_left_only(self):
        pass

    @staticmethod
    def _interp_section(num_cores=4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None,
                        mod_OCT: ModOCT = None, OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None):
        def resample_single_scanline(resampled_galvo, galvo_scanline, OCT_scanline):
            return interpolate.interp1d(galvo_scanline, OCT_scanline)(resampled_galvo)

        def loop_func(scan_index, data_index, max_length_scan_size, galvo_data, resampled_galvo, mod_OCT_data, OCT_data: OCTData, blankA: OCTData=None, progress_update=False):
            if progress_update == True:
                if scan_index % 100 == 0:
                    print('scan_index is {}'.format(scan_index))
            storage_index = [scan_index * max_length_scan_size, (scan_index + 1) * max_length_scan_size]
            stor_diff = storage_index[1] - storage_index[0]
            index_diff = data_index[1] - data_index[0]
            OCT_bin_filepath = OCT_data.file_path

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
            return

        blankA_bin_filepath = blankA.file_path
        indices = galvo_data.sectioned_indices_list
        max_length_scan_size = galvo_data.max_indices_per_scanline

        # save this value as the number of A-scans per B-scan
        mod_OCT_param.write_to_file('A-Scans per B-Scan', max_length_scan_size)
        mod_OCT_param.write_to_file('B-Scans', galvo_data.num_scanlines)

        # resample galvo data
        left_trimd_crd = GalvoData.mm_to_volt(OCT_sc.left_trimd_crd, 'x')
        right_trimd_crd = GalvoData.mm_to_volt(OCT_sc.right_trimd_crd, 'x')
        resampled_galvo = np.linspace(left_trimd_crd, right_trimd_crd, max_length_scan_size)

        # allocate memory for modified OCT data
        num_segs = galvo_data.num_scanlines
        mod_OCT_data = mod_OCT.allocate_memory_for_sectioned_data(mod_OCT_param)

        # process in parallel
        # if num_cores == 1:
        #     for scan_index, data_index in enumerate(indices):
        #         loop_func(scan_index, data_index, max_length_scan_size, galvo_data.x_filt, resampled_galvo, mod_OCT_data, raw_OCT, blankA_bin_filepath, progress_update=True)
        # else:
        if multiprocessing.cpu_count() < num_cores:
            num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(
            delayed(loop_func)(scan_index, data_index, max_length_scan_size, galvo_data.x_filt, resampled_galvo, mod_OCT_data, raw_OCT, blankA_bin_filepath, progress_update=True)
            for scan_index, data_index in enumerate(indices))

