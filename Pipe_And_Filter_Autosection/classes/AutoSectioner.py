from Pipe_And_Filter_Autosection.classes.OCTData import OCTData
from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
from Pipe_And_Filter_Autosection.classes.OCTParameters import OCTParameters as OCT_P
from Pipe_And_Filter_Autosection.classes.ModOCT import ModOCT
from Pipe_And_Filter_Autosection.classes.OCTEC1000 import OCTEC1000
from Pipe_And_Filter_Autosection.classes.ModOCTParameters import ModOCTParameters
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
from numba import jit


class AutoSectioner:
    """

    Args:
        
    Todo:
        Make a method to return all the datasets that have already been cut
    """
    # def __init__(self):
    #     super().__init__()

    def __init__(self, alg_name=None):
        self._alg_name = alg_name
        self.sectioned_indices = None

    @staticmethod
    @jit
    def _subtract_blankA(dataset, blankA):
        # blankA and dataset should be '>u2' type
        blankA = blankA.astype(np.float64)
        return_data = (dataset.transpose() - blankA).transpose()
        return_data = return_data - np.min(return_data)
        if np.max(return_data) < 2 ** 16:
            return_data = return_data.astype('>u2')
        else:
            raise ("error")
        return return_data

    @property
    def alg_name(self):
        """y galvo location data"""
        return self._alg_name

    @alg_name.setter
    def alg_name(self, alg_name):
        self._alg_name = alg_name

    def autosection_data(self, alg_name: str = 'fast_section', num_cores = 4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None,
                         mod_OCT: ModOCT = None, OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None):
        print(raw_OCT.file_path)
        self._alg_name = alg_name
        OCT_sc.write_to_file('section_alg', alg_name, 'Sectioning_Parameters')
        if alg_name == 'fast_section':
            self._alg_name = 'left_to_right_only'
            alg_name = 'left_to_right_only'

        AutoSectioner.build_sectioning_index_array(galvo_data, self._alg_name)

        if alg_name == 'interp_section':
            #deprecated - use max_alignment instead
            self._interp_section(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc,
                                 OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                                 mod_OCT_param=mod_OCT_param, blankA=blankA)
        elif alg_name == 'left_to_right_only':
            self._one_dir_only(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc,
                               OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                               mod_OCT_param=mod_OCT_param, blankA=blankA, l_to_r=True)
        elif alg_name == 'right_to_left_only':
            self._one_dir_only(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc,
                               OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                               mod_OCT_param=mod_OCT_param, blankA=blankA, l_to_r=False)
        elif alg_name == 'both_dir':
            self._both_dir(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc,
                           OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                           mod_OCT_param=mod_OCT_param, blankA=blankA)
        elif alg_name == 'max_alignment':
            self._max_alignment(num_cores=num_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_sc, OCT_param=OCT_param, mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000,
                                mod_OCT_param=mod_OCT_param, blankA=blankA)
        else:
            raise Exception('Not a valid sectioning algorithm name')

    # @staticmethod
    # def section_galvo_index_list(galvo_data, alg_name):
    #     if alg_name == 'interp_section':
    #         raise Exception(f"not implemented for {alg_name} algorithm")
    #     elif alg_name == 'left_to_right_only':
    #         AutoSectioner.section_galvo_index_list(galvo_data, 'both_dir')
    #         galvo_data.sectioning_index_array = galvo_data.sectioning_index_array[0::2, :]
    #     elif alg_name == 'right_to_left_only':
    #         AutoSectioner.section_galvo_index_list(galvo_data, 'both_dir')
    #         galvo_data.sectioning_index_array = galvo_data.sectioning_index_array[1::2, :]
    #     elif alg_name == 'both_dir':
    #         galvo_data.in_range_indices_list = np.asarray(galvo_data.in_range_indices_list, dtype=np.int64)
    #         galvo_data.sectioning_index_array = galvo_data.in_range_indices_list;
    #         galvo_data.sectioning_index_array[::2, 1] = np.asarray(galvo_data.in_range_indices_list)[::2, 0] + galvo_data.max_indices_per_scanline
    #         galvo_data.sectioning_index_array[1::2, 0] = np.asarray(galvo_data.in_range_indices_list)[1::2, 1] - galvo_data.max_indices_per_scanline
    #     elif alg_name == 'max_alignment':
    #         # calculate indices
    #         galvo_data.in_range_indices_list = np.asarray(galvo_data.in_range_indices_list, dtype=np.int64)
    #         if galvo_data.pattern[-1] < galvo_data.pattern[0]:
    #             galvo_data.pattern = galvo_data.pattern[::-1]
    #
    #         for b_scan_index, data_index in enumerate(galvo_data.in_range_indices_list):
    #             # do all the stuff to get the list of lengths and values of the runs
    #             if b_scan_index % 2 == 0:
    #                 extended_current_b_scan_galvo = galvo_data.x_filt[data_index[0]-galvo_data.max_length_diff:data_index[1]+galvo_data.max_length_diff]
    #             else:
    #                 extended_current_b_scan_galvo = galvo_data.x_filt[data_index[1] + galvo_data.max_length_diff:data_index[0] - galvo_data.max_length_diff:-1]
    #             closest_indices = AutoSectioner.find_index_of_closest(extended_current_b_scan_galvo, galvo_data.pattern)
    #
    #             # if reverse:
    #             if (b_scan_index+1) % 2 == 0:
    #                 closest_indices = closest_indices[::-1]
    #             galvo_data.sectioned_indices_full_list[b_scan_index] = closest_indices

    @staticmethod
    def build_sectioning_index_array(galvo_data, alg_name):
        """This method populates galvo_data.sectioning_index_array which contains the indexes of the galvo/oct data which should populate each pixel of an en face image

        Args:
            galvo_data:
            alg_name:

        Returns:

        """
        galvo_data.in_range_indices_list = np.asarray(galvo_data.in_range_indices_list, dtype=np.int64)
        if alg_name == 'interp_section':
            raise Exception(f"not implemented for {alg_name} algorithm")
        elif alg_name == 'left_to_right_only':
            galvo_data.sectioned_indices_full_list = np.empty((galvo_data.num_ltor_scanlines, galvo_data._max_indices_per_scanline), dtype=np.int64)
            temp_array = np.copy(galvo_data.in_range_indices_list[::2, :])
            temp_array[:, 1] = np.asarray(temp_array)[:, 0] + galvo_data.max_indices_per_scanline
            for i, row in enumerate(temp_array):
                galvo_data.sectioned_indices_full_list[i, :] = np.arange(row[0], row[1], 1)
        elif alg_name == 'right_to_left_only':
            galvo_data.sectioned_indices_full_list = np.empty((galvo_data.ltor_scanlines, galvo_data._max_indices_per_scanline), dtype=np.int64)
            temp_array = np.copy(galvo_data.in_range_indices_list[1::2, :])
            temp_array[:, 0] = np.asarray(temp_array)[:, 1] - galvo_data.max_indices_per_scanline
            for i, row in enumerate(temp_array):
                galvo_data.sectioned_indices_full_list[i, :] = np.arange(row[1], row[0], -1)
        elif alg_name == 'both_dir':
            galvo_data.sectioned_indices_full_list = np.empty((galvo_data.num_scanlines, galvo_data._max_indices_per_scanline), dtype=np.int64)
            temp_array = np.copy(galvo_data.in_range_indices_list)
            temp_array[::2, 1] = np.asarray(temp_array)[::2, 0] + galvo_data.max_indices_per_scanline
            temp_array[1::2, 0] = np.asarray(temp_array)[1::2, 1] - galvo_data.max_indices_per_scanline
            for i, row in enumerate(temp_array):
                if i % 2 == 0:
                    galvo_data.sectioned_indices_full_list[i, :] = np.arange(row[0], row[1], 1)
                else:
                    galvo_data.sectioned_indices_full_list[i, :] = np.arange(row[1], row[0], -1)
        elif alg_name == 'max_alignment':
            galvo_data.sectioned_indices_full_list = np.empty((galvo_data.num_scanlines, galvo_data.pattern.size), dtype=np.int64)

            # calculate indices
            if galvo_data.volt_to_mm(galvo_data.pattern[-1], 'x') < galvo_data.volt_to_mm(galvo_data.pattern[0], 'x'):
                galvo_data.pattern = galvo_data.pattern[::-1]

            for b_scan_index, data_index in enumerate(galvo_data.in_range_indices_list):
                # do all the stuff to get the list of lengths and values of the runs
                if b_scan_index % 2 == 0:
                    extended_current_b_scan_galvo = galvo_data.x_filt[data_index[0]-galvo_data.max_length_diff:data_index[1]+galvo_data.max_length_diff]
                else:
                    extended_current_b_scan_galvo = galvo_data.x_filt[data_index[1] + galvo_data.max_length_diff:data_index[0] - galvo_data.max_length_diff:-1]
                closest_indices = AutoSectioner.find_index_of_closest(extended_current_b_scan_galvo, galvo_data.pattern)

                if (b_scan_index) % 2 == 0:
                    galvo_data.sectioned_indices_full_list[b_scan_index] = data_index[0]-galvo_data.max_length_diff + closest_indices
                else:
                    galvo_data.sectioned_indices_full_list[b_scan_index] = data_index[1]+galvo_data.max_length_diff - closest_indices

    @staticmethod
    def _max_alignment(num_cores=4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None, mod_OCT: ModOCT = None,
                       OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None):

        # save this value as the number of A-scans per B-scan
        mod_OCT_param.write_to_file('A-Scans per B-Scan', galvo_data.pattern.size)
        mod_OCT_param.write_to_file('B-Scans', galvo_data.num_scanlines)

        # allocate memory for modified OCT data
        mod_OCT.allocate_memory_for_sectioned_data(mod_OCT_param)

        # @jit
        def loop_func(b_scan_index, data_indices, galvo_data, mod_OCT: ModOCT, OCT_data: OCTData, blankA: OCTData = None,
                      progress_update=False):
            if progress_update == True:
                if b_scan_index % 100 == 0:
                    print('scan_index is {} of {}.'.format(b_scan_index, galvo_data.num_scanlines))

            storage_index = [b_scan_index*galvo_data.pattern.size, (b_scan_index+1)*galvo_data.pattern.size]
            read_shape = (mod_OCT_param.sp['Points Per A-Scan'], galvo_data.pattern.size+2*galvo_data.max_length_diff)
            if b_scan_index % 2 == 0:
                sectioned_indices_adjusted_to_read_data = data_indices - data_indices[0]
                read_offset = mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_indices[0])
            else:
                sectioned_indices_adjusted_to_read_data = data_indices - data_indices[-1]
                read_offset = mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_indices[-1])
            AutoSectioner.write_mod_OCT_data(mod_OCT, storage_index, OCT_data, read_offset, read_shape, sectioned_indices_adjusted_to_read_data, blankA)

        if num_cores != 1:
            if multiprocessing.cpu_count() < num_cores:
                num_cores = multiprocessing.cpu_count()
            Parallel(n_jobs=num_cores)(
                delayed(loop_func)(b_scan_index, data_indices, galvo_data, mod_OCT, raw_OCT, blankA, progress_update=True) for b_scan_index, data_indices in
                enumerate(galvo_data.sectioned_indices_full_list))
        else:
            for b_scan_index, data_indices in enumerate(galvo_data.sectioned_indices_full_list):
                loop_func(b_scan_index, data_indices, galvo_data, mod_OCT, raw_OCT, blankA, progress_update=True)

        # (galvo_data.in_range_indices_list))
        # for b_scan_index, data_index in enumerate(galvo_data.sectioned_indices_list):
        #     loop_func(b_scan_index, data_index, galvo_data, mod_OCT, raw_OCT, blankA, progress_update=True)

    @staticmethod
    def write_mod_OCT_data(mod_OCT, storage_index, OCT_data, read_offset, read_shape, sub_ind=None, blankA=None):
        if sub_ind is None:
            mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = AutoSectioner.return_OCT_data(OCT_data, read_offset,
                                                                                                       read_shape, blankA)
        else:
            mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = AutoSectioner.return_OCT_data(OCT_data, read_offset, read_shape, blankA)[:, sub_ind]

    @staticmethod
    # @jit
    def return_OCT_data(OCT_data, offset, shape, blankA):
        OCT_scanline = np.memmap(OCT_data.file_path, dtype='>u2', mode='r', offset=int(offset), shape=shape, order='F')
        if blankA is not None:
            OCT_scanline = AutoSectioner._subtract_blankA(OCT_scanline, blankA.data)
        return OCT_scanline

    @staticmethod
    def _both_dir(num_cores=4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None, mod_OCT: ModOCT = None,
                  OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None):

        # save this value as the number of A-scans per B-scan
        mod_OCT_param.write_to_file('A-Scans per B-Scan', galvo_data.max_indices_per_scanline)
        mod_OCT_param.write_to_file('B-Scans', galvo_data.num_scanlines)

        # allocate memory for modified OCT data
        mod_OCT.allocate_memory_for_sectioned_data(mod_OCT_param)


        def loop_func(b_scan_index, data_indices, galvo_data, mod_OCT: ModOCT, OCT_data: OCTData, blankA: OCTData = None, progress_update=False):
            if progress_update == True:
                if b_scan_index % 100 == 0:
                    print('scan_index is {} of {}.'.format(b_scan_index, galvo_data.num_scanlines))

            storage_index = [b_scan_index * galvo_data.max_indices_per_scanline, (b_scan_index + 1) * galvo_data.max_indices_per_scanline]
            read_shape = (mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline)
            if b_scan_index % 2 == 0:
                sectioned_indices_adjusted_to_read_data = data_indices - data_indices[0]
                read_offset = mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_indices[0])
            else:
                sectioned_indices_adjusted_to_read_data = data_indices - data_indices[-1]
                read_offset = mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_indices[-1])
            AutoSectioner.write_mod_OCT_data(mod_OCT, storage_index, OCT_data, read_offset, read_shape, sectioned_indices_adjusted_to_read_data, blankA)

        if multiprocessing.cpu_count() < num_cores:
            num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(
            delayed(loop_func)(scan_index, data_index, galvo_data, mod_OCT, raw_OCT, blankA, progress_update=True) for scan_index, data_index in
            enumerate(galvo_data.sectioned_indices_full_list))

    @staticmethod
    def _one_dir_only(num_cores=4, raw_OCT: OCTData = None, galvo_data: GalvoData = None, OCT_sc: OCT_SC = None, OCT_param: OCT_P = None, mod_OCT: ModOCT = None,
                      OCT_ec1000: OCTEC1000 = None, mod_OCT_param: ModOCTParameters = None, blankA: OCTData = None, l_to_r=True):

        # save this value as the number of A-scans per B-scan
        mod_OCT_param.write_to_file('A-Scans per B-Scan', galvo_data.max_indices_per_scanline)
        mod_OCT_param.write_to_file('B-Scans', galvo_data.calc_num_left_to_right_scanlines())

        # allocate memory for modified OCT data
        mod_OCT.allocate_memory_for_sectioned_data(mod_OCT_param)

        def loop_func(b_scan_index, data_indices, galvo_data, mod_OCT: ModOCT, OCT_data: OCTData, blankA: OCTData=None, progress_update=False):
            if progress_update == True:
                if b_scan_index % 100 == 0:
                    print('b_scan_index is {} of {}.'.format(b_scan_index, galvo_data.num_ltor_scanlines))

            storage_index = [b_scan_index * galvo_data.max_indices_per_scanline, (b_scan_index + 1) * galvo_data.max_indices_per_scanline]
            read_shape = (mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline)
            if l_to_r:
                sectioned_indices_adjusted_to_read_data = data_indices - data_indices[0]
                read_offset = mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_indices[0])
            else:
                sectioned_indices_adjusted_to_read_data = data_indices - data_indices[-1]
                read_offset = mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_indices[-1])
            AutoSectioner.write_mod_OCT_data(mod_OCT, storage_index, OCT_data, read_offset, read_shape, sectioned_indices_adjusted_to_read_data, blankA)

            # storage_index = [b_scan_index * galvo_data.max_indices_per_scanline, (b_scan_index + 1) * galvo_data.max_indices_per_scanline]
            # offset = mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (data_indices[0] - 1)
            # shape = (mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline)
            # if l_to_r:
            #     temp_b_scan = AutoSectioner.return_OCT_data(OCT_data, offset, shape, blankA)
            #     mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = temp_b_scan
            #
            # else:
            #     mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = np.fliplr(np.memmap(OCT_data.file_path, dtype='>u2', mode='r',
            #                                                                                      offset=int(mod_OCT_param.sp['Bits'] // 8 * mod_OCT_param.sp['Points Per A-Scan'] * (
            #                                                                                              data_indices[0] - 1)),
            #                                                                                      shape=(mod_OCT_param.sp['Points Per A-Scan'], galvo_data.max_indices_per_scanline),
            #                                                                                      order='F'))

        if multiprocessing.cpu_count() < num_cores:
            num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(
            delayed(loop_func)(scan_index, data_index, galvo_data, mod_OCT, raw_OCT, blankA, progress_update=True) for scan_index, data_index in enumerate(galvo_data.sectioned_indices_full_list))

    def calc_section_indices(self, galvo_data_indices):
        self.sectioned_indices = AutoSectioner.static_calc_section_indices(galvo_data_indices, self.alg_name)

    @staticmethod
    def static_calc_section_indices(galvo_data_indices, alg_name):
        if alg_name == "left_to_right_only":
            as_sectioned_indices_list = np.asarray(galvo_data_indices[::2], dtype=np.int64)
            as_sectioned_indices_list[:,1] = np.asarray(as_sectioned_indices_list)[:, 0] + np.max(np.diff(galvo_data_indices))
        return as_sectioned_indices_list

    @staticmethod
    def add_blank(mod_OCT, storage_index):
        mod_OCT.mod_OCT_data[:, storage_index[0]:storage_index[1]] = AutoSectioner.return_blank(shape=1, val=1)

    @staticmethod
    def return_blank(shape, val):
        return np.ones(shape=shape, dtype='>u2')*val

    @staticmethod
    def return_run_val_and_length(pattern, cloth):
        closest_indices = AutoSectioner.find_index_of_closest(pattern, cloth)
        add_del_vector = np.diff(closest_indices-np.arange(np.size(closest_indices)))
        run_lengths = GalvoData.run_identifier(add_del_vector)

        total_length = 0

        # to prevent the first two rows having the same value (possibly not needed)
        if add_del_vector[0] == closest_indices[0]:
            run_val_and_length = [[add_del_vector[0], run_lengths[0]+1]]
            total_length = total_length + run_lengths[0]
            run_lengths = run_lengths[1:]
        else:
            run_val_and_length = [[closest_indices[0], 1]]

        for length in run_lengths:
            total_length += length
            run_val_and_length.append([add_del_vector[total_length-1], length])

        for val, length in run_val_and_length:
            if val > 0:
                assert length == 1, 'error here'
            if val < 0:
                assert length == 1, 'error here'
        return run_val_and_length

    @staticmethod
    @jit
    def find_index_of_closest(cloth, pattern):
        # pattern must be sorted
        assert (np.all(np.diff(pattern) >= 0)), 'pattern must be sorted'
        idx = cloth.searchsorted(pattern)
        idx = np.clip(idx, 1, len(cloth) - 1)
        left = cloth[idx - 1]
        right = cloth[idx]
        idx -= pattern - left < right - pattern
        return idx

    @staticmethod
    def shape_and_section_data(data, shaped_index_array):
        """

        Args:
            data: data(1D) to be sectioned on the 1st axis (columns) (m x n)
            shaped_index_array: a 2D array where each element is the data index to keep (mm x nn)

        Returns:
            shaped_and_sectioned_data:  the shaped and sectioned data (m x mm x nn)
        """
        if data.shape.size() == 1:
            # galvo data
            shaped_and_sectioned_data = np.empty(shape=(shaped_index_array.shape), dtype=data.dtype)
            for i, row in enumerate(shaped_index_array):
                shaped_and_sectioned_data[i,:] = data[i, shaped_index_array[i]]
        else:
            raise Exception("Error here")