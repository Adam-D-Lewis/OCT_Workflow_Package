import socket
import numpy as np
import sys
import io
from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData as GD
from Pipe_And_Filter_Autosection.classes.AutoSectioner import AutoSectioner as AS
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
from HeightData import HeightData as HD
from scipy import interpolate
from tkinter import filedialog, Tk

def calc_interp_rel_height_offset(galvo_filepath, config_filepath):
    # open the file and process it
    oct_sc = OCT_SC(config_filepath)
    gd = GD(file_path=galvo_filepath, OCT_sc=oct_sc)
    hd = HD()
    gd.filter_galvo_data(1500)
    gd.detect_in_range_indices(oct_sc)

    alg_name = oct_sc._secp['section_alg']
    asec = AS(alg_name=alg_name)
    asec.build_sectioning_index_array(gd, asec._alg_name)
    sectioned_x_gd = np.empty(shape=(gd.sectioned_indices_full_list.shape))
    sectioned_y_gd = np.empty(shape=(gd.sectioned_indices_full_list.shape))
    for i, scanline_indices in enumerate(gd.sectioned_indices_full_list):
        sectioned_x_gd[i, :] = gd.volt_to_mm(gd.x_filt[scanline_indices], 'x')
        sectioned_y_gd[i, :] = gd.volt_to_mm(gd.y_filt[scanline_indices], 'y')
    # sectioned_x_gd = sectioned_x_gd.flatten()
    # sectioned_y_gd = sectioned_y_gd.flatten()

    # load the coefficients from config_filepath, if it's not there then ask which to use
    try:
        hd.fit_coeff = oct_sc._secp['height_fit_coefficients']
    except:
        Tk().withdraw()
        coeff_file = filedialog.askopenfilename(initialdir=oct_sc.file_path, title='choose file with fit coefficients', filetypes=(('oct config files', "*.oct_config"),("all files","*.*")))
        coef_oct_sc = OCT_SC(coeff_file)
        oct_sc.write_to_file(key='height_fit_coefficients', value=coeff_file, heading='Sectioning_Parameters')
        oct_sc._secp['height_fit_coefficients'] = coef_oct_sc._secp['height_fit_coefficients']
        hd.fit_coeff = oct_sc._secp['height_fit_coefficients']
    poly_order = int(np.sqrt(hd.fit_coeff.size-2))
    hd.build_A_matrix(sectioned_x_gd, sectioned_y_gd, poly_order)
    hd.calc_rel_height_offset_pix()
    hd.rel_height_offset_pix = hd.rel_height_offset_pix.reshape(gd.sectioned_indices_full_list.shape)
    # if poly_order == 2:
    #     # hd.rel_height_offset_pix = the number of rows is the number of scanlines performed (each row is associated with a unique y value)
    #     y_val = hd.rel_height_offset_pix[:, -1]
    #     a = hd.fit_coeff[0]
    #     b = hd.fit_coeff[1]
    #     c = hd.fit_coeff[2]
    #     d = hd.fit_coeff[3]
    #     e = hd.fit_coeff[4]
    #     f = hd.fit_coeff[5]
    #     x_argmin = -(b+d*y_val)/(2*e)  #took deriv and set equal to 0
    #     coeff = np.empty((np.size(y_val), 3))
    #     coeff[:, 0] = a+c*y_val+f*y_val**2
    #     coeff[:, 1] = b+d*y_val
    #     coeff[:, 2] = e
    #     A = np.empty((np.size(y_val), 3))
    #     for i in range(3):
    #         A[:, i] = x_argmin**i
    #     h_min_at_y = np.sum(A*coeff, axis=1)
    #     h_offset = np.expand_dims(h_min_at_y - np.min(h_min_at_y), 1)
    #     hd.rel_height_offset_pix = hd.rel_height_offset_pix + h_offset


    s = io.StringIO()
    np.savetxt(s, hd.rel_height_offset_pix, delimiter=',', newline='\n', fmt='%i')
    rel_height_offset_str = s.getvalue()
    num_bytes = len(rel_height_offset_str)

    HOST = "localhost"
    PORT = 65500

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(bytearray(str(num_bytes)+"\n", encoding='ascii'))
    sock.send(bytearray(rel_height_offset_str, encoding='ascii'))
    sock.close()
    print("Socket closed")
    # return hd


try:
    calc_interp_rel_height_offset(sys.argv[1], sys.argv[2])
except:
    pass
# galvo_filepath = r'Z:\Adam Lewis\2018_09_07_Nylon12\Logs\45%\179\MessUpNonsymmetric\Layer 0\galvo_post.2d_dbl'
# config_filepath = r'Z:\Adam Lewis\2018_09_07_Nylon12\Logs\45%\179\MessUpNonsymmetric\Layer 0\scan_param.oct_config'
# calc_interp_rel_height_offset(galvo_filepath, config_filepath)
