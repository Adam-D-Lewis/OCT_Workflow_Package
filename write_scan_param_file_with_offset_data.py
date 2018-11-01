import configparser
import numpy as np
from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData

def write_scan_param_file_with_offset_data(filename, crd1, crd2, x_spacer = 2.25, y_spacer = 1.75, start_trim = 2, stop_trim = 2, offset_crd = (-0.25, 1.75), new_hatch=0.03, x_fit = [0.012028579168343727, 0.176539806980887], y_fit = [0.01049734457618291, 0.038106664903670096], galvo_speed=3000):
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
    b_scan_estimate = int(round((2060-old_delay*old_OCT_fs/512)*new_area/old_area*(old_hatch/new_hatch)*1500/galvo_speed*1.05+new_delay*new_OCT_fs/512, -1))

    x_m, x_b = x_fit
    y_m, y_b = y_fit

    #write config file
    config = configparser.ConfigParser()
    config['Scan_Parameters'] = {'galvo_speed': str(galvo_speed),
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

    config['Sectioning_Parameters'] = {'x_mm_to_volt_slope': x_m,
                                        'x_mm_to_volt_intercept': x_b,
                                        'y_mm_to_volt_slope': y_m,
                                        'y_mm_to_volt_intercept': y_b}

    with open(filename, 'w') as f:
        config.write(f)

filepath = r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\2018_10_31 Curl Part\oct_scan\Reg\scan_param.oct_config'
write_scan_param_file_with_offset_data(filepath, (-84, 10), (84, -20), x_spacer=0, y_spacer=0, offset_crd=(4.5, -3.5), new_hatch=0.1)
