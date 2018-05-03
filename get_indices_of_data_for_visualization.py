from galvo_voltage_location_conversion import volt_to_mm, mm_to_volt
from filters import filter_galvo_data
import numpy as np
from return_num_scanlines import return_num_scanlines


def get_indices_of_data_for_visualization(filt_galvo_data, x_or_y, scan_params, xml_file=None):
    # takes some galvo data and bounds (in mm) to find the indices and returns start_stop indices in a list of lists [[0,5],[10,15]]

    sp = scan_params
    mm_range_values_to_keep = np.asarray([sp['left_crd'] + sp['start_trim'], sp['left_crd'] + sp['scan_width'] - sp['stop_trim']])
    voltage_range_values_to_keep = mm_to_volt(mm_range_values_to_keep, x_or_y)

    # create mask
    filt_galvo_data = np.ma.masked_outside(filt_galvo_data, voltage_range_values_to_keep[0], voltage_range_values_to_keep[1])

    def run_identifier(data, stepsize=0):
        split_data = np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
        return split_data

    run_info = run_identifier(filt_galvo_data.mask, 0)

    run_lengths = np.asarray([np.size(elem) for elem in run_info])

    index_list = []
    run_length_sum = 0
    for i, val in np.ndenumerate(run_lengths):
        run_length_sum += val
        index_list.append(run_length_sum)

    num_scans_to_view = return_num_scanlines(xml_file=xml_file, scan_params=scan_params)

    # trim index list so we only keep the last num_scans_to_view indices
    index_list = index_list[-int(num_scans_to_view*2)-1:-1]

    # reshape and cast to list
    index_list = np.reshape(index_list, (-1, 2)).tolist()

    return index_list
