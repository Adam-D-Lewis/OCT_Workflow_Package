def main():
    #add to path
    from os import path
    import sys
    sys.path.append(r'C:\Users\LAMPS_SLS\PycharmProjects\galvos\LabVIEW_Interface')
    from autosection_folder import autosection_folder

    a = sys.argv[1:]
    directory = a[0]
    blankA_bin_filepath = a[1]
    num_cores = a[2]

    if blankA_bin_filepath == '-1':
        blankA_bin_filepath = None

    autosection_folder(directory, blankA_bin_filepath, num_cores)
    # autosection_folder(r'C:\Software\Lamps_3DP_GIT\trunk\OCT\OCT_Manual_Mode\temporary_files', None, 8)

if __name__ == "__main__":
    main()
