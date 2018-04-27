import numpy as np
def readGalvoFiles(filename):
    segSize = 50000
    data = np.fromfile(filename, dtype='>d')
    if np.size(data) % (2*segSize) == 0:
        numIter = int(np.size(data)/segSize)
        xGalvo, yGalvo = [], []
        for i in range(numIter):
            xGalvo = np.append(xGalvo, data[2*i*segSize:(2*i+1)*segSize])
            yGalvo = np.append(yGalvo, data[(2*i+1)*segSize:(2*i+2)*segSize])
        return [xGalvo, yGalvo]
    else:
        raise ValueError('The filename size isnt divisible by ' + str(2*segSize))