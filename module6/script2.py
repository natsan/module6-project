# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        script2
# Purpose:
#
# Author:      Nataliya
#
# Created:     20.09.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from .tools import prepare_data as prepare
from .tools import write_data as write
from .tools import to_string, cut_column, remove_duplicates, cut_table, \
rectangle_fun, join_columns, element_multiply, is_existed

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
    """ to calculate intensity of the formula:
        I(theta) = Sum(  (I(i) + I(i+1)) * (phi(i+1) - phi(i))  )/2
        I(theta) = I(theta)*distance^2

        initial data:
            theta - table[0]
            phi - table[1]
            intensity - talbe[2]
            if 'far.d' contains 'f'
                r - table[3]
    """
    print(__name__ + ": calculating...")
    if not is_existed(table):
        stderr.write("Data is incorrect\n")
        return None

    str_table = to_string(join_columns(table))
##    print(len(str_table))
    # get theta and remove duplicates
    set_column = table[0]
##    print(len(set_column))
    dct, col = remove_duplicates(set_column)
    iteta = []
##    distance = cut_column(table, 0)
    dist_index_list = []
    theta_list = []
    intensity = []
    for i in range(len(col)):
        theta = col[i]
        theta_index = dct[theta]
        temp_table = cut_table(str_table, [0, 1, 2], theta_index, theta)
        dist_index_list.append(theta_index)
        col_x = cut_column(temp_table, 0)
        col_f = cut_column(temp_table, 1)
        intensity.append(rectangle_fun(col_f, col_x))
        theta_list.append(theta)

    if len(table) == 4:
        r = table[3]
        distance = []
        for i in range(len(dist_index_list)):
            distance.append(r[dist_index_list[i]])
        intensity = element_multiply(intensity, distance)
        intensity = element_multiply(intensity, distance)

    return join_columns([theta_list, intensity])

#-------------------------------------------------------------------------------

def write_data(path, data_name, header, data):
    """ To convert data to string and to write them in file """
    return write(path, data_name, header, data)
#-------------------------------------------------------------------------------

def main():
    table = prepare_data('far.d', 1.42, [0, 3 - 1, 4 - 1, 11 - 1])
##    print(table)
    data = calc(table)
    write_data('rectangles', '# 1-teta\t2-I_teta\n', 1.42, data)

if __name__ == '__main__':
    main()
