import numpy as np
from j_to_py import j_array_to_np_array as j2np
import scipy as sp
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import ndimage
import tempfile
import os
from mpl_toolkits.mplot3d import Axes3D

class HeightData:
    """

    Args:

    NTodo:
        Make a method to return all the datasets that have already been cut
    """

    def __init__(self, j_arr_str_path=None, mmPerPixel=7.81/1000):
        self.mmPerPixel = mmPerPixel
        if j_arr_str_path:
            self.height_mm = self.read_height_data(j_arr_str_path)
        self.fit_coeff = None
        self.height_fit_mm = None
        self.error = None
        self.Z_rel_offset_pixels = None

    def polyfit_height_data(self, sectioned_x_galvo, sectioned_y_galvo, poly_order=2):
        # #  example numbers
        # sectioned_x_galvo = np.arange(3,5)
        # sectioned_y_galvo = np.arange(1,3)
        # poly_order = 3

        # make matrices of increasing powers
        sectioned_x_galvo = sectioned_x_galvo.flatten()
        sectioned_y_galvo = sectioned_y_galvo.flatten()
        x_mat = np.empty((sectioned_x_galvo.size, poly_order))
        y_mat = np.empty((sectioned_y_galvo.size, poly_order))
        for n in range(poly_order):
            x_mat[:, n] = sectioned_x_galvo**n
            y_mat[:, n] = sectioned_y_galvo**n
        A = np.empty((sectioned_x_galvo.size, poly_order**2+2))
        for y_ind, y_col in enumerate(y_mat.transpose()):
            A[:, y_ind*poly_order:(y_ind+1)*poly_order] = (x_mat.transpose()*y_col).transpose()
        A[:, -2] = sectioned_x_galvo**poly_order
        A[:, -1] = sectioned_y_galvo ** poly_order
        C, _, _, _ = sp.linalg.lstsq(A, self.height_mm.flatten())
        self.fit_coeff = C
        self.height_fit_mm = np.dot(A, C).reshape(np.shape(self.height_mm))
        return self.height_fit_mm

    def geomfit_height_data(self, sectioned_x_galvo_mm, sectioned_y_galvo_mm):
        XY, Z = self._prepare_vars_for_fit_to_poly(self.height_mm, sectioned_x_galvo_mm, sectioned_y_galvo_mm)

        # fit to the polynomial
        z_ref = 520 # mm (35in = 889 mm)
        z_c = z_ref + 0.55  # mm
        h = -1.92  # mm (x offset)
        k = -10.697  # mm (y offset)
        p0 = [z_ref, z_c, h, k]
        bnds = np.vstack(([z_ref*0.7, z_c*0.7, h-2, k-5], [z_ref*1.3, z_c*1.3, h+2, k+5]))

        popt, pcov = opt.curve_fit(self._z_func, XY, Z, p0, bounds=bnds)
        z_ref, z_c, h, k = popt
        self.C = popt
        self.height_fit_mm = self._z_func(XY, z_ref, z_c, h, k).reshape(np.shape(self.height_mm))
        return self.height_fit_mm

        # # write the parameters to file
        # oct_sc.write_to_file('z_ref', z_ref, 'HEIGHT_CORRECTION')
        # oct_sc.write_to_file('z_c', z_c, 'HEIGHT_CORRECTION')
        # oct_sc.write_to_file('h', h, 'HEIGHT_CORRECTION')
        # oct_sc.write_to_file('k', k, 'HEIGHT_CORRECTION')

    def _z_func(self, XY, z_ref, z_c, h, k):
        """
        >>> print('hi')
        hi
        """
        X = XY[:, 0]
        Y = XY[:, 1]
        Z = np.sqrt(z_c ** 2 + (X - h) ** 2 + (Y - k) ** 2) - z_ref
        return Z

    def _prepare_vars_for_fit_to_poly(self, height, sec_x_gd, sec_y_gd):
        """

        Args:
            height: 2D numpy array
            sec_x_gd:
            sec_y_gd:

        Returns:

        """
        X, Y = sec_x_gd, sec_y_gd
        XY = np.vstack((X.flatten(), Y.flatten())).transpose()
        Z = height.flatten()
        return XY, Z

    def plot_height(self, x_galvo, y_galvo, plot_fit=False, plot_error=False):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        x_galvo = x_galvo
        y_galvo = y_galvo
        ax.plot_surface(x_galvo, y_galvo, self.height_mm, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        if plot_fit:
            self.plot_height_fit(x_galvo, y_galvo, plot_error, show=False)

        plt.show()

    def plot_height_fit(self, x_galvo, y_galvo, plot_error=True, show=True):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(x_galvo, y_galvo, self.height_fit_mm, cmap=cm.coolwarm, linewidth=0, antialiased=False)

        if plot_error:
            self.error = self.height_mm - self.height_fit_mm
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot_surface(x_galvo, y_galvo, self.error, cmap=cm.coolwarm, linewidth=0, antialiased=False)
            plt.title('ave |error| = {}'.format(round(np.mean(abs(self.error)), 3)))
        if show:
            plt.show()
            print('bye')


    def read_height_data(self, j_arr_str_path):
        with open(j_arr_str_path, 'r') as f:
            j_arr_str = f.read()
        height_mm = j2np(j_arr_str) * self.mmPerPixel  # mm
        return height_mm


    def filter_height_data(self, kernal_size=3):
        """applies a median filter to the height data

        Args:
            kernal_size: length of the kernal (number of pixels in kernal is kernal_length**2)

        Returns:

        """
        height_mm = ndimage.median_filter(self.height_mm, size=kernal_size)
        self.height_mm = height_mm

    def calc_rel_offset(self, use_height_data=False):
        if use_height_data:
            Z_rel_offset_mm = self.height_mm - np.min(self.height_mm)
        else:
            Z_rel_offset_mm = self.height_fit_mm - np.min(self.height_fit_mm)

        self.Z_rel_offset_pixels = np.round(Z_rel_offset_mm/self.mmPerPixel)  # pixels
        return self.Z_rel_offset_pixels

    def write_rel_offset_to_file(self):
        Z_rel_offset_pixels_arrstr = np.char.mod('%i', self.Z_rel_offset_pixels).flatten()
        Z_rel_offset_pixels_str = ",".join(Z_rel_offset_pixels_arrstr)

        new_file, filename = tempfile.mkstemp()
        os.write(new_file, bytearray(Z_rel_offset_pixels_str, encoding='ascii'))
        print(filename)
