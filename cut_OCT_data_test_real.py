from cut_OCT_data_to_indices import cut_OCT_data_to_indices
from read_OCT_bin_files import read_OCT_bin_files
from save_OCT_bin_file import save_OCT_bin_file
from get_indices_of_data_for_visualization import get_indices_of_data_for_visualization
from read_galvo_files import read_galvo_files
from filters import filter_galvo_data
import numpy as np
import matplotlib.pyplot as plt
from galvo_voltage_location_conversion import volt_to_mm, mm_to_volt
from read_config_file import read_config_file
from return_num_scanlines import return_num_scanlines
from resample_and_cut_OCT_data import resample_and_cut_OCT_data
from os import path
import time
from correct_B_scan_with_blank_A_scan import correct_B_scan_with_blank_A_scan

#inputs
# galvo_filepath = path.abspath(r'D:\OCT Test\Attempt 10\galvo.2d_dbl') #FIX - need to write the number of points in each file somewhere
galvo_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\10-5-2-1 Logs\Layer 10\galvo_post.2d_dbl')
scan_parameters_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\scan_params.txt')
xml_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\post_OCT_xml\10-5-2-1_29x31.xml') #optional, default value = None
# blank_Ascan_filepath = path.abspath(r'E:\OCT Data\2018-04-25 AutoSection Test Data\15by15\blankA.bin')

OCT_bin_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\10-5-2-1 Logs\Layer 10\3_07_15 PM 5-11-2018\data.bin')
OCT_bin_savepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\10-5-2-1 Logs\Layer 10\3_07_15 PM 5-11-2018\data_mod.bin')

plot_on = 1
x_or_y = 'x'

#open the galvo files, scan params files, xml_files, and OCT_data
x_galvo, y_galvo, _ = read_galvo_files(galvo_filepath, num_channels=3, segSize=50000)
sp = read_config_file(scan_parameters_filepath, section_title="Scan_Parameters")
#convert sp string values to floats and put in a dictionary
sp = {key: float(val) for key, val in sp.items()}

num_scan_lines = return_num_scanlines(xml_file=None, scan_params=sp)
x_galvo_filt = filter_galvo_data(x_galvo, sp['galvo_speed'], sp['scan_width'], sp['fs'], multiple=8)
y_galvo_filt = filter_galvo_data(y_galvo, sp['galvo_speed'], sp['scan_width'], sp['fs'], multiple=8)

with open(xml_filepath, 'r') as xml_file:
    #get indices
    section_indices = get_indices_of_data_for_visualization(x_galvo_filt, x_or_y, sp, xml_file=xml_file)
OCT_data = read_OCT_bin_files(OCT_bin_filepath)

#subtract out blank A-scan
# blankA = read_OCT_bin_files(blank_Ascan_filepath)
# OCT_data = correct_B_scan_with_blank_A_scan(OCT_data, blankA)

#plot
if plot_on:
    plt.figure()
    # plt.plot(volt_to_mm(x_galvo, x_or_y), label='raw')
    plt.plot(volt_to_mm(x_galvo_filt, x_or_y), label='filtered')
    for inds in section_indices:
        plt.plot(np.arange(inds[0], inds[1]), volt_to_mm(x_galvo_filt[inds[0]:inds[1]], x_or_y), 'r')
    plt.legend()
    plt.title('X Galvo Position Reading vs. Index')
    plt.xlabel('Index')
    plt.ylabel('X Galvo Position Reading (mm)')

    plt.figure()
    # plt.plot(volt_to_mm(y_galvo, 'y'), label='raw')
    plt.plot(volt_to_mm(y_galvo_filt, 'y'), label='filtered')
    plt.legend()
    plt.title('Y Galvo Position Reading vs. Index')
    plt.xlabel('Index')
    plt.ylabel('Y Galvo Position Reading (mm)')

    plt.show()

#cut the OCT data appropriately
t0 = time.time()
mod_OCT_data = resample_and_cut_OCT_data(section_indices, x_galvo_filt, OCT_data, sp)
t1 = time.time()
dt = t1-t0
print(dt)

#save OCT file
save_OCT_bin_file(mod_OCT_data, OCT_bin_savepath)