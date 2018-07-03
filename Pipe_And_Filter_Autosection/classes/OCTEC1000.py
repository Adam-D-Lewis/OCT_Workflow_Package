from typing import List, Union, Dict
from os import path
import os
import shutil
from collections import defaultdict
import copy
import matplotlib.pyplot as plt
import numpy as np
# from Pipe_And_Filter_Autosection.classes.Filter import Filter
from filters import single_point_freq_filter, interpolate_masked_data_array, butter_lowpass_filter
import configparser
import xml.etree.ElementTree as ET
from os import path
import numpy as np
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig
from Pipe_And_Filter_Autosection.classes.ModOCTParameters import ModOCTParameters

class OCTEC1000:
    """

    Args:

    Attributes:
        sp (): dictionary of the scan parameters file
        num_scanlines ():
        y_data ():
        x_filt ():
        y_filt ():
        filter_name (str): name of filter applied if any. (unused)
        attr2 (:obj:`int`, optional): Description of `attr2`.

    Properties:
        num_channels: 3
        seg_size: 50,000

    Todo:
        Make a method to return all the datasets that have already been cut
    """

    @property
    def num_scanlines(self):
        return self._num_scanlines

    @property
    def file_path(self):
        return self._file_path

    def __init__(self, file_path: str = None) -> None:
        #initialize vars
        self._file_path = file_path
        self._num_scanlines = OCTScanConfig.return_num_scanlines(xml_file=self.file_path)

    def record_num_scanlines(self, mod_OCT_parameters: ModOCTParameters):
        mod_OCT_parameters.write_to_file('Expected B-Scans', self.num_scanlines)
