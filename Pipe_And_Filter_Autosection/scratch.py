from Pipe_And_Filter_Autosection.classes.AutoSectioner import AutoSectioner as AS
from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData as GD
import numpy as np
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
import copy
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
value = 'Z:/Adam Lewis/2018_09_07_Nylon12/Logs/45%/179/MessUpNonsymmetric/Layer 0/scan_param.oct_config'
newvalue = copy(value)
for pos, char in enumerate(newvalue):
    if char == '%':
        if value[pos + 1] != '%' and value[pos-1] != '%':
            value = value[:pos] + '%' + value[pos:]


print('bye')

