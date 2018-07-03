import configparser
import numpy as np
from Pipe_And_Filter_Autosection.classes.ModOCTParameters import ModOCTParameters
from Pipe_And_Filter_Autosection.classes.OCTData import OCTData


class ModOCT(OCTData):
    """

    Args:

    Attributes:

    Properties:


    Todo:
        Make a method to return all the datasets that have already been cut
    """
    def __init__(self, file_path):
        self.mod_OCT_data = None
        super().__init__(file_path)

    def allocate_memory_for_sectioned_data(self, mod_OCT_param: ModOCTParameters):
        self.mod_OCT_data = np.memmap(self.file_path, dtype='>u2', mode='w+', offset=0,
                                      shape=(mod_OCT_param.sp['Points Per A-Scan'], mod_OCT_param.sp['B-Scans'] * mod_OCT_param.sp['A-Scans per B-Scan']), order='F')
        return self.mod_OCT_data
