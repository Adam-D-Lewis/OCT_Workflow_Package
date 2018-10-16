from Pipe_And_Filter_Autosection.classes.FileManager import FileManager as FM
import configparser
import xml.etree.ElementTree as ET
import numpy as np

class OCTScanConfig:
    """

    Args:

    Attributes:
        sp (): dictionary of the scan parameters file
        num_scanlines ():
        y_data ():
        x_filt ():
        y_filt ():
        filter_name (str): name of filter applied if any.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    Properties:
        num_channels: 3
        seg_size: 50,000

    Todo:
        Make a method to return all the datasets that have already been cut
    """

    @staticmethod
    def height_fit_coeff_read_func(strOrCSV):
        # strOrCSV is either a comma delimited string of numberical coefficients or it is a filepath to the OCT_ScanConfig file where the coefficients are held
        coeff = np.fromstring(strOrCSV, sep=',')
        if coeff.size == 0:
            coeff_oct_sc = OCTScanConfig(strOrCSV)
            coeff = coeff_oct_sc._secp['height_fit_coefficients']
        return coeff

    # values are functions that should be performed for certain keys
    key_types = {'num_b_scans_estimate': int, 'section_alg': str, 'height_fit_coefficients': height_fit_coeff_read_func.__func__}

    def write_to_file(self, key, value, heading='SCAN_SETTINGS'):
        """write to a config file
        Args:
            key:
            value:
            heading:

        Returns:

        """
        if heading.lower() == 'SCAN_SETTINGS'.lower():
            dict_to_write_to = self.sp
        elif heading.lower() == 'Sectioning_Parameters'.lower():
            dict_to_write_to = self._secp
        else:
            raise Exception("Unexpected Section Title")

        FM.write_to_config_file(self.file_path, dict_to_write_to, key, value, heading)

    @property
    def left_trimd_crd(self):
        return self._left_trimd_crd

    @property
    def right_trimd_crd(self):
        return self._right_trimd_crd

    @property
    def num_scanlines(self):
        return self._num_scanlines

    @property
    def sp(self):
        return self._sp

    @property
    def file_path(self):
        return self._file_path

    def __init__(self, file_path: str = None) -> None:
        #initialize vars
        self._file_path = file_path
        self._sp = OCTScanConfig.read_config_file(file_path, "Scan_Parameters", self.key_types)
        self._num_scanlines = None
        self._secp = None
        try:
            self._secp = OCTScanConfig.read_config_file(file_path, 'Sectioning_Parameters', self.key_types)
        except configparser.NoOptionError or configparser.NoSectionError as e:
            pass
        self._left_trimd_crd = self.sp['left_crd'] + self.sp['start_trim']
        self._right_trimd_crd = self.sp['left_crd'] + self.sp['scan_width'] - self.sp['stop_trim']
        self.section_alg = None

    def set_num_scanlines(self):
        self._num_scanlines = OCTScanConfig.return_num_scanlines(None, self._sp)

    @staticmethod
    def read_config_file(filepath, section_title=None, key_type=None):
        #  returns config if section title isn't given, otherwise it returns the config[section_title] dictionary
        config = configparser.ConfigParser()
        config.optionxform = str  # makes config read files case sensitively
        config.read(filepath)
        # print(config.sections())
        if section_title is None:
            config_dict = {}
            for section_title in config.sections():
                temp_config_dict = {}
                for key, val in config[section_title].items():
                    if key in key_type:
                        temp_config_dict[key] = key_type[key](val)
                    else:
                        try:
                            temp_config_dict[key] = float(val)
                        except ValueError:
                            temp_config_dict[key] = val
                config_dict = {**config_dict, **temp_config_dict}  # combine dictionaries from all sections together
            return config_dict
        else:
            config_dict = {}
            for key, val in config[section_title].items():
                if key in key_type:
                    config_dict[key] = key_type[key](val)
                else:
                    try:
                        config_dict[key] = float(val)
                    except ValueError:
                        config_dict[key] = val
            return config_dict


    @staticmethod
    def return_num_scanlines(xml_file=None, scan_params=None):
        if xml_file is None:
            if scan_params is None:
                raise ('Both inputs can\'t be None')
            else:
                num_scans_to_view = np.size(np.arange(scan_params['top_crd'], scan_params['top_crd'] - scan_params['scan_height'], -scan_params['hatch_spacing']))
                return int(num_scans_to_view)
        else:
            ec1000_commands = OCTScanConfig.return_list_of_xml_commands(xml_file)
            return_number_of_jump_commands = 0
            for child in ec1000_commands:
                if child.tag.lower() == 'JumpAbs'.lower():
                    return_number_of_jump_commands += 1

            return int(return_number_of_jump_commands / 2)

    @staticmethod
    def return_list_of_xml_commands(xml_file=None):
        with open(xml_file, 'r') as f:
            xml_string = f.read()
        # open xml file and parse
        try:
            tree = ET.parse(xml_string)
            root = tree.getroot()
        except:  # if it doesn't have overarching tag, then add it
            xml_string = "<BeginJob>\n" + xml_string + "\n</BeginJob>"
            root = ET.fromstring(xml_string)
        xml_commands = list(root)
        return xml_commands
