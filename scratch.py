import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
from readGalvoFiles import readGalvoFiles
#%matplotlib notebook

import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt
import matplotlib.pyplot as plt


[xGalvo, yGalvo] = readGalvoFiles(r'C:\Users\LAMPS_SLS\Documents\Builds\Adam\Galvo Signal\motors_off\100.glv')
# [xGalvo, yGalvo] = readGalvoFiles(r'C:\Users\adl628\Box Sync\Academics & Work\Research\Experiments\AutoCutOCT\Galvo Position Signals\motors_on\10.glv')

plt.figure()
plt.plot(yGalvo)

plt.figure()
plt.plot(xGalvo)
plt.title('xGalvo')
plt.show()


print('bye')
