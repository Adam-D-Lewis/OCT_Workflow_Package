import numpy as np

def cut_OCT_data_to_indices(OCT_data, indices):
    max_diff = int(np.max(np.diff(indices)))
    print('max_diff is: ' + str(max_diff))
    num_segs = np.shape(indices)[0]
    mod_OCT_data = np.zeros((2048, num_segs*max_diff), dtype='>u2')
    # mod_OCT_data = np.array([], dtype=np.int16).reshape(2048, num_segs*max_diff)
    for index, start_index in enumerate(indices):
        start_index = start_index[0]
        store_ind = [index*max_diff, (index+1)*max_diff]
        if index % 2 == 1:
            #flip the odd indices
            mod_OCT_data[:, store_ind[0]:store_ind[1]] = OCT_data[:, start_index+max_diff:start_index:-1]
        else:
            mod_OCT_data[:, store_ind[0]:store_ind[1]] = OCT_data[:, start_index:start_index + max_diff]

    return mod_OCT_data