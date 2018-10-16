import socket
import numpy as np
import sys
import io
from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData as GD
from Pipe_And_Filter_Autosection.classes.AutoSectioner import AutoSectioner as AS
from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC

def return_csv_galvo_via_tcp_socket(galvo_filepath, config_filepath):
    galvo_filepath = r'Z:\Adam Lewis\2018_09_07_Nylon12\Logs\45%\179\MessUpNonsymmetric\Layer 0\galvo_post.2d_dbl'
    config_filepath = r'Z:\Adam Lewis\2018_09_07_Nylon12\Logs\45%\179\MessUpNonsymmetric\Layer 0\scan_param.oct_config'
    # open the file and process it
    oct_sc = OCT_SC(config_filepath)
    gd = GD(file_path=galvo_filepath, OCT_sc=oct_sc)
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
    sectioned_x_gd = sectioned_x_gd.flatten()
    sectioned_y_gd = sectioned_y_gd.flatten()
    joined_gd_array = np.vstack((sectioned_x_gd, sectioned_y_gd)).transpose()
    # num_lines = joined_gd_array.shape[0]
    csv = io.BytesIO()
    np.savetxt(csv, joined_gd_array, fmt='%.2f', delimiter=',', newline='\n')
    num_bytes = len(csv.getvalue())
    galvo_data_csv = csv.getvalue().decode("ascii")
    # galvo_data_csv = ','.join(['%.5f' % num for num in joined_gd_array])

    # send the galvo data back to java
    HOST = "localhost"
    PORT = 65500

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(bytearray(str(num_bytes)+"\n", encoding='ascii'))
    sock.send(bytearray(galvo_data_csv, encoding='ascii'))
    sock.close()
    print("Socket closed")

# return_csv_galvo_via_tcp_socket(sys.argv[1], sys.argv[2])
return_csv_galvo_via_tcp_socket(1, 1)




