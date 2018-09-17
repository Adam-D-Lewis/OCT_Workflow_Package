def autosection_OCT_data(galvo_filepath, scan_parameters_filepath, xml_filepath, OCT_bin_filepath, OCT_bin_savepath,
                         mod_OCT_parameters_filepath, num_cores, blankA_bin_filepath=None, alg='fast'):
    # if __name__ == "__main__":
    #import statments
    from get_indices_of_data_for_visualization import get_indices_of_data_for_visualization
    from read_galvo_files import read_galvo_files
    from filters import filter_galvo_data
    import numpy as np
    import matplotlib.pyplot as plt
    from galvo_voltage_location_conversion import volt_to_mm
    from read_config_file import read_config_file
    from return_num_scanlines import return_num_scanlines
    from resample_and_cut_OCT_data import resample_and_cut_OCT_data

    #inputs
    # galvo_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\10-5-2-1 Logs\Layer 10\galvo_post.2d_dbl')
    # scan_parameters_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\scan_params.txt')
    # xml_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\post_OCT_xml\10-5-2-1_29x31.xml') #optional, default value = None
    # # galvo_filepath = path.abspath(r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\motors_on\OCT Test\first\galvo.2d_dbl')
    # # scan_parameters_filepath = path.abspath(r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\motors_on\OCT Test\first\scan_params.txt')
    # # xml_filepath = path.abspath(r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\Build Files\12by12\12by12.xml') #optional, default value = None
    #
    #
    # OCT_bin_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\10-5-2-1 Logs\Layer 10\3_07_15 PM 5-11-2018\orig\data.bin')
    # OCT_bin_savepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\10-5-2-1 Logs\Layer 10\3_07_15 PM 5-11-2018\orig\data_mod.bin')
    # # OCT_bin_filepath = path.abspath(r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\motors_on\OCT Test\first\3_24_40 PM 5-7-2018\data.bin')
    # # OCT_bin_savepath = path.abspath(r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\motors_on\OCT Test\first\3_24_40 PM 5-7-2018\data_mod.bin')
    #
    # OCT_parameters_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\10-5-2-1 Logs\Layer 10\3_07_15 PM 5-11-2018\parameters.oct_scan')
    # mod_OCT_parameters_filepath = path.abspath(r'E:\OCT Data\2018-05-11 Pore Detection\10-5-2-1\10-5-2-1 Logs\Layer 10\3_07_15 PM 5-11-2018\parameters.oct_scan')

    # num_cores = 12
    plot_on = 0
    x_or_y = 'x'
    #end of inputs

    #open the galvo files, scan params files, xml_files, and OCT_data
    x_galvo, y_galvo, _ = read_galvo_files(galvo_filepath, num_channels=3, segSize=50000)
    sp = read_config_file(scan_parameters_filepath, section_title="Scan_Parameters")
    #convert sp string values to floats and put in a dictionary
    sp = {key: float(val) for key, val in sp.items()}

    num_scan_lines = return_num_scanlines(xml_file=None, scan_params=sp)
    x_galvo_filt = filter_galvo_data(x_galvo, sp['galvo_speed'], sp['scan_width'], sp['fs'], multiple=8)
    y_galvo_filt = filter_galvo_data(y_galvo, sp['galvo_speed'], sp['scan_width'], sp['fs'], multiple=8)

    try:
        with open(xml_filepath, 'r') as xml_file:
            #get indices
            section_indices = get_indices_of_data_for_visualization(x_galvo_filt, x_or_y, sp, mod_OCT_parameters_filepath, xml_file=xml_file)
    except:
        plt.figure()
        # plt.plot(volt_to_mm(_, x_or_y), label='laser_enable')
        plt.plot(volt_to_mm(x_galvo, x_or_y), label='raw_error')
        plt.plot(volt_to_mm(x_galvo_filt, x_or_y), label='filtered_error')
        plt.legend()
        plt.figure()
        plt.plot(volt_to_mm(y_galvo_filt, 'y'), label='filtered_y')
        plt.legend()
        plt.show()

    #plot
    if plot_on:
        plt.figure()
        plt.plot(volt_to_mm(x_galvo, x_or_y), label='raw')
        plt.plot(volt_to_mm(x_galvo_filt, x_or_y), label='filtered')
        for inds in section_indices:
            plt.plot(np.arange(inds[0], inds[1]), volt_to_mm(x_galvo_filt[inds[0]:inds[1]], x_or_y), 'r')
        plt.legend()
        plt.title('X Galvo Position Reading vs. Index')
        plt.xlabel('Index')
        plt.ylabel('X Galvo Position Reading (mm)')

        plt.figure()
        # plt.plot(volt_to_mm(y_galvo, 'y'), label='raw')
        plt.plot(volt_to_mm(y_galvo_filt, 'y'), label='filtered')
        plt.legend()
        plt.title('Y Galvo Position Reading vs. Index')
        plt.xlabel('Index')
        plt.ylabel('Y Galvo Position Reading (mm)')

        plt.show()

    #cut the OCT data appropriately
    # t0 = time.time()
    mod_OCT_data = resample_and_cut_OCT_data(section_indices, x_galvo_filt, sp, OCT_bin_filepath, OCT_bin_savepath, mod_OCT_parameters_filepath, num_cores=num_cores, blankA_bin_filepath=blankA_bin_filepath)
    # t1 = time.time()
    # print(t1-t0)
