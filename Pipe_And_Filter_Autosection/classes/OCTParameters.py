class OCTParameters:
    """

    Args:

    Attributes:

    Properties:


    Todo:
        Make a method to return all the datasets that have already been cut
    """

    key_types = {}
    int_keys = ['Clock', 'Channel', 'Bits', 'Trigger Slope', 'Trigger Source', 'A-Scans Per Transfer', 'B-Scans, A-Scans per B-Scan', 'Points Per A-Scan', 'Start Trim', 'Stop Trim',
                'B-Scan Repition']
    for key in int_keys:
        key_types[key] = int

    def __init__(self, file_path: str = None) -> None:
        #initialize vars
        self._file_path = file_path

    @property
    def file_path(self):
        """returns the file_path of the ModOCTParameters file"""
        return self._file_path



    # def write_to_file(self):
    #     mod_OCT_params = configparser.ConfigParser()
    #     mod_OCT_params.read(mod_OCT_parameters_savepath)
    #     mod_OCT_params['SCAN_SETTINGS']['B-Scans'] = str(np.shape(index_list)[0])
    #     with open(mod_OCT_parameters_savepath, 'w') as configfile:
    #         mod_OCT_params.write(configfile)