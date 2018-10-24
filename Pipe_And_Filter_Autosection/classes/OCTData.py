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

    def open_data(self, mod_oct_p, indices_to_open):
        if indices_to_open is None:
            self.data = np.fromfile(self.file_path, dtype='>u2')
            self.data = np.reshape(self.data, (mod_oct_p.sp['Points Per A-Scan'], -1))
        else:
            offset = indices_to_open[0]*mod_oct_p.sp['Bits'] // 8 * mod_oct_p.sp['Points Per A-Scan']
            shape = (mod_oct_p.sp['Points Per A-Scan'], indices_to_open[-1]-indices_to_open[0]+1)
            # (indices_to_open[-1]-indices_to_open[0]+1)*mod_oct_p.sp['Points Per A-Scan']
            self.data = np.memmap(self.file_path, dtype='>u2', mode='r', offset=offset, shape=shape, order='F')
            # self.data = np.reshape(self.data, (mod_oct_p.sp['Points Per A-Scan'], -1))
            self.data = self.data[:, indices_to_open-indices_to_open[0]]

        return self.data

    def average_data(self):
        self.data = np.mean(self.data, axis=1).astype('>u2')
        return self.data