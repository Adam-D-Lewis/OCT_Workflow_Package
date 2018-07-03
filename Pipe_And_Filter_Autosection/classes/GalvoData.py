from typing import List, Union, Dict
import matplotlib.pyplot as plt
import numpy as np
from filters import single_point_freq_filter, interpolate_masked_data_array, butter_lowpass_filter

class GalvoData:
    """

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

    def __init__(self, file_path: str = None, num_channels: int = 3, seg_size: int = 50000) -> None:
        #initialize vars
        self._num_channels = num_channels
        self._seg_size = seg_size
        self._filter_name = None
        self._x_data, self._y_data = None, None
        self._x_filt, self._y_filt = None, None
        self._sectioned_indices_list = None
        self._num_scanlines = None
        self._max_indices_per_scanline = None
        self.ltor_scanlines = None
        if file_path is None:
            pass
        else:
            self.read_galvo_files(file_path, num_channels, seg_size)

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
    def sectioned_indices_list(self):
        """y galvo location data"""
        return self._sectioned_indices_list

    @sectioned_indices_list.setter
    def sectioned_indices_list(self, sectioned_indices_list):
        self._sectioned_indices_list = sectioned_indices_list



    def plot(self):
        """plots the x and y galvo data"""
        for set_ in [[self._x_data, self._x_filt], [self._y_data, self._y_filt]]:
            assert set_ is not None, "{} is not defined".format(set_.__name__)

            plt.figure()
            for trace in set_:
                plt.plot(trace)
            plt.title(set_.__name__)
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
        self._x_filt = GalvoData._filter_galvo_data(self._x_data, galvo_speed, fs, multiple)
        self._y_filt = GalvoData._filter_galvo_data(self._y_data, galvo_speed, fs, multiple)

    @staticmethod
    def _filter_galvo_data(ma_data_array, galvo_speed, fs=50000, multiple=8):
        # 1
        threshold = np.abs((GalvoData.mm_to_volt(galvo_speed / fs, 'x') - GalvoData.mm_to_volt(0, 'x')) * multiple)
        ma_data_array = single_point_freq_filter(ma_data_array, threshold)  # single point filter

        # 2
        ma_data_array = interpolate_masked_data_array(ma_data_array)  # interpolate masked data array

        # 3
        ma_data_array = butter_lowpass_filter(ma_data_array, GalvoData._cutoff_freq, fs, order=5)
        return ma_data_array

    @staticmethod
    def volt_to_mm(volt, x_or_y):
        m, b = GalvoData._return_m_b(x_or_y, 'volt_to_mm')
        mm = m * volt + b
        return mm

    @staticmethod
    def mm_to_volt(mm, x_or_y):
        m, b = GalvoData._return_m_b(x_or_y, 'mm_to_volt')
        volt = m * mm + b
        return volt

    @staticmethod
    def _return_m_b(x_or_y, what_to_what):
        if x_or_y == 'x':
            # m = -0.012546660621089764
            # b = -0.06912179728030933
            m = 0.0125475
            b = 0.06922331

        elif x_or_y == 'y':
            # m = -0.012882209183473516
            # b = -0.06530445662203191
            m = 0.01288427
            b = 0.06470308

        if what_to_what == 'mm_to_volt':
            return m, b
        elif what_to_what == 'volt_to_mm':
            return 1 / m, -b / m

    def section_galvo_data(self, OCT_scan_config):
        """

        Args:
            OCT_scan_config:
            mod_OCT_parameters_savepath:

        Returns:

        """
        self._sectioned_indices_list = self._get_indices_of_data_for_visualization(self._x_filt, 'x', OCT_scan_config)

    def _get_indices_of_data_for_visualization(self, filt_galvo_data, x_or_y, OCT_scan_config):
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
        voltage_range_values_to_keep = GalvoData.mm_to_volt(mm_range_values_to_keep, x_or_y)

        # create mask
        filt_galvo_data = np.ma.masked_outside(filt_galvo_data, voltage_range_values_to_keep[0], voltage_range_values_to_keep[1])

        def run_identifier(data, stepsize=0):
            split_data = np.split(data, np.where(np.diff(data) != stepsize)[0] + 1)
            return split_data

        run_info = run_identifier(filt_galvo_data.mask, 0)
        run_lengths = np.asarray([np.size(elem) for elem in run_info])

        index_list = []
        run_length_sum = 0
        for i, val in np.ndenumerate(run_lengths):
            run_length_sum += val
            index_list.append(run_length_sum)

        # trim index list so we only keep the last num_scans_to_view indices
        # index_list = index_list[-int(num_scanlines_expected * 2) - 1:-1]

        # discard useless data at beginning
        # figure out if I'm starting left, in the middle, or to the right of the area I want to image
        if GalvoData.volt_to_mm(filt_galvo_data.data[0], x_or_y) < mm_range_values_to_keep[0]:
            # starting to left of area to be imaged
            pass
        elif GalvoData.volt_to_mm(filt_galvo_data.data[0], x_or_y) > mm_range_values_to_keep[0]:
            # starting to the right of the area to be imaged
            index_list = index_list[2:]
        elif mm_range_values_to_keep[0] <= GalvoData.volt_to_mm(filt_galvo_data.data[0], x_or_y) <= mm_range_values_to_keep[1]:
            # starting in the area to be imaged
            index_list = index_list[1:]
        else:
            raise Exception('Unknown error')

        if np.size(index_list) % 2 != 0:
            index_list = index_list[:-1]

        # reshape and cast to list
        index_list = np.reshape(index_list, (-1, 2)).tolist()

        # set number of scanlines
        self._num_scanlines = np.shape(index_list)[0]
        self._max_indices_per_scanline = int(np.max(np.diff(index_list)))

        return index_list

    def calc_num_left_to_right_scanlines(self):
        """This assumes that we fully captured the first scanline of the dataset

        Returns:

        """
        if self.num_scanlines % 2 != 0:
            # odd number of scanlines
            self.ltor_scanlines = int((self.num_scanlines+1)/2)
        else:
            self.ltor_scanlines = int(self.num_scanlines/2)
        return self.ltor_scanlines
