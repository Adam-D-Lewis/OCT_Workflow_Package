import configparser
import numpy as np
from Pipe_And_Filter_Autosection.classes.ModOCTParameters import ModOCTParameters
class OCTData:
    """

    Args:

    Attributes:

    Properties:


    Todo:
        Make a method to return all the datasets that have already been cut
    """

    def __init__(self, file_path: str) -> None:
        #initialize vars
        self._file_path = file_path
        self.data = None

    @property
    def file_path(self):
        """returns the file_path of the ModOCTParameters file"""
        return self._file_path

    @staticmethod
    def save_OCT_bin_file(data, filepath):
        data = data.astype('>u2')
        with open(filepath, 'w') as f:
            data.transpose().tofile(f)

    def open_data(self, mod_oct_p):
        self.data = np.fromfile(self.file_path, dtype='>u2')
        self.data = np.reshape(self.data, (mod_oct_p.sp['Points Per A-Scan'], -1))
        return self.data
