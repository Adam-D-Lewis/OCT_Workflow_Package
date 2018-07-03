import configparser
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
from Pipe_And_Filter_Autosection.classes.FileManager import FileManager as FM


class ModOCTParameters:
    """

    Args:

    Attributes:

    Properties:


    Todo:
        Make a method to return all the datasets that have already been cut
    """

    key_types = {}
    int_keys = ['Clock', 'Channel', 'Bits', 'Trigger Slope', 'Trigger Source', 'A-Scans Per Transfer', 'B-Scans', 'A-Scans per B-Scan', 'Points Per A-Scan', 'Start Trim', 'Stop Trim',
                'B-Scan Repition']
    for key in int_keys:
        key_types[key] = int
    key_types['Bits'] = lambda x: int(float(x))

    def __init__(self, file_path: str) -> None:
        # initialize vars
        self._file_path = file_path
        self._sp = self._read_config_file(file_path)

    def _read_config_file(self, file_path, section_title='SCAN_SETTINGS'):
        #  returns config if section title isn't given, otherwise it returns the config[section_title] dictionary
        return OCT_SC.read_config_file(file_path, section_title, self.key_types)

    @property
    def file_path(self):
        """returns the file_path of the ModOCTParameters file"""
        return self._file_path

    @property
    def sp(self):
        return self._sp

    def write_to_file(self, key, value, heading='SCAN_SETTINGS'):
        """write to a config file
        Args:
            key:
            value:
            heading:

        Returns:

        """
        FM.write_to_config_file(self.file_path, self.sp, key, value, heading)