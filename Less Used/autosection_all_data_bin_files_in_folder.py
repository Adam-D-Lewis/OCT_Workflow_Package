if __name__ == "__main__":
    from os import path
    import os
    from autosection_OCT_data import autosection_OCT_data
    import shutil
    import time
    from joblib import Parallel, delayed
    import multiprocessing

    #inputs
    parallel = 0
    # directory = path.abspath(r'C:\Software\Lamps_3DP_GIT\trunk\OCT\OCT_Manual_Mode\temporary_files')
    directory = path.abspath(r'G:\2018_06_08 Cylinders\Log Files\OCT\PostBuild8\Right')
    # blankA_bin_filepath = path.abspath(r'E:\OCT Data\2018_06_11_3PointBars_Constant_Power\blankA\4_32_12 PM 6-11-2018\data.bin')
    blankA_bin_filepath = None

    if parallel:
        Parallel(n_jobs=5)(delayed())

                # create cut dir if it doesn't exist
                mod_dir = path.join(root, 'cut')
                if not os.path.exists(mod_dir):
                    os.makedirs(mod_dir)


                #copy cut parameters
                mod_OCT_parameters_filepath = path.join(mod_dir, 'parameters.oct_scan')
                if not os.path.exists(mod_OCT_parameters_filepath):
                    shutil.copyfile(OCT_parameters_filepath, mod_OCT_parameters_filepath)

                #autosection the file
                print('autosectioning {}'.format(OCT_bin_filepath))
                t0 = time.time()
                if parallel:
                    Parallel(n_jobs=5)(delayed(autosection_OCT_data)(galvo_filepath, scan_parameters_filepath, xml_filepath, OCT_bin_filepath, OCT_bin_savepath, mod_OCT_parameters_filepath, num_cores=4, blankA_bin_filepath=blankA_bin_filepath))
                else:
                    autosection_OCT_data(galvo_filepath, scan_parameters_filepath, xml_filepath, OCT_bin_filepath, OCT_bin_savepath, mod_OCT_parameters_filepath, num_cores=4,
                                         blankA_bin_filepath=blankA_bin_filepath)

                print(time.time()-t0)
                # Parallel(n_jobs=num_cores)(
                #     delayed(loop_func)(scan_index, data_index, max_length_scan_size, galvo_data, resampled_galvo, mod_OCT_data, OCT_bin_filepath, blankA_bin_filepath) for
                #     scan_index, data_index in
                #     enumerate(indices))