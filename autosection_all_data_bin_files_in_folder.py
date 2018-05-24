if __name__ == "__main__":
    from os import path
    import os
    from autosection_OCT_data import autosection_OCT_data
    import shutil
    import time

    #inputs
    directory = path.abspath(r'E:\OCT Data\2018-05-17 Square_Variations\Log_Files')
    scan_parameters_filepath = path.abspath(r'E:\OCT Data\2018-05-17 Square_Variations\scan_params.txt')
    xml_filepath = path.abspath(r'E:\OCT Data\2018-05-17 Square_Variations\oct_scan\oct_scan.xml')
    blankA_bin_filepath = path.abspath(r'E:\OCT Data\2018-05-17 Square_Variations\blankA\2_43_27 PM 5-17-2018\data.bin')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'data.bin':
                #OCT_bin_filepath
                OCT_bin_filepath = path.join(root, 'data.bin')

                #find OCT parameters filepath
                for f in os.listdir(root):
                    if f.endswith('.oct_scan'):
                        OCT_parameters_filepath = path.join(root, f)

                #find galvo filepath

                parent_dir = path.dirname(root)
                for f in os.listdir(parent_dir):
                    if f.endswith(".2d_dbl"):
                        galvo_filepath = path.join(parent_dir, f)

                # create cut dir if it doesn't exist
                mod_dir = path.join(root, 'cut')
                if not os.path.exists(mod_dir):
                    os.makedirs(mod_dir)

                #OCT savepath
                OCT_bin_savepath = path.join(mod_dir, 'cut_data.bin')

                #cut parameters
                mod_OCT_parameters_filepath = path.join(mod_dir, 'parameters.oct_scan')
                if not os.path.exists(mod_OCT_parameters_filepath):
                    shutil.copyfile(OCT_parameters_filepath, mod_OCT_parameters_filepath)

                #autosection the file
                print('autosectioning {}'.format(OCT_bin_filepath))
                t0 = time.time()
                autosection_OCT_data(galvo_filepath, scan_parameters_filepath, xml_filepath, OCT_bin_filepath, OCT_bin_savepath, mod_OCT_parameters_filepath, num_cores=12, blankA_bin_filepath=blankA_bin_filepath)
                print(time.time()-t0)