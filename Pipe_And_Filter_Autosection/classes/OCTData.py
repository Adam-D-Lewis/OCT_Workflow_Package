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

    @property
    def file_path(self):
        """returns the file_path of the ModOCTParameters file"""
        return self._file_path