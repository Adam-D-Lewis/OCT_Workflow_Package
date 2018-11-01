from read_scan_params_create_xml import read_scan_params_create_xml
from write_scan_param_file_with_offset_data import write_scan_param_file_with_offset_data

write_scan_param_file_with_offset_data(r'./scan_param.oct_config', crd1=(-55, 55), crd2=(55, -55), x_spacer=0, y_spacer=0, start_trim=2, stop_trim=2, offset_crd=0, new_hatch=.6)

scan_params_filepath = r'./scan_param.oct_config'
read_scan_params_create_xml(scan_params_filepath, r'./oct_scan.xml')