from Pipe_And_Filter_Autosection.classes.AutoSectioner import AutoSectioner as AS
from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData as GD
import numpy as np
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
import copy
from Pipe_And_Filter_Autosection.HeightData import HeightData as HD
from Pipe_And_Filter_Autosection.calc_interp_rel_height_offset import calc_interp_rel_height_offset
#
# gd = GD()
# gd.pattern = [2, 3, 3.5, 4]
# unit = np.arange(0,8)
# gd._x_filt = np.hstack((unit, unit[::-1], unit, [7, 6, 5, 4, 3.5, 3, 2.5, 2, 1, 0]))
# gd._m_x = 0.0125475
# gd._b_x = 0.06922331
# gd.in_range_indices_list = [[2, 4], [11, 13], [18, 20], [27, 31]]
# gd._max_length_diff = 2
# gd._max_indices_per_scanline = np.max(np.diff(gd.in_range_indices_list, axis=1))
# gd._min_indices_per_scanline = np.min(np.diff(gd.in_range_indices_list, axis=1))
# gd._num_scanlines = np.shape(gd._in_range_indices_list)[0]
#
# AS.build_sectioning_index_array(gd, 'max_alignment')
# AS._max_alignment(num_cores=4, raw_OCT = None, galvo_data = gd, mod_OCT = None, mod_OCT_param = None, blankA = None)

# from Pipe_And_Filter_Autosection.return_csv_galvo_via_tcp_socket import return_csv_galvo_via_tcp_socket as ret
# ret("C:\\Users\\adl628\\Desktop\\Height Correction\\galvo_post.2d_dbl", "C:\\Users\\adl628\\Desktop\\Height Correction\\scan_param.oct_config")

# oct_sc = OCT_SC(r'C:\Users\adl628\Desktop\Height Correction\Layer 0\scan_param.oct_config')

# hd = HD()
oct_sc = OCT_SC(r'Z:\Adam Lewis\OCT Data\2018_10_16 Surface_Fit\logs\fullscan4\scan_param.oct_config')
gd = GD(r'Z:\Adam Lewis\OCT Data\2018_10_16 Surface_Fit\logs\fullscan4\galvo.2d_dbl', OCT_sc=oct_sc)
gd.filter_galvo_data(oct_sc._sp['galvo_speed'])
gd.detect_in_range_indices(oct_sc)
alg_name = oct_sc._secp['section_alg']
asec = AS(alg_name=alg_name)
asec.build_sectioning_index_array(gd, asec._alg_name)

gd.sectioned_x_galvo_data_mm = np.empty(shape=(gd.sectioned_indices_full_list.shape))
gd.sectioned_y_galvo_data_mm = np.empty(shape=(gd.sectioned_indices_full_list.shape))
for i, scanline_indices in enumerate(gd.sectioned_indices_full_list):
    gd.sectioned_x_galvo_data_mm[i, :] = gd.volt_to_mm(gd.x_filt[scanline_indices], 'x')
    gd.sectioned_y_galvo_data_mm[i, :] = gd.volt_to_mm(gd.y_filt[scanline_indices], 'y')

hd = calc_interp_rel_height_offset(gd.file_path, oct_sc.file_path)
hd.height_mm = hd.rel_height_offset_pix*hd.mmPerPixel
print(hd.fit_coeff)
hd.polyfit_height_data(gd.sectioned_x_galvo_data_mm, gd.sectioned_y_galvo_data_mm, 2)
print(hd.fit_coeff)

print('bye')
