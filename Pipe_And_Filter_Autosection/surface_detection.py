from fit_to_polynomial import return_offset_values
import sys, os
import tempfile

sys.argv = [0, r'C:\Users\adl628\AppData\Local\Temp\height2064797635151627302.tmp', r'Z:\Adam Lewis\2018_09_07_Nylon12\Logs\45%\179\MessUpNonsymmetric\Layer 0\galvo_post.2d_dbl', r'Z:\Adam Lewis\2018_09_07_Nylon12\Logs\45%\179\MessUpNonsymmetric\Layer 0\scan_param.oct_config', '1']

height = sys.argv[1]
galvo_data = sys.argv[2]
oct_sc_cfg = sys.argv[3]
save = sys.argv[4]

#  send results to standard output
results_path = return_offset_values(height, galvo_data, oct_sc_cfg, save)

#  save the results to a temporary file
# results_file = tempfile.TemporaryFile('w', encoding='ascii')
# results_file.write(str(height))

#  send the results file location to the standard out
print(results_path)
