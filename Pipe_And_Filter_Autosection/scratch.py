from Pipe_And_Filter_Autosection.classes.GalvoData import GalvoData as GD
from Pipe_And_Filter_Autosection.classes.FileManager import FileManager as FM
from Pipe_And_Filter_Autosection.classes.ModOCTParameters import ModOCTParameters
from os import path
#testdir
testdir = path.abspath(r'C:\Users\adl628\Desktop\test')
mod_param_file = path.join(testdir, r'parameters.oct_scan')

fm = FM()
mod_OCT_parameters = ModOCTParameters(mod_param_file)

print_heading = 'B-Scans'.lower()
heading_val = mod_OCT_parameters.sp[print_heading]
mod_OCT_parameters.sp[print_heading] = mod_OCT_parameters.sp[print_heading] + 1
print(print_heading + ' is {} before modification'.format(heading_val))
mod_OCT_parameters.write_to_file(print_heading, heading_val+1)
print(print_heading + ' is {} after modification'.format(mod_OCT_parameters.sp[print_heading]))


