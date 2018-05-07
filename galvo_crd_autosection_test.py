from get_indices_of_data_for_visualization import get_indices_of_data_for_visualization
from read_config_file import read_config_file
from read_galvo_files import read_galvo_files
from filters import filter_galvo_data
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from galvo_voltage_location_conversion import volt_to_mm

matplotlib.get_backend()

galvo_data_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\15by15\first\galvo.2d_dbl'
# galvo_data_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\Attempt 4\galvo.2d_dbl'
scan_params_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\15by15\scan_params.txt'
# xml_filepath = r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\Galvos\Galvo Position Signals\Galvo Wobble Build Files\12by12.xml'
xml_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\15by15\15by15.xml'

# params = read_key_value_comment_file(scan_params_filepath)
raw_galvo_data, y_galvo, _ = read_galvo_files(galvo_data_filepath, 3, 50000)
x_galvo_filt = filter_galvo_data(raw_galvo_data, 1500, 15, fs=50000, multiple=8)[:300000]

sp = read_config_file(scan_params_filepath, 'Scan_Parameters')
#convert sp string values to floats and put in a dictionary
sp = {key: float(val) for key, val in sp.items()}

with open(xml_filepath, 'r') as xml_file:
    #get indices
    section_indices = get_indices_of_data_for_visualization(x_galvo_filt, 'x', sp, xml_file=xml_file)

raw_galvo_data = volt_to_mm(raw_galvo_data, 'x')
x_galvo_filt = volt_to_mm(x_galvo_filt, 'x')

plt.figure()
# plt.plot(raw_galvo_data, label='raw')
plt.plot(x_galvo_filt, label='filtered')
for ind, index_pair in enumerate(section_indices):
    if ind == 0:
        plt.plot(range(index_pair[0], index_pair[1]), x_galvo_filt[index_pair[0]:index_pair[1]], 'r', linewidth=3, label='autosectioned_indices')
    else:
        plt.plot(range(index_pair[0], index_pair[1]), x_galvo_filt[index_pair[0]: index_pair[1]], 'r', linewidth=3)
plt.legend()
plt.title('Galvo Position Reading vs. Index')
plt.xlabel('Index')
plt.ylabel('Galvo Position Reading (mm)')


# diff = [val[1]-val[0] for val in indices]
# diff2 = (params['scan_width']-params['start_trim']-params['stop_trim'])/(np.asarray(diff)/params['fs'])
# plt.figure()
# plt.plot(diff2) #plot speed


plt.show()

print('bye')
