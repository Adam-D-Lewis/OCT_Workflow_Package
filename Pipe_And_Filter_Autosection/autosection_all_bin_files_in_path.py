if __name__ == "__main__":
    from os import path
    import time
    import numpy as np
    from joblib import Parallel, delayed
    from Pipe_And_Filter_Autosection.classes.FileManager import FileManager as FM
    from Pipe_And_Filter_Autosection.classes.OCTData import OCTData
    from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData as GD
    from Pipe_And_Filter_Autosection.classes.OCTScanConfig import OCTScanConfig as OCT_SC
    from Pipe_And_Filter_Autosection.classes.OCTParameters import OCTParameters
    from Pipe_And_Filter_Autosection.classes.ModOCT import ModOCT
    from Pipe_And_Filter_Autosection.classes.OCTEC1000 import OCTEC1000
    from Pipe_And_Filter_Autosection.classes.ModOCTParameters import ModOCTParameters
    from Pipe_And_Filter_Autosection.classes.AutoSectioner import AutoSectioner

    # inputs
    num_cores = 2
    sub_cores = 4
    plot = 0
    directory = path.abspath(r'C:\Users\adl628\Desktop\2018_10_16_Surface_Fit\logs')
    # blankA_bin_filepath = path.abspath(r'G:\OCT Data\2018_06_11_3PointBars_Constant_Power\blankA\4_32_12 PM 6-11-2018\data.bin')
    blankA_bin_filepath = None

    fm = FM()
    file_list = fm.find_all_with_filename(directory, 'data.bin', exclude_folder_list=[])
    fileset_list = fm.construct_fileset(file_list, '../', '../', './', './cut/cut_data.bin', '../', './cut/parameters.oct_scan', blankA_bin_filepath)

    def process_data(file_dict):
        # try:
            raw_OCT = OCTData(file_dict['raw_OCT_path'])
            OCT_scan_config = OCT_SC(file_dict['OCT_scan_config_path'])
            galvo_data = GD(file_dict['raw_galvo_path'], OCT_sc=OCT_scan_config)
            OCT_parameters = OCTParameters(file_dict['raw_OCT_parameters_path'])
            mod_OCT = ModOCT(file_dict['mod_OCT_path'])
            OCT_ec1000 = OCTEC1000(file_dict['OCT_EC1000_path'])
            mod_OCT_parameters = ModOCTParameters(file_dict['mod_OCT_parameters_path'])
            blankA = OCTData(file_dict['blank_A_path'])
            auto_sectioner = AutoSectioner()

            OCT_ec1000.record_num_scanlines(mod_OCT_parameters)
            galvo_data.filter_galvo_data(OCT_scan_config.sp['galvo_speed'])
            galvo_data.detect_in_range_indices(OCT_scan_config)

            #load blankA for background subtraction
            galvo_data.set_blankA_indices((-145, 145), (-155, 155))
            if galvo_data.blankA_indices is None:
                if blankA_bin_filepath is not None:
                    blankA = OCTData(blankA_bin_filepath)
                    if np.size(blankA.data) > mod_OCT_parameters.sp['Points Per A-Scan']:
                        blankA.average_data()
                        blankA.save_OCT_bin_file(blankA.data, blankA.file_path)
                else:
                    blankA = None
            else:
                blankA = OCTData(file_dict['raw_OCT_path'])
                blankA.open_data(mod_OCT_parameters, indices_to_open=galvo_data.blankA_indices)
                blankA.average_data()


            if plot:
                galvo_data.plot()
            auto_sectioner.autosection_data(alg_name='max_alignment', num_cores=sub_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_scan_config, OCT_param=OCT_parameters,
                                            mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000, mod_OCT_param=mod_OCT_parameters, blankA=blankA)
        # print('hi')
        # except Exception as e:
        #     print('Failed to process {}'.format(file_dict['raw_OCT_path']))
        #     print(e)
    t0 = time.time()
    if num_cores != 1:
        Parallel(n_jobs=num_cores)(
            delayed(process_data)(file_dict) for file_dict in fileset_list)
    else:
        for file_dict in fileset_list:
            process_data(file_dict)
    dt = time.time()-t0
    print(dt)
