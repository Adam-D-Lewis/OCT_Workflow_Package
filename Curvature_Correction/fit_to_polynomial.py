import numpy as np
from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig
from HeightData import HeightData
from Pipe_And_Filter_Autosection.classes.AutoSectioner import AutoSectioner
import os
import pickle

#parameters
micronPerPixel = 7.81 #microns per pixel
mmPerPixel = micronPerPixel/1000
z_ref = 520 # mm (35in = 889 mm)
z_c = z_ref+0.55  # mm
h = -1.92  # mm (x offset)
k = -10.697  # mm (y offset)

def generate_sample_data():
    x = np.arange(-25.897, -25.897+51,.03)
    y = np.arange(21.903, 21.903-74.823, -.03)
    X,Y = np.meshgrid(x, y)
    XY = np.vstack((X.flatten(),Y.flatten())).transpose()
    Z = z_func(XY, z_ref, z_c, h, k)*np.random.normal(1, 0.05)
    return XY, Z

# XY, Z = generate_sample_data()
# import matplotlib.pyplot as plt
# plt.plot(Z)
# plt.gca().invert_yaxis()
# plt.show()

# height_data = np.genfromtxt('height.csv', delimiter=',')

def return_offset_values(j_arr_str_path, galvo_file, oct_scan_cfg, plot=1):

    # hd = HeightData(j_arr_str_path, mmPerPixel=mmPerPixel)
    hd = HeightData()
    # with open(os.path.abspath(r'C:\Users\adl628\Box Sync\JavaProjects\OCT_Plugin_REALLY_REAL\src\main\test_data\height_gd_octsc_b2_att1.pickle'), 'wb') as f:
    #     pickle.dump([hd.height_mm, galvo_file, oct_scan_cfg], f)

    # raise('error, lolz')
    with open(os.path.abspath(r'C:\Users\adl628\Box Sync\JavaProjects\OCT_Plugin_REALLY_REAL\src\main\test_data\height_gd_octsc_b2_att1.pickle'), 'rb') as f:
        hd.height_mm, galvo_file, oct_scan_cfg = pickle.load(f)

    hd.filter_height_data(kernal_size=21)
    oct_sc = OCTScanConfig(oct_scan_cfg)
    gd = GalvoData(galvo_file)
    gd.filter_galvo_data(1500)

    # figure out which cutting algorithm was performed on the gd
    if oct_sc.sp['section_alg'] == 'left_to_right_only':
        gd.detect_in_range_indices(oct_sc)
        ause = AutoSectioner('left_to_right_only')
        ause.calc_section_indices(gd.in_range_indices_list)
        nrows = np.shape(ause.sectioned_indices)[0]
        gd.sectioned_x_galvo_data_mm = np.zeros(shape=(nrows, gd.max_indices_per_scanline))
        gd.sectioned_y_galvo_data_mm = np.zeros(shape=(nrows, gd.max_indices_per_scanline))
        for i, si in enumerate(ause.sectioned_indices):
            gd.sectioned_x_galvo_data_mm[i, :] = gd.volt_to_mm(gd.x_filt[si[0]:si[1]], 'x')
            gd.sectioned_y_galvo_data_mm[i, :] = gd.volt_to_mm(gd.y_filt[si[0]:si[1]], 'y')

        hd.polyfit_height_data(gd.sectioned_x_galvo_data_mm, gd.sectioned_y_galvo_data_mm, poly_order=2)
        # hd.plot_height(gd.sectioned_x_galvo_data_mm, gd.sectioned_y_galvo_data_mm, plot_fit=1, plot_error=1)

        # calculate the offset for every XY location
        hd.calc_rel_offset(use_height_data=True)
        hd.write_rel_offset_to_file()

        hd.plot_height(gd.sectioned_x_galvo_data_mm, gd.sectioned_y_galvo_data_mm, 1, 1)

        return
    else:
        raise NotImplementedError(
            "Data cut with the " + oct_sc.sp['section_alg'] + " algorithm is not supported for height correction.  Only the 'left_to_right_only' algorithm is supported.")

return_offset_values(1,1,1)