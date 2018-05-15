import numpy as np

def read_OCT_bin_files(filepath):
    data = np.fromfile(filepath, dtype='>u2')

    #reshape data
    data = np.reshape(data, (2048, -1), 'F')
    return data