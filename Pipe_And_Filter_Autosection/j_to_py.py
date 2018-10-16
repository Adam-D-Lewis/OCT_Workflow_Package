import numpy as np
import re


def j_array_to_np_array(j_array2D):
    """This method converts an 2D-dimensional java int array (string representation) to a np.array

    Examples/Doctests:
        >>> j_array_str = "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]"
        >>> np_array = np.asarray([[1,2,3],[4,5,6],[7,8,9]])
        >>> np.array_equal(j_array_to_np_array(j_array_str), np_array)
        True

    """
    num_dims = 0
    ch = iter(j_array2D)
    while next(ch) == '[':
         num_dims += 1
    rows = j_array2D.count('[')-num_dims+1
    j_array2D = j_array2D.split(",")
    j_array2D = [int(re.sub("\D", "", item)) for item in j_array2D]
    j_array2D = np.reshape(np.asarray(j_array2D), (rows, -1)).transpose()
    return j_array2D

