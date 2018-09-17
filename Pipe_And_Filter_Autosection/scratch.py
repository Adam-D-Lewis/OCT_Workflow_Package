from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData
from Pipe_And_Filter_Autosection.classes.FileManager import FileManager
import matplotlib.pyplot as plt

# fm = FileManager()
# filepaths = [r'Z:\Adam\OCT ARL Tensile Bars\oct scan ec1000 files\full_build_area.xml', r'Z:\Adam\OCT ARL Tensile Bars\oct config files\full_build_area.oct_config']
# search_dir = r'Z:\Adam\OCT ARL Tensile Bars\Logs'
# fm.copy_files_to_rel_loc_of_filename(filepaths, '../', search_dir, 'data.bin')


filename = ['galvo X Scan.2d_dbl', 'galvo Y Scan.2d_dbl']
for file in filename:
    file_path = r'D:\9_13_2018 Laser Ring Exploration\LOG Galvo\\' + file
    gd = GalvoData(file_path)
    plt.figure()
    plt.title(file)
    plt.plot(gd.volt_to_mm(gd.x_data, 'x'))
    plt.figure()
    plt.title(file)
    plt.plot(gd.volt_to_mm(gd.y_data, 'y'))

plt.show()