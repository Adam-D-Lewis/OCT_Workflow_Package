import xml.etree.ElementTree as ET
from os import path
import numpy as np

def return_num_scanlines(xml_file=None, scan_params=None):
    if xml_file is None:
        if scan_params is None:
            raise('Both inputs can\'t be None')
        else:
            num_scans_to_view = np.size(np.arange(scan_params['top_crd'], scan_params['top_crd'] - scan_params['scan_height'], -scan_params['hatch_spacing']))
            return num_scans_to_view
    else:
        xml_string = xml_file.read()
        # open xml file and parse
        try:
            tree = ET.parse(xml_string)
            root = tree.getroot()
        except:  # if it doesn't have overarching tag, then add it
            xml_string = "<BeginJob>\n" + xml_string + "\n</BeginJob>"
            root = ET.fromstring(xml_string)

        ec1000_commands = list(root)
        return_number_of_jump_commands = 0
        for child in ec1000_commands:
            if child.tag.lower() == 'JumpAbs'.lower():
                return_number_of_jump_commands += 1

        return return_number_of_jump_commands / 2
