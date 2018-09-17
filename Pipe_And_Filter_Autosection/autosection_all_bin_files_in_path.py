if __name__ == "__main__":
    from os import path
    import time
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
    num_cores = 1
    sub_cores = 1
    plot = 0
    directory = path.abspath(r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\2018_09_10_Nylon 12\log_files\Layer 19')
    # blankA_bin_filepath = path.abspath(r'G:\2018_06_13_Flex Bars_Variable_Power\blankA\12_48_47 PM 6-13-2018\data.bin')
    blankA_bin_filepath = None

    fm = FM()
    file_list = fm.find_all_with_filename(directory, 'data.bin', exclude_folder_list=[])
    fileset_list = fm.construct_fileset(file_list, '../', '../', './', './cut/cut_data.bin', '../', './cut/parameters.oct_scan', blankA_bin_filepath)

    def process_data(file_dict):
        # try:
        raw_OCT = OCTData(file_dict['raw_OCT_path'])
        galvo_data = GD(file_dict['raw_galvo_path'])
        OCT_scan_config = OCT_SC(file_dict['OCT_scan_config_path'])
        OCT_parameters = OCTParameters(file_dict['raw_OCT_parameters_path'])
        mod_OCT = ModOCT(file_dict['mod_OCT_path'])
        OCT_ec1000 = OCTEC1000(file_dict['OCT_EC1000_path'])
        mod_OCT_parameters = ModOCTParameters(file_dict['mod_OCT_parameters_path'])
        blankA = OCTData(file_dict['blank_A_path'])
        auto_sectioner = AutoSectioner()

        OCT_ec1000.record_num_scanlines(mod_OCT_parameters)
        galvo_data.filter_galvo_data(OCT_scan_config.sp['galvo_speed'])
        galvo_data.section_galvo_data(OCT_scan_config)

        if plot:
            galvo_data.plot()
        auto_sectioner.autosection_data(alg_name='left_to_right_only', num_cores=sub_cores, raw_OCT=raw_OCT, galvo_data=galvo_data, OCT_sc=OCT_scan_config, OCT_param=OCT_parameters,
                                        mod_OCT=mod_OCT, OCT_ec1000=OCT_ec1000, mod_OCT_param=mod_OCT_parameters, blankA=blankA)
        # except:
        #     print('Failed to process {}'.format(file_dict['raw_OCT_path']))
    t0 = time.time()
    Parallel(n_jobs=num_cores)(
        delayed(process_data)(file_dict) for file_dict in fileset_list)
    # for file_dict in fileset_list:
    #     process_data(file_dict)
    dt = time.time()-t0
    print(dt)
