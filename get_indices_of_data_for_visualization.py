from readGalvoFiles import readGalvoFiles
from filters import filter_galvo_data
#returns start_stop locations in a list of lists [[0,5],[10,15]]

def get_indices_of_data_for_visualization(galvo_data_filepath, scan_parameters_filepath):
    #open galvo data
    galvo_data = readGalvoFiles(galvo_data_filepath)

    #filter data
    filt_galvo_data = filter_galvo_data(galvo_data, galvo_speed=1500, scanline_length_mm=20, fs=50000, single_point_change_threshold=0.0004, multiple=8)

    #find contiguous data values (iterator?)