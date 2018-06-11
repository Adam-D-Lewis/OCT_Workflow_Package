#add to path
from os import path
import sys
sys.path.append(r'C:\Users\LAMPS_SLS\PycharmProjects\galvos')
sys.path.append(r'C:\Users\LAMPS_SLS\PycharmProjects\galvos\writeXMLBuildFile')


#import other modules
from write_scan_param_file_with_offset_data import write_scan_param_file_with_offset_data
from read_scan_params_create_xml import read_scan_params_create_xml


#temporary filename
#sys.argv = r'blah C:\Software\Lamps_3DP_GIT\trunk\OCT\OCT_Manual_Mode\temporary_files -1.000000 1.000000 1.000000 -1.000000 0.000000 0.000000 0.000000 0.000000 0.000000 0.000000 0.3000'.split(' ')
temp_dir = sys.argv[1]
scan_param_filename = path.join(temp_dir, 'scan_param.oct_config')
a = [float(val) for val in sys.argv[2:]]

write_scan_param_file_with_offset_data(scan_param_filename, a[0:2], a[2:4], a[4], a[5], a[6], a[7], a[8:10], a[10])

#read scan param file and create oct_scan.xml file
oct_scan_filename = path.join(temp_dir, 'oct_scan.xml')
read_scan_params_create_xml(scan_param_filename, oct_scan_filename)

print(oct_scan_filename)

