from typing import List, Union, Dict
from os import path
import os
import shutil
from collections import defaultdict
import copy
import configparser

class FileManager:
    """FileManager keeps track of all files used in the sectioning OCT algorithm

    Args:
        
    Todo:
        Make a method to return all the datasets that have already been cut
    """

    @staticmethod
    def construct_fileset(file_list: List[str], raw_galvo_relpath, OCT_scan_config_relpath, raw_OCT_parameters_relpath, mod_OCT_relpath, OCT_EC1000_relpath, mod_OCT_parameters_relpath, blank_A_path='') -> List[Dict[str, str]]:
        """This method constucts a list of OCT fileset dictionaries from a list of .bin files and the relative paths to the other files and the absolute path to the blank_A_dataset

        Args:
            file_list:
            file_list: contains raw_OCT_paths
            raw_galvo_relpath:
            OCT_scan_config_relpath:
            raw_OCT_parameters_relpath:
            mod_OCT_relpath:
            OCT_EC1000_relpath:
            mod_OCT_parameters_relpath:
            blank_A_path:

        Returns:
            filset_list = List[Dict[str
        Note:  It is important that the arguments which are relative paths have 'relpath' in their name, and that those that are not relative paths, do not have 'relpath' in their name
        """
        extension_dict = {'raw_OCT_path': '.bin', 'raw_galvo_relpath': '.2d_dbl', 'OCT_scan_config_relpath': '.oct_config', 'raw_OCT_parameters_relpath': '.oct_scan', 'mod_OCT_relpath': '.bin',
                          'OCT_EC1000_relpath': '.xml', 'mod_OCT_parameters_relpath': 'oct_scan', 'blank_A_path': '.bin'}
        fileset_list = []
        for file in file_list:
            fileset_dict = {'raw_OCT_path': file}
            fileset_list.append(fileset_dict)
            for var, val in (('raw_galvo_relpath', raw_galvo_relpath), ('OCT_scan_config_relpath', OCT_scan_config_relpath), ('raw_OCT_parameters_relpath', raw_OCT_parameters_relpath), ('OCT_EC1000_relpath', OCT_EC1000_relpath)):
                file_path = path.join(path.dirname(fileset_dict['raw_OCT_path']), val)
                file_name = FileManager.find_file_with_extension(file_path, extension_dict[var])
                if 'relpath' in var:
                    var = var.replace('relpath', 'path')
                    fileset_dict[var] = file_name
                    # path.abspath(path.join(path.dirname(file), va))
                else:
                    fileset_dict[var] = path.abspath(val)
            # filename = path.basename(fileset_dict['raw_OCT_parameters_path'])
            fileset_dict['mod_OCT_parameters_path'] = path.join(path.dirname(fileset_dict['raw_OCT_path']), mod_OCT_parameters_relpath)
            # filename = path.basename('cut_data.bin')
            fileset_dict['mod_OCT_path'] = path.join(path.dirname(fileset_dict['raw_OCT_path']), mod_OCT_relpath)
            fileset_dict['blank_A_path'] = blank_A_path

            # copy dir if necessary for mod_OCT_parameters file
            mod_param_file = fileset_dict['mod_OCT_parameters_path']
            mod_dir = path.dirname(mod_param_file)
            if not os.path.exists(mod_dir):
                os.makedirs(mod_dir)
            # copy mod_OCT_parameters file
            shutil.copyfile(fileset_dict['raw_OCT_parameters_path'], mod_param_file)

        return fileset_list


    def find_all_with_filename(self, directory: str, filenames: Union[List[str], str], exclude_folder_list: Union[List[str], str] = []) -> List[str]:
        """This method recursively searches a directory for every instance with one of a set of filenames.  It then returns a list of paths to each of these files.

        Args:
            directory: directory to be search for each instance of a specific filename
            filenames:  filename to be searched for
            exclude_folder_list: a list of folder names to be excluded from the search

        Returns:
            path_list: list of paths to each file with filename
        """
        path_list = []
        if isinstance(filenames, str):
            filenames = [filenames]
        if isinstance(exclude_folder_list, str):
            exclude_folder_list = [exclude_folder_list]

        for root, dirs, files in os.walk(directory):
            if path.basename(root) not in exclude_folder_list:
                for file in files:
                    if file in filenames:
                        full_path = path.join(root, file)
                        path_list.append(full_path)
        return path_list

    def copy_files_to_rel_loc_of_filename(self, path_of_files_to_copy: Union[str, List[str]], relative_location_to_put_files: str = './', search_directory: str = '', search_for_filenames: Union[List[str], str] = ''):
        """This recursively searches a directory for each file with a specified filename, then copies a specified file(s) to a relative location of each instance of the filename.

        Args:
            path_of_files_to_copy:
            relative_location_to_put_files:
            search_directory:
            search_for_filename:

        Returns:
            num_copies: a dictionary with the key being the filename and the value being the number of copies of that file made
        """
        num_copies = defaultdict(int)
        if isinstance(path_of_files_to_copy, str):
            path_of_files_to_copy = [path_of_files_to_copy]

        path_list = self.find_all_with_filename(search_directory, search_for_filenames)
        for copy_filepath in path_of_files_to_copy:
            assert path.isfile(copy_filepath), "{} does not exist.".format(copy_filepath)
            for path_var in path_list:
                copy_filename = path.basename(copy_filepath)
                path_var = path.join(path.dirname(path_var), relative_location_to_put_files, copy_filename)
                if path.abspath(copy_filepath) != path.abspath(path_var):
                    shutil.copy(copy_filepath, path_var)
                    num_copies[copy_filepath] += 1
        return num_copies

    @staticmethod
    def find_file_with_extension(dir, ext):
        file_list = []
        for file in os.listdir(dir):
            if file.endswith(ext):
                file_path = path.join(dir, file)
                file_list.append(file_path)
        if len(file_list) == 0:
            raise Exception('No files with {} extension were found in {}'.format(ext, dir))
        if len(file_list) == 1:
            return file_list[0]
        else:
            raise Exception('Multiple files with {} extension were found in {}'.format(ext, dir))

    @staticmethod
    def write_to_config_file(file_path, sp, key, value, heading='SCAN_SETTINGS'):
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = str
        config_parser.read(file_path)
        sp[key] = value
        config_parser[heading][key] = str(value)
        with open(file_path, 'w') as configfile:
            config_parser.write(configfile)

    def __init__(self) -> None:
        pass
