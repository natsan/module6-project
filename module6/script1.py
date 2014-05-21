# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        script1
# Purpose:
#
# Author:      Nataliya
#
# Created:     20.09.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import stderr
from .tools import prepare_data as prepare
from .tools import write_data as write
from .tools import element_multiply, join_columns, is_existed
from math import sin, cos, radians

def prepare_data(path, wavelength, names):
    """ to prepare data for calculation:
        path - 'far.d'
    """
    found_wavelength, table = prepare(path, wavelength, names)
    if not is_existed(table):
        return None, None
    print(__name__ + ": data is prepared")
    return found_wavelength, table
#-------------------------------------------------------------------------------

def calc(table):
    """ to calculate I(x, y)
        x = sin(teta)*cos(phi)
        y = sin(teta)*sin(phi)

        P_norm = P_norm*distance^2

        initial data (table):
        table[0] - theta
        table[1] - phi
        table[2] - P_norm

        if far.d contain 'f':
            table[3] - r

        output data (new_table):
        x - column 0
        y - column 1
        P_norm - column 2
    """
    print(__name__ + ": calculating...")
    if not is_existed(table):
        stderr.write("Data is incorrect\n")
        return None

    sin_theta = []
    cos_phi = []
    sin_phi = []
    intensity = []
    for i in range(len(table[0])):
        sin_theta.append(sin(radians(table[0][i])))
        cos_phi.append(cos(radians(table[1][i])))
        sin_phi.append(sin(radians(table[1][i])))

    x = element_multiply(sin_theta, cos_phi)
    y = element_multiply(sin_theta, sin_phi)

    # if there is f in 'far.d' it needs multiplying on r^2
    if len(table) == 4:
        intensity = element_multiply(table[2], table[3])
        intensity = element_multiply(intensity, table[3])
    elif len(table) == 3:
        intensity = table[2]
    else:
        stderr.write('Error: data is incorrect\n')
        return None
##    data = join_columns([x, y, intensity])
    return [x, y, intensity]
#-------------------------------------------------------------------------------

def write_data(path, data_name, header, data):
    """ To convert data to string and to write them in file """
    write(path, data_name, header, data)

#-------------------------------------------------------------------------------

def main():
    table = prepare_data('far.d', 1.42, [0, 3 - 1, 4 - 1, 11 - 1])
    data = calc(table)
    write_data('output','# 1-theta\t2-phi\t3-P_norm\n', 1.42, data)

if __name__ == '__main__':
    main()
