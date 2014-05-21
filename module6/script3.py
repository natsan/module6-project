# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        script3
# Purpose:
#
# Author:      Nataliya
#
# Created:     25.09.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from .tools import prepare_data as prepare
from .tools import write_data as write
from .tools import cut_column, find_nearest_num, remove_duplicates,\
element_multiply, join_columns, is_existed

#-------------------------------------------------------------------------------
def prepare_data(path, wavelength, azimuth_angle, names):
    """ to prepare data
        path - 'far.d'
        table[0] - theta
        table[1] - phi
        table[2] - P_norm
        if 'far.d' contains r
            table[3] - r
            P_norm = P_norm*r^2
    """
    found_wavelen, table = prepare(path, wavelength, names)
    if not is_existed(table):
        return None, None, None

    theta_col = table[0]
    phi_col = table[1]
    dct, phi = remove_duplicates(phi_col)
    desired_angle = find_nearest_num(phi, azimuth_angle)
    new_theta = []
    intensity = []
    dist_index_list = []
    for i in range(len(table[0])):
        if phi_col[i] == desired_angle:
            new_theta.append(theta_col[i])
            intensity.append(table[2][i])
            dist_index_list.append(i)

    # if 'far.d' contains column of 'r', intensity = intensity*r^2
    if len(table) == 4:
        distance = []
        r = table[3]
        for i in range(len(dist_index_list)):
            distance.append(r[dist_index_list[i]])
        intensity = element_multiply(intensity, distance)
        intensity = element_multiply(intensity, distance)
    print(__name__ + ": data is prepared")
    return found_wavelen, desired_angle, join_columns([new_theta, intensity])
#-------------------------------------------------------------------------------

def calc():
    pass
#-------------------------------------------------------------------------------

def write_data(path, data_name, header, data):
    """ To convert data to string and to write them in file """
    return write(path, data_name, header, data)
#-------------------------------------------------------------------------------

def main():
    table = prepare_data('far.d', 1.42, 0, [0, 3 - 1, 4 - 1, 11 - 1])
    print(table)

if __name__ == '__main__':
    main()
