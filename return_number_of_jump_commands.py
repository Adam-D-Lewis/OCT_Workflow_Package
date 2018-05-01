import xml.etree.ElementTree as ET
from os import path
import numpy as np

def return_number_of_jump_commands(xml_filepath):
    # open xml file and parse
    try:
        tree = ET.parse(xml_filepath)
        root = tree.getroot()
    except:  # if it doesn't have overarching tag, then add it
        with open(xml_filepath, 'r') as data:
            data = data.read()
            data = "<BeginJob>\n" + data + "\n</BeginJob>"
            root = ET.fromstring(data)

    ec1000_commands = list(root)
    return_number_of_jump_commands = 0
    for child in ec1000_commands:
        if child.tag.lower() == 'JumpAbs'.lower():
            return_number_of_jump_commands += 1

    return return_number_of_jump_commands