from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData
from Pipe_And_Filter_Autosection.classes.FileManager import FileManager
import matplotlib.pyplot as plt

fm = FileManager()
filepaths = [r'Z:\Adam\OCT ARL Tensile Bars\oct scan ec1000 files\full_build_area.xml', r'Z:\Adam\OCT ARL Tensile Bars\oct config files\full_build_area.oct_config']
search_dir = r'Z:\Adam\OCT ARL Tensile Bars\Logs'
fm.copy_files_to_rel_loc_of_filename(filepaths, '../', search_dir, 'data.bin')
