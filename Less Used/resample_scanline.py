from scipy import interpolate
import numpy as np
def resample_scanline(galvo_data, OCT_data, start_resample_x, end_resample_x, num_pts_x):
    # should be a single scanline of data
    #start_resample_x and end_resample_x should have the same units (either volt or mm) as galvo_data

    resampled_x = np.linspace(start_resample_x, end_resample_x, num_pts_x)

    # accounting_vec = np.arange(1, len(galvo_data) + 1)
    # div_vec = np.arange(1, len(resampled_x)+1)
    # mult_vec = np.interp(resampled_x, galvo_data[::-1], accounting_vec[::-1])
    # mult_vec = mult_vec/div_vec
    # resampled_y = OCT_data*mult_vec

    resampled_y_func = interpolate.interp1d(galvo_data, OCT_data)
    resampled_y = resampled_y_func(resampled_x)
    return resampled_y