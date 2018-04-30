from get_indices_of_data_for_visualization import get_indices_of_data_for_visualization
from read_key_value_coment_file import read_key_value_comment_file
from readGalvoFiles import readGalvoFiles
from filters import filter_galvo_data
import numpy as np
import matplotlib.pyplot as plt
from galvo_voltage_location_conversion import volt_to_mm

galvo_data_filepath = r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\motors_on\OCT Test\Attempt 8\galvo.2d_dbl'
# galvo_data_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\Attempt 4\galvo.2d_dbl'
# scan_params_filepath = r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\Galvos\Galvo Position Signals\scan_params.txt'
# xml_filepath = r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\Galvos\Galvo Position Signals\Galvo Wobble Build Files\12by12.xml'
xml_filepath = r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\Build Files\12by12.xml'
# indices = get_indices_of_data_for_visualization(galvo_data_filepath, scan_params_filepath, xml_filepath)

# params = read_key_value_comment_file(scan_params_filepath)
raw_galvo_data = readGalvoFiles(galvo_data_filepath)[0]
filtered_galvo_data = filter_galvo_data(raw_galvo_data, 1500, 12, fs=50000, multiple=8)

raw_galvo_data = volt_to_mm(raw_galvo_data, 'x')
filtered_galvo_data = volt_to_mm(filtered_galvo_data, 'x')

plt.figure()
plt.plot(raw_galvo_data, label='raw')
plt.plot(filtered_galvo_data, label='filtered')
# for ind, index_pair in enumerate(indices):
#     if ind == 0:
#         plt.plot(range(index_pair[0], index_pair[1]), filtered_galvo_data[index_pair[0]:index_pair[1]], 'r', linewidth=3, label='autosectioned_indices')
#     else:
#         plt.plot(range(index_pair[0], index_pair[1]), filtered_galvo_data[index_pair[0]: index_pair[1]], 'r', linewidth=3)
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
