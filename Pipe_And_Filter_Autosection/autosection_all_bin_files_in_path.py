if __name__ == "__main__":
    from os import path
    import os
    from autosection_OCT_data import autosection_OCT_data
    import shutil
    import time
    from joblib import Parallel, delayed
    import multiprocessing
    from Pipe_And_Filter_Autosection.classes.FileManager import FileManager as FM
    from Pipe_And_Filter_Autosection.classes.OCTData import OCTData
    from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData as GD
    from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
    from Pipe_And_Filter_Autosection.classes.OCTParameters import OCTParameters
    from Pipe_And_Filter_Autosection.classes.ModOCT import ModOCT
    from Pipe_And_Filter_Autosection.classes.OCTEC1000 import OCTEC1000
    from Pipe_And_Filter_Autosection.classes.ModOCTParameters import ModOCTParameters
    from Pipe_And_Filter_Autosection.classes.AutoSectioner import AutoSectioner
    #inputs
    num_cores = 1
    sub_cores = 1
    plot = 0
    # directory = path.abspath(r'C:\Software\Lamps_3DP_GIT\trunk\OCT\OCT_Manual_Mode\temporary_files')
    directory = path.abspath(r'C:\Users\adl628\Desktop\test')
    # blankA_bin_filepath = path.abspath(r'E:\OCT Data\2018_06_11_3PointBars_Constant_Power\blankA\4_32_12 PM 6-11-2018\data.bin')
    blankA_bin_filepath = None

    fm = FM()
    file_list = fm.find_all_with_filename(directory, 'data.bin', exclude_folder_list=[])
    fileset_list = fm.construct_fileset(file_list, '../', '../', './', './cut/cut_data.bin', '../', './cut/parameters.oct_scan', blankA_bin_filepath)

    def process_data(file_list):
        raw_OCT = OCTData(file_list['raw_OCT_path'])
        galvo_data = GD(file_list['raw_galvo_path'])
        OCT_scan_config = OCT_SC(file_list['OCT_scan_config_path'])
        OCT_parameters = OCTParameters(file_list['raw_OCT_parameters_path'])
        mod_OCT = ModOCT(file_list['mod_OCT_path'])
        OCT_ec1000 = OCTEC1000(file_list['OCT_EC1000_path'])
        mod_OCT_parameters = ModOCTParameters(file_list['mod_OCT_parameters_path'])
        blankA = OCTData(file_list['blank_A_path'])
        auto_sectioner = AutoSectioner()

        OCT_ec1000.record_num_scanlines(mod_OCT_parameters)
        galvo_data.filter_galvo_data(OCT_scan_config.sp['galvo_speed'])
        galvo_data.section_galvo_data(OCT_scan_config)

        #test feature
        import matplotlib.pyplot as plt
        import numpy as np
        l_to_r = galvo_data.sectioned_indices_list[::2]
        l_to_r_galvo = []
        for elem in l_to_r:
            # l_to_r_galvo.append(galvo_data.x_filt[elem[0]:elem[0]+978])
            l_to_r_galvo.append(galvo_data.volt_to_mm(galvo_data.x_filt[elem[0]:elem[0]+984], 'x'))

        r_to_l = galvo_data.sectioned_indices_list[1::2]
        r_to_l_galvo = []
        for elem in r_to_l:
            # r_to_l_galvo.append(galvo_data.x_filt[elem[1]:elem[1]-978:-1])
            r_to_l_galvo.append(galvo_data.volt_to_mm(galvo_data.x_filt[elem[1]:elem[1]-984:-1], 'x'))

        true_sizes = [a[1]-a[0] for a in galvo_data.sectioned_indices_list]
        l_to_r_sizes = true_sizes[::2]
        r_to_l_sizes = true_sizes[1::2]
        # lr_ave = np.mean(l_to_r_galvo, axis=0)
        #
        # rl_ave = np.mean(r_to_l_galvo, axis=0)
        # unique, counts = np.unique(sizes, return_counts=True)
        # size_dict = dict(zip(unique, counts)) #{978: 5, 979: 107, 980: 438, 981: 390, 982: 90, 983: 3, 984: 1}

        # plt.figure()
        # plt.plot(lr_ave)
        # plt.plot(rl_ave, 'b:')

        lr_sm = l_to_r_galvo[np.argmin(l_to_r_sizes)]
        lr_big = l_to_r_galvo[np.argmax(l_to_r_sizes)]
        rl_sm = r_to_l_galvo[np.argmin(r_to_l_sizes)]
        rl_big = r_to_l_galvo[np.argmax(r_to_l_sizes)]

        plt.figure()
        plt.plot(lr_sm, label='lrmin')
        plt.plot(lr_big, label='lrmax')
        plt.plot(rl_sm, ':', label='rlmin')
        plt.plot(rl_big, ':', label='rlmax')
        plt.legend()

        plt.figure()
        plt.plot((lr_sm - lr_big), label='difference')
        plt.plot([0, 984], [np.mean(np.diff(lr_sm))]*2)
        plt.plot([0, 984], [np.mean(np.diff(lr_sm))*2]*2)
        plt.plot([0, 984], [np.mean(np.diff(lr_sm))*3]*2)
        plt.plot([0, 984], [np.mean(np.diff(lr_sm))*4]*2)
        plt.plot([0, 984], [np.mean(np.diff(lr_sm)) * 5] * 2)
        plt.ylabel('microns difference between fast and slow b-scan')

        plt.figure()
        plt.plot(np.diff((lr_sm - lr_big))*1000, label='difference rate')
        plt.plot([0, 984], [1610/50000*1000]*2, label='ave dist travelled per sample')
        plt.ylabel('difference rate in micron/(50kHz)^-1 time')
        plt.legend()

        plt.figure()
        plt.plot(np.diff(lr_sm), label='lr_sm')
        plt.plot(np.diff(lr_big), label='lr_big')
        plt.legend()

        def check_all_and_del_one(small, large):
            temp_large = large[:np.size(small)]
            for el in temp_large:
                temp_smaller_large = temp_large

        # for thing in l_to_r_galvo:
        #     plt.plot(thing)
        #
        # plt.figure()
        # for thing in r_to_l_galvo:
        #     plt.plot(thing)
        plt.show()

        if plot:
            galvo_data.plot()
        auto_sectioner.autosection_data(alg_name='both_dir', num_cores=sub_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_scan_config, OCT_param=OCT_parameters,
                                        mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000, mod_OCT_param=mod_OCT_parameters, blankA=blankA)
        return

    if num_cores != 1:
        Parallel(n_jobs=num_cores)(
            delayed(process_data)(file_dict for file_dict in fileset_list))
    else:
        for file_dict in fileset_list:
            process_data(file_dict)
