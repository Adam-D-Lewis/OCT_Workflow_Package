import configparser
import numpy as np

def write_scan_param_file_with_offset_data(filename, crd1, crd2, x_spacer = 2.25, y_spacer = 1.75, start_trim = 1, stop_trim = 1, offset_crd = (-0.25, 1.75), new_hatch=0.03):
    # offset is the adjustment I should make to each crd, its -1 * the location of the OCT center when the galvos are at 0,0

    #account for offset
    crd1 = np.asarray(crd1)+offset_crd
    crd2 = np.asarray(crd2)+offset_crd

    x, y = [], []
    x.append(crd1[0])
    x.append(crd2[0])
    y.append(crd1[1])
    y.append(crd2[1])

    x.sort(), y.sort()
    x[0] -= x_spacer+start_trim
    x[1] += x_spacer+stop_trim
    y[0] -= y_spacer
    y[1] += y_spacer

    #b_scan estimate
    new_area = (y[1]-y[0])*(x[1]-x[0])
    old_area = 28.5*31.5
    old_delay = 0.7
    new_delay = 0.7
    old_OCT_fs = 50000
    new_OCT_fs = 50000
    old_hatch = 0.03
    b_scan_estimate = int(round((2060-old_delay*old_OCT_fs/512)*new_area/old_area*(old_hatch/new_hatch)*1.05+new_delay*new_OCT_fs/512, -1))

    #write config file
    config = configparser.ConfigParser()
    config['Scan_Parameters'] = {'galvo_speed': '1500',
                                    'top_crd': str(y[1]),
                                    'left_crd': str(x[0]),
                                    'scan_height': str(y[1]-y[0]),
                                    'scan_width': str(x[1]-x[0]),
                                    'fs': str(50000),
                                    'hatch_spacing': str(new_hatch),
                                    'start_delay': 1.0,
                                    'start_trim': str(start_trim),
                                    'stop_trim': str(stop_trim),
                                    'num_b_scans_estimate': str(b_scan_estimate)}

    with open(filename, 'w') as f:
        config.write(f)

# filepath = r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\Galvos\oct_scan_large_xml_cylinder\oct_scan.xml'
# write_scan_param_file_with_offset_data(filepath, (-13.75, 13.75), (13.75, -13.75))
