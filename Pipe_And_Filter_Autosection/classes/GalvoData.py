import matplotlib.pyplot as plt
import numpy as np
from filters import single_point_freq_filter, interpolate_masked_data_array, butter_lowpass_filter
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
from Pipe_And_Filter_Autosection.classes.OCTEC1000 import OCTEC1000 as OCT_EC
import configparser

class GalvoData():
    """August 7, 2018

    Args:

    Attributes:
        x_data ():
        y_data ():
        x_filt ():
        y_filt ():
        filter_name (str): name of filter applied if any. (unused)
        sectioned_indices_list (:obj:`int`, optional): Description of `attr2`.
        _num_scanlines
    Properties:
        num_channels: 3
        seg_size: 50,000
        num_scanlines: this is the number of whole scanlines collected by the galvos.  It is not necessarily equal to the number of scanlines after sectioning is done since some
        sectioning algorithms may not utilize every scanline.

    Todo:
        Make a method to return all the datasets that have already been cut
    """
    _cutoff_freq = 450

    def __init__(self, file_path: str = None, num_channels: int = 3, seg_size: int = 50000, OCT_sc: OCT_SC = None) -> None:
        #initialize vars
        self._num_channels = num_channels
        self._seg_size = seg_size
        self._filter_name = None
        self._x_data, self._y_data = None, None
        self._x_filt, self._y_filt = None, None
        self._in_range_indices_list = None
        self._sectioned_indices_full_list = None
        self._num_scanlines = None
        self._max_indices_per_scanline = None
        self._num_ltor_scanlines = None
        self._pattern = None
        self._b_scan_lengths = None
        self._max_length_diff = None
        self.sectioned_x_galvo_data_mm = None
        self.sectioned_y_galvo_data_mm = None
        self._m_x = None
        self._b_x = None
        self._m_y = None
        self._b_y = None
        self.blankA_indices = None
        self.file_path = file_path
        if file_path is None:
            pass
        else:
            self.read_galvo_files(file_path, num_channels, seg_size)
        if OCT_sc is not None:
            self.read_m_and_b(OCT_sc)

    @property
    def num_ltor_scanlines(self):
        if self._num_ltor_scanlines is None:
            self.calc_num_left_to_right_scanlines()
        return self._num_ltor_scanlines

    @property
    def sectioned_indices_full_list(self):
        # if self._sectioned_indices_full_list is None:
        #     self._sectioned_indices_full_list = np.empty((self._num_scanlines, self._max_indices_per_scanline), dtype=np.int64)
        return self._sectioned_indices_full_list

    @sectioned_indices_full_list.setter
    def sectioned_indices_full_list(self, sectioned_indices_full_list):
        # if self._sectioned_indices_full_list is None:
        #     self._sectioned_indices_full_list = np.empty(self._num_scanlines, self._max_indices_per_scanline)
        # else:
        self._sectioned_indices_full_list = sectioned_indices_full_list

    def read_m_and_b(self, OCT_sc):
        try:
            self._m_x = OCT_sc._secp['x_mm_to_volt_slope']
            self._b_x = OCT_sc._secp['x_mm_to_volt_intercept']
            self._m_y = OCT_sc._secp['y_mm_to_volt_slope']
            self._b_y = OCT_sc._secp['y_mm_to_volt_intercept']
        except configparser.NoSectionError or configparser.NoOptionError:
            raise Exception("Likely doesn't have slope and intercept of fit defined in the oct_config file")


    @property
    def num_scanlines(self):
        """Number of channels in galvo files (default = 3)"""
        return self._num_scanlines

    @property
    def max_indices_per_scanline(self):
        """Number of channels in galvo files (default = 3)"""
        return self._max_indices_per_scanline

    @property
    def num_channels(self):
        """Number of channels in galvo files (default = 3)"""
        return self._num_channels

    @property
    def seg_size(self):
        """Segment size of each channel in galvo files (default = 50000)"""
        return self._seg_size

    @property
    def filter_name(self):
        """Name of filter applied to galvo data (unused currently)"""
        return self._filter_name

    @property
    def x_data(self):
        """x galvo location data"""
        return self._x_data

    @property
    def y_data(self):
        """y galvo location data"""
        return self._y_data

    @property
    def x_filt(self):
        """x galvo location data"""
        return self._x_filt

    @property
    def y_filt(self):
        """x galvo location data"""
        return self._y_filt

    @property
    def in_range_indices_list(self):
        """y galvo location data"""
        return self._in_range_indices_list

    @in_range_indices_list.setter
    def in_range_indices_list(self, sectioned_indices_list):
        self._in_range_indices_list = sectioned_indices_list

    @property
    def pattern(self):
        if self._pattern is None:
            self._find_pattern_b_scan()
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = pattern


    @property
    def max_length_diff(self):
        if self._max_length_diff is None:
            self._max_length_diff = int(self._max_indices_per_scanline-self._min_indices_per_scanline)
        return self._max_length_diff

    @property
    def filter_name(self):
        """Name of filter applied to galvo data (unused currently)"""
        return self._filter_name

    @property
    def b_scan_lengths(self):
        if self._b_scan_lengths is None:
            self._calc_b_scan_lengths()
        return self._b_scan_lengths

    def _calc_b_scan_lengths(self):
        self._b_scan_lengths = [i[1] - i[0] for i in self._in_range_indices_list]

    def plot(self):
        """plots the x and y galvo data"""
        for set_ in [['self._x_data', 'self._x_filt'], ['self._y_data', 'self._y_filt']]:
            assert set_ is not None, "{} is not defined".format(set_.__name__)

            plt.figure()
            for trace in set_:
                plt.plot(eval(trace))
            plt.title(trace)
            if trace == 'self._x_filt':
                for indices in self.in_range_indices_list:
                    plt.plot(range(indices[0], indices[1]), self._x_filt[indices[0]:indices[1]], 'r')
        plt.show()

    def read_galvo_files(self, filename, num_channels=None, seg_size=None):
        if num_channels is None:
            num_channels = self.num_channels
        else:
            self._num_channels = num_channels

        if seg_size is None:
            seg_size = self.seg_size
        else:
            self._seg_size = seg_size

        data = np.fromfile(filename, dtype='>d')
        if np.size(data) % (num_channels * seg_size) == 0:
            numIter = int(np.size(data) / seg_size)
            channels = [[] for _ in np.arange(num_channels)]
            for i in range(numIter):
                for j in range(num_channels):
                    channels[j] = np.append(channels[j], data[(num_channels * i + j) * seg_size:(num_channels * i + j + 1) * seg_size])
            self._x_data = channels[0]
            self._y_data = channels[1]
            # save other channels?
        else:
            raise ValueError('The filesize isn\'t divisible by ' + str(num_channels * seg_size))

    def filter_galvo_data(self, galvo_speed, fs=50000, multiple=8):
        self._x_filt = self._filter_galvo_data(self._x_data, galvo_speed, fs, multiple)
        self._y_filt = self._filter_galvo_data(self._y_data, galvo_speed, fs, multiple)

    # @staticmethod
    def _filter_galvo_data(self, ma_data_array, galvo_speed, fs=50000, multiple=8):
        # 1
        threshold = np.abs((self.mm_to_volt(galvo_speed / fs, 'x') - self.mm_to_volt(0, 'x')) * multiple)
        ma_data_array = single_point_freq_filter(ma_data_array, threshold)  # single point filter

        # 2
        ma_data_array = interpolate_masked_data_array(ma_data_array)  # interpolate masked data array

        # 3
        ma_data_array = butter_lowpass_filter(ma_data_array, GalvoData._cutoff_freq, fs, order=5)
        return ma_data_array

    # @staticmethod
    def volt_to_mm(self, volt, x_or_y):
        m, b = self.return_m_b(x_or_y, 'volt_to_mm')
        mm = m * volt + b
        return mm

    # @staticmethod
    def mm_to_volt(self, mm, x_or_y):
        m, b = self.return_m_b(x_or_y, 'mm_to_volt')
        volt = m * mm + b
        return volt

    def return_m_b(self, x_or_y, what_to_what):
        if x_or_y == 'x':
            #first
            # m = -0.012546660621089764
            # b = -0.06912179728030933
            #second
            # m = 0.0125475
            # b = 0.06922331
            # third (9/6/18)
            # m = 0.01202708578008938
            # b = 0.1766113594805716
            #final
            m = self._m_x
            b = self._b_x

        elif x_or_y == 'y':
            # first
            # m = -0.012882209183473516
            # b = -0.06530445662203191
            # second
            # m = 0.01288427
            # b = 0.06470308
            # third (9/6/18)
            # m = 0.010475955599136673
            # b = 0.0378721858793456
            # final
            m = self._m_y
            b = self._b_y

        if what_to_what == 'mm_to_volt':
            return m, b
        elif what_to_what == 'volt_to_mm':
            return 1 / m, -b / m

    def detect_in_range_indices(self, OCT_scan_config):
        """

        Args:
            OCT_scan_config:
            mod_OCT_parameters_savepath:

        Returns:

        """
        self._in_range_indices_list = self._get_indices_of_data_for_visualization(self._x_filt, 'x', OCT_scan_config)

    @staticmethod
    def run_identifier(data, stepsize=0):
        """

        Args:
            data: 
            stepsize: 

        Returns:
            index_list: 

        """
        split_data = np.split(data, np.where(np.diff(data) != stepsize)[0] + 1)
        run_lengths = np.asarray([np.size(elem) for elem in split_data])
        return run_lengths

    def _get_indices_of_data_for_visualization(self, filt_galvo_data, x_or_y, OCT_scan_config, tol_mm=0.2):
        """

        Args:
            filt_galvo_data: should be voltage (not mm)
            x_or_y:
            scan_params:
            mod_OCT_parameters_savepath:

        Returns:

        Examples:
            [1,2,3,4,5,5,4,3,2,1] - example galvo data
            [2,4] - voltage_range_values_to_keep
            [1,0,0,0,1,1,0,0,0,1] - filt_galvo_data.mask

        """
        # takes some galvo data and bounds (in mm) to find the indices and returns start_stop indices in a list of lists [[0,5],[10,15]]

        sp = OCT_scan_config.sp
        mm_range_values_to_keep = np.asarray([sp['left_crd'] + sp['start_trim'], sp['left_crd'] + sp['scan_width'] - sp['stop_trim']])
        voltage_range_values_to_keep = self.mm_to_volt(mm_range_values_to_keep, x_or_y)

        # create mask
        filt_galvo_data = np.ma.masked_outside(filt_galvo_data, voltage_range_values_to_keep[0], voltage_range_values_to_keep[1])

        run_lengths = GalvoData.run_identifier(filt_galvo_data.mask, 0)
        index_list = []
        run_length_sum = 0
        for val in run_lengths:
            run_length_sum += val
            index_list.append(run_length_sum-1)  # because index is 1 less than the length

        index_list = np.asarray(index_list)
        index_list = np.vstack((index_list[:-1], index_list[1:])).transpose()
        filtered_index_list = []
        first_found = False
        for ind1, ind2 in index_list:
            if not first_found:
                if self.mm_to_volt(mm_range_values_to_keep[0] - tol_mm, x_or_y) < filt_galvo_data.data[ind1] < self.mm_to_volt(
                        mm_range_values_to_keep[0] + tol_mm, x_or_y):
                    if self.mm_to_volt(mm_range_values_to_keep[1] - tol_mm, x_or_y) < filt_galvo_data.data[ind2] < self.mm_to_volt(
                            mm_range_values_to_keep[1] + tol_mm, x_or_y):
                        first_found = True
                        filtered_index_list.append(ind1)
                        filtered_index_list.append(ind2)
            else:
                if self.mm_to_volt(mm_range_values_to_keep[0] - tol_mm, x_or_y) < filt_galvo_data.data[ind1] < self.mm_to_volt(mm_range_values_to_keep[0] + tol_mm, x_or_y):
                    if self.mm_to_volt(mm_range_values_to_keep[1] - tol_mm, x_or_y) < filt_galvo_data.data[ind2] < self.mm_to_volt(mm_range_values_to_keep[1] + tol_mm, x_or_y):
                        filtered_index_list.append(ind1)
                        filtered_index_list.append(ind2)
                elif self.mm_to_volt(mm_range_values_to_keep[1] - tol_mm, x_or_y) < filt_galvo_data.data[ind1] < self.mm_to_volt(mm_range_values_to_keep[1] + tol_mm, x_or_y):
                    if self.mm_to_volt(mm_range_values_to_keep[0] - tol_mm, x_or_y) < filt_galvo_data.data[ind2] < self.mm_to_volt(mm_range_values_to_keep[0] + tol_mm, x_or_y):
                        filtered_index_list.append(ind1)
                        filtered_index_list.append(ind2)

        index_list = filtered_index_list

        # reshape and cast to list
        index_list = np.reshape(index_list, (-1, 2)).tolist()

        # set number of scanlines
        self._num_scanlines = np.shape(index_list)[0]
        self._max_indices_per_scanline = int(np.max(np.diff(index_list)))
        self._min_indices_per_scanline = int(np.min(np.diff(index_list)))

        return index_list

    def _find_pattern_b_scan(self):
        b_scan_num = np.argmax(self.b_scan_lengths)
        galvo_data_indices = self._in_range_indices_list[b_scan_num]
        self._pattern = self._x_filt[galvo_data_indices[0]:galvo_data_indices[1]]

    def calc_num_left_to_right_scanlines(self):
        """This assumes that we fully captured the first scanline of the dataset

        Returns:

        """
        if self.num_scanlines % 2 != 0:
            # odd number of scanlines
            self._num_ltor_scanlines = int((self.num_scanlines + 1) / 2)
        else:
            self._num_ltor_scanlines = int(self.num_scanlines / 2)
        return self._num_ltor_scanlines

    @staticmethod
    def adjust_to_pattern(cloth, run_val_and_length):
        total_len = np.sum(run_val_and_length, axis=0)[1]
        ind_list = []
        # create ind_list
        for i, vals in enumerate(run_val_and_length):
            val, length = vals
            if val < 0:
                pass
            elif val > 0:
                ind_list.append([ind_list[-1, 1]+1, ind_list[-1, 1]+val+2])
            else:
                ind_list.append([ind_list[-1, 1]+1, ind_list[-1, 1]+length+1])

        adjusted_cloth = np.zeros(shape=total_len)
        length_sum = 0
        for i, vals in enumerate(run_val_and_length):
            val, length = vals
            if val < 0:  # delete
                pass
            elif val > 0:
                adjusted_cloth[ind_list[i, 0]: ind_list[i,1]-1] = [adjusted_cloth[-1]]*length
            else:
                adjusted_cloth[ind_list[i, 0]: ind_list[i,1]] = cloth

    def analyze_volt_to_mm_coeff_file(self, oct_ec: OCT_EC):
        fs = 50000
        # filter the file
        self.filter_galvo_data(oct_ec.get_jump_speed(), fs=50000)
        diff = np.diff(self.x_filt)

    def return_indices_where_position_between_two_crds(self, crd1, crd2):
        x_lims = self.mm_to_volt(np.asarray([crd1[0], crd2[0]]), 'x')
        y_lims = self.mm_to_volt(np.asarray([crd1[1], crd2[1]]), 'y')
        x_ma = np.ma.masked_inside(self.x_filt, x_lims[0], x_lims[1])
        y_ma = np.ma.masked_inside(self.y_filt, y_lims[0], y_lims[1])
        and_mask = x_ma.mask * y_ma.mask
        return np.nonzero(and_mask)[0]

    def set_blankA_indices(self, crd1=(-145, 145), crd2=(-155, 155)):
        blankA_indices = self.return_indices_where_position_between_two_crds(crd1, crd2)
        if np.size(blankA_indices) != 0:
            self.blankA_indices = blankA_indices
        else:
            self.blankA_indices = None

        return self.blankA_indices

        #calculate the coefficients

        #write them to a file in the classes folder

        #read them when I write a new oct_scna file


        #find the middle of all sets of values where the consecutive value is less than a certain value