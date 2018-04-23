from readGalvoFiles import readGalvoFiles
from filters import filter_galvo_data
import numpy as np
#returns start_stop locations in a list of lists [[0,5],[10,15]]

def get_indices_of_data_for_visualization(galvo_data_filepath, scan_parameters_filepath):
    #open galvo data
    galvo_data = readGalvoFiles(galvo_data_filepath)

    #filter data
    filt_galvo_data = filter_galvo_data(galvo_data, galvo_speed=1500, scanline_length_mm=20, fs=50000, single_point_change_threshold=0.0004, multiple=8)

    #open scan parameters
    #just for now ---
    voltage_range_values_to_keep = [-0.1, -0.025]

    #create mask
    filt_galvo_data = np.ma.masked_outside(filt_galvo_data, voltage_range_values_to_keep[0], voltage_range_values_to_keep[1])

    #open OCT data
    def run_identifier(data, stepsize=0):
        split_data = np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

    run_info = run_identifier(filt_galvo_data.mask, 0)

    run_lengths = [np.size(elem) for elem in run_info]

    index_list = []
    run_length_sum = 0
    for i, val in np.ndenumerate(run_lengths):
        run_length_sum += val
        index_list.append(run_length_sum)

    if voltage_range_values_to_keep[0] <= filt_galvo_data[0] <= voltage_range_values_to_keep[1]:
        #first segment is data_in_range, and we don't want the first segment since it was just data going from random coordinate to first outside of range value
        index_list.pop(0)

    np.reshape(index_list, (-1, 2))

    #now I can save the list in the param file?