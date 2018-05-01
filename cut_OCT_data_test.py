from cut_OCT_data_to_indices import cut_OCT_data_to_indices
from read_OCT_bin_files import read_OCT_bin_files
from save_OCT_bin_file import save_OCT_bin_file
from get_indices_of_data_for_visualization import get_indices_of_data_for_visualization
from readGalvoFiles import readGalvoFiles
from filters import filter_galvo_data
import numpy as np
import matplotlib.pyplot as plt
from galvo_voltage_location_conversion import volt_to_mm, mm_to_volt
from resample_scanline2 import resample_scanline2

#read galvo file and get indices
galvo_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\Attempt 10\galvo.2d_dbl' #FIX - need to write the number of points in each file somewhere
scan_parameters_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\scan_params.txt'
xml_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\12by12.xml'

OCT_bin_filepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\Attempt 10\4_34_12 PM 4-30-2018\data.bin'
OCT_bin_savepath = r'E:\OCT Data\2018-04-25 AutoSection Test Data\Attempt 10\4_34_12 PM 4-30-2018\data_mod.bin'

section_indices = get_indices_of_data_for_visualization(galvo_filepath, scan_parameters_filepath, xml_filepath)

#plot
galvo_data = readGalvoFiles(galvo_filepath)
y_data = galvo_data[1]
galvo_data = galvo_data[0]
filtered_galvo = filter_galvo_data(galvo_data, 1500, 12)
filtered_y = filter_galvo_data(y_data, 1500, 12, 50000, 8)

#read OCT_file
OCT_data = read_OCT_bin_files(OCT_bin_filepath)

# plt.figure()
# plt.plot(galvo_data, label='raw')
# plt.plot(filtered_galvo, label='filtered')
galvo_locations = []
mod_OCT_data = np.zeros((2048, 402*359), dtype='>u2')

max_diff = 359

div_vec = np.arange(1,max_diff+1)
resampled_x = np.linspace(mm_to_volt(-5.5, 'x'), mm_to_volt(5.5, 'x'), 359)
for ind, index_pair in enumerate(section_indices):
    store_ind = [ind * max_diff, (ind + 1) * max_diff]
    if ind == 0:
        pass
        # plt.plot(range(index_pair[0], index_pair[1]), filtered_galvo[index_pair[0]:index_pair[1]], 'r', linewidth=3, label='autosectioned_indices')
    else:
        pass
        # plt.plot(range(index_pair[0], index_pair[1]), filtered_galvo[index_pair[0]: index_pair[1]], 'r', linewidth=3)
    scanline_galvo = filtered_galvo[index_pair[0]:index_pair[1]]
    scanline_galvo2 = filtered_galvo[index_pair[0]-1:index_pair[1]+1]
    accounting_vec = np.arange(1, np.size(scanline_galvo2)+1)
    scanline_OCT = OCT_data[:, index_pair[0]:index_pair[0]+max_diff]
    galvo_locations.append(scanline_galvo)
    # mod_OCT_data[:, store_ind[0]:store_ind[1]] = resample_scanline(scanline_galvo2, scanline_OCT, mm_to_volt(-5.5, 'x'), mm_to_volt(5.5, 'x'), 359)
    mod_OCT_data[:, store_ind[0]:store_ind[1]] = resample_scanline2(scanline_galvo2, scanline_OCT, accounting_vec, div_vec, resampled_x)
# plt.legend()
# plt.title('Galvo Position Reading vs. Index')
# plt.xlabel('Index')
# plt.ylabel('Galvo Position Reading (mm)')

# plt.figure()
# plt.plot(y_data, label='raw')
# plt.plot(filtered_y, label='filt')
# plt.show()

galvo_locations = volt_to_mm(np.asarray(galvo_locations), 'x')

plt.figure()
plt.plot(galvo_locations[0], label='0')
plt.plot(galvo_locations[1][::-1], label='1')
plt.legend()
# plt.show()


# mod_OCT_data = cut_OCT_data_to_indices(OCT_data, section_indices)

#check if the same
if np.array_equal(OCT_data[:,section_indices[0][0]:section_indices[0][0]+254], mod_OCT_data[:, 0:254]):
    print(True)
else:
    pass
    # raise('Blah!')

#save OCT file
save_OCT_bin_file(mod_OCT_data, OCT_bin_savepath)