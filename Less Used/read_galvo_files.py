import numpy as np
def read_galvo_files(filename, num_channels, segSize):
    data = np.fromfile(filename, dtype='>d')
    if np.size(data) % (num_channels*segSize) == 0:
        numIter = int(np.size(data)/segSize)
        channels = [[] for _ in np.arange(num_channels)]
        for i in range(numIter):
            for j in range(num_channels):
                channels[j] = np.append(channels[j], data[(num_channels*i+j)*segSize:(num_channels*i+j+1)*segSize])
        return channels
    else:
        raise ValueError('The filesize isn\'t divisible by ' + str(num_channels*segSize))