from scipy import interpolate
import numpy as np
def resample_scanline2(galvo_data, OCT_data, accounting_vec, div_vec, resampled_x):
    # should be a single scanline of data
    #start_resample_x and end_resample_x should have the same units (either volt or mm) as galvo_data
    #accounting vec needs to be the same length as galvo_data
    #div_vec needs to be the same length as resampled_x

    # resampled_x = np.linspace(start_resample_x, end_resample_x, num_pts_x)
    mult_vec = np.interp(resampled_x, galvo_data[::-1], accounting_vec[::-1])
    mult_vec = mult_vec/div_vec
    resampled_y = OCT_data*mult_vec

    # accounting_vec = np.arange(1, len(galvo_data) + 1)
    # div_vec = np.arange(1, len(resampled_x)+1)
    # mult_vec = np.interp(resampled_x, galvo_data[::-1], accounting_vec[::-1])
    # mult_vec = mult_vec/div_vec
    # resampled_y = OCT_data*mult_vec

    # resampled_y_func = interpolate.interp1d(galvo_data, OCT_data)
    # resampled_y = resampled_y_func(resampled_x)
    return resampled_y