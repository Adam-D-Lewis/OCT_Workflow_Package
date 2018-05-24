import numpy as np

def subtract_blankA(dataset, blankA):
    #blankA and dataset should be '>u2' type
    blankA = blankA.astype(np.float64)
    return_data = (dataset.transpose()-blankA).transpose()
    return_data = return_data-np.min(return_data)
    if np.max(return_data) < 2**16:
        return_data = return_data.astype('>u2')
    else:
        raise("error")
    return return_data