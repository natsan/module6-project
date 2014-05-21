# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        script4
# Purpose:
#
# Author:      Nataliya
#
# Created:     25.09.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import stderr
from math import sin, radians
from .tools import write_data as write
from .tools import to_string, cut_column, remove_duplicates, cut_table, \
read_file, rectangle_fun, double_integral, element_multiply, join_columns,\
get_heads, get_head_nums, is_existed
from os.path import exists
#-------------------------------------------------------------------------------
def prepare_data(cone_angle, path = ['spectra.d', 'far.d', 'power.d'], names = None):
    """ to prepare data for calculation
        path[0] - 'spectra.d'
        path[1] - 'far.d'
        path[2] - 'power.d'
    """
    i_up = None
    i_g = None
    far_table = None
    distance = None
    # get Ig
    # read file 'power.d'
    p_table = read_file(path[2])
    if not is_existed(p_table):
        stderr.write("Error: file " + path[2] + " is not found\n")
        return None
    del p_table[0] # delete heads
    f = cut_column(p_table, 0) # f = 1/wavelength
    i_g = cut_column(p_table, 1)

    # get Iup or cut table from 'far.d'
    if cone_angle == 90 and exists(path[0]):
        # read file "spectra.d"
        table = read_file(path[0])
        del table[0] # delete heads
        i_up = cut_column(table, 1)

    else:
        if names == None or exists(path[1]) == False:
            stderr.write("Error: data is incorrect or file " + path[1] +\
            " is not found\n")
            return None
        else:
            # read file "far.d"
            table = read_file(path[1])
            heads = get_heads(table[0])
            cut_columns = get_head_nums(heads, names)
            del table[0] # delete heads
            # get wavelength
            column = cut_column(table,cut_columns[0])
            # return [dictionary[value, index], list without duplicates]
            dct, col = remove_duplicates(column)
            # dct - dictionary
            # col - ordered list without duplicates

            r = None
            # if 'far.d' contains column of 'r'
            if heads[0] == 'f':
                r = cut_column(table, cut_columns[-1])

            far_table = []
            if r != None:
                del cut_columns[-1]
                distance = []

            for i in range(len(col)):
                value = col[i]
                index = dct[value]
                temp_table = cut_table(table, cut_columns, index, value)
                if r != None:
                    distance.append(r[dct[value]])
                far_table.append(temp_table)

    print(__name__ + ": data is prepared")

    return [i_g, i_up, f, far_table, distance, heads[0]]
#-------------------------------------------------------------------------------

def calc(cone_angle, table):
    """ to calculate list of efficiency:
        if cone_angle == 90 and file 'spectra.d' exists
            efficiency = i_up/i_g
        else:
            for i in theta:
            for j in phi:
            i_up += (  ( (P_norm(i,j) + P_norm(i, j+1))*sin(theta(i)) +
            (P_norm(i+1, j) + P_norm(i+1, j+1))*sin(theta(i+1)) )
            *( theta(i+1) - theta(i)*(phi(j+1) - phi(j)/4

            efficiency = i_up/i_g

            if 'far.d' contains column of 'r' and 'f'
                wav = 1/f
                efficiency = efficiency*r^2

    """
    print(__name__ + ": calculating...")
    if not is_existed(table):
        stderr.write("Data is incorrect\n")
        return None
    i_g = table[0]

    i_up = table[1]
    f = table[2]
    far_table = table[3]
    distance = None
    # if 'far.d' contains column of 'r'
    if table[4] != None:
        distance = table[4]

    nu = [] # efficiency

    if i_up == None:
        i_up = []
        for i in range(len(far_table)):
            i_up.append(double_integral(far_table[i], cone_angle))

    # calculate efficiency
    for i in range(len(f)):
        nu.append(i_up[i]/i_g[i])

    if distance != None:
        # multiply nu*distance^2
        nu = element_multiply(nu, distance)
        nu = element_multiply(nu, distance)

    # wavelength or frequency?
    # if it is frequency, wavelength = 1/frequency
    wav = []
    if table[5] == 'f':
        for n in f:
            wav.append(1/n)
    elif table[5] =='wavelength':
        wav = f
    return join_columns([wav, nu])

#-------------------------------------------------------------------------------

def write_data(path, data_name, header, data):
    """ To convert data to string and to write them in file """
    write(path, data_name, header, data)
#-------------------------------------------------------------------------------

def main():
    # test prepare_data:
    path = ['spectra.d', 'far.d', 'power.d']
    table = prepare_data(90, path, [0, 3 - 1, 4 - 1, 11 - 1])
    write('test','# 1-theta\t2-phi\t3-P_norm\n',
             1/1.42, table[3][0])
##    print(len(table[3][0]))
    res = calc_Iup(table[3][0], 90)
    print(res)
##    res = calc(20, table)
##    write_data('efficiently', '#1-wavelength\t2-efficiency\n', None, res)

if __name__ == '__main__':
    main()
