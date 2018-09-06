from fit_to_polynomial import return_offset_values
import sys, os
import tempfile

height = sys.argv[1]
galvo_data = sys.argv[2]
oct_sc_cfg = sys.argv[3]

#  send results to standard output
results = return_offset_values(height, galvo_data, oct_sc_cfg)

#  save the results to a temporary file
results_file = tempfile.TemporaryFile('w', encoding='ascii')
results_file.write(str(height))

#  send the results file location to the standard out
print(results_file.name)
