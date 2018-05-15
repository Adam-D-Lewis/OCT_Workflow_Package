import numpy as np

def save_OCT_bin_file(data, filepath):
    data.astype('>u2')
    with open(filepath, 'w') as f:
        data.transpose().tofile(f)
