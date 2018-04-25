from readGalvoFiles import readGalvoFiles
from read_key_value_coment_file import read_key_value_comment_file
from galvo_voltage_location_conversion import volt_to_mm, mm_to_volt
from filters import filter_galvo_data
import numpy as np
from return_number_of_jump_commands import return_number_of_jump_commands
#returns start_stop locations in a list of lists [[0,5],[10,15]]

def get_indices_of_data_for_visualization(galvo_data_filepath, scan_parameters_filepath, xml_filepath=None):
    #open galvo data
    galvo_data = readGalvoFiles(galvo_data_filepath)[0] #only need x values

    #open scan parameters
    sp = read_key_value_comment_file(scan_parameters_filepath) #scan params dictionary

    mm_range_values_to_keep = np.asarray([sp['left_crd'] + sp['start_trim'], sp['left_crd'] + sp['scan_width'] - sp['stop_trim']])
    voltage_range_values_to_keep = mm_to_volt(mm_range_values_to_keep, 'x')

    # filter data
    filt_galvo_data = filter_galvo_data(galvo_data, sp['galvo_speed'], sp['scan_width'], sp['fs'], multiple=8)

    #create mask
    filt_galvo_data = np.ma.masked_outside(filt_galvo_data, voltage_range_values_to_keep[0], voltage_range_values_to_keep[1])

    #open OCT data
    def run_identifier(data, stepsize=0):
        split_data = np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
        return split_data

    run_info = run_identifier(filt_galvo_data.mask, 0)

    run_lengths = [np.size(elem) for elem in run_info]

    index_list = []
    run_length_sum = 0
    for i, val in np.ndenumerate(run_lengths):
        run_length_sum += val
        index_list.append(run_length_sum)

    if xml_filepath == None:
        num_scans_to_view = np.size(np.arange(sp['top_crd'], sp['top_crd']-sp['scan_height'], -sp['hatch_spacing']))
    else:
        num_scans_to_view = return_number_of_jump_commands(xml_filepath)/2

    index_list = np.reshape(index_list[-int(num_scans_to_view*2)-1:-1], (-1, 2))

    return index_list.tolist()