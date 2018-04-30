import numpy as np
def readGalvoFiles(filename):
    segSize = 50000
    data = np.fromfile(filename, dtype='>d')
    if np.size(data) % (segSize) == 0:
        numIter = int(np.size(data)/segSize)
        xGalvo, yGalvo = [], []
        for i in range(numIter):
            xGalvo = np.append(xGalvo, data[3*i*segSize:(3*i+1)*segSize])
            yGalvo = np.append(yGalvo, data[(3*i+1)*segSize:(3*i+2)*segSize])
        return [xGalvo, yGalvo]
    else:
        pass
        # raise ValueError('The filename size isnt divisible by ' + str(2*segSize))