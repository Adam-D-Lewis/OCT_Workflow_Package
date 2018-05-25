import configparser
import writeEC1000file as EC
from os import path

#Inputs
# scan_params_filepath = path.abspath(r'E:\OCT Data\2018-04-25 AutoSection Test Data\15by15\scan_params.txt')
# ec1000_xml_savepath = path.abspath(r'E:\OCT Data\2018-04-25 AutoSection Test Data\15by15\15by15.xml')
scan_params_filepath = path.abspath(r'E:\OCT Data\2018-05-24 3PointBars\scan_params.txt')
ec1000_xml_savepath = path.abspath(r'E:\OCT Data\2018-05-24 3PointBars\oct_scan\oct_scan.xml')

#Read Folder
config = configparser.ConfigParser()
config.read(scan_params_filepath)
p = config['Scan_Parameters']

#create file
EC.write_oct_ec1000_file(ec1000_xml_savepath, float(p['left_crd']), float(p['top_crd']), float(p['scan_width']), float(p['scan_height']), float(p['start_delay']), float(p['hatch_spacing']), float(p['galvo_speed']))





