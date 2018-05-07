import time
import socket
import struct
import numpy as np
from skimage.color import rgb2gray


def send_to_imagej(img, address, title='Image'):
    """Pack and send images to ImageJ, along with a title
    """
    max_ = img.max()

    if img.dtype.kind == 'f':
        if max_ <= 1:
            img *= 2**16 - 1
            max_ *= 2**16 - 1

    if max_ <= 255:
        img = img.astype(np.int16)
        img -= 127
        img = img.astype(np.int8)
        dtype = b'b'

    else:
        # check for 12 bit - looking images (or just improve contrast)
        if max_ <= 2**12:
            img *= 2**4
        img = img.astype(np.int32)
        img -= 2 ** 15 - 1
        img = img.astype(np.int16)
        img += np.random.randint(-1000, 1000)
        dtype = b'h'

    img = rgb2gray(img)

    data = struct.pack('>ccHH100s',
                       b'1', dtype, img.shape[0], img.shape[1],
                        title.encode('utf-8'))
    send_over_socket(address, data + img.tobytes())


def send_over_socket(address, data):
    if isinstance(address, (tuple, list)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        sock.connect(address)
    except socket.error:
        time.sleep(0.1)
        try:
            sock.connect(address)
        except socket.error as e:
            raise socket.error('Could not open "%s": %s' % (address, e))

    try:
        sock.sendall(data)
    finally:
        sock.close()


if __name__ == '__main__':
    from skimage import data, img_as_float, img_as_uint
    image = 255*np.ones((50,50))

    moon = img_as_uint(data.camera())

    send_to_imagej(image, ('', 5048), 'My Very Very Special Image')
