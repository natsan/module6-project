# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        script8
# Purpose:
#
# Author:      Nataliya
#
# Created:     29.10.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import stderr
from os import listdir
from math import sqrt
from .tools import find_nearest_num, cut_column, join_columns, get_head_nums,\
cut_data, read_file, get_heads, is_existed, is_number
from .tools import write_data as write
#-------------------------------------------------------------------------------

def prepare_data(voltage, names):
    """ to prepare data for calculating """
    # define path of file
    directory = '.'
    file_list = listdir(directory);

    voltages = []
    # get list of files with needed voltages
    for f in file_list:
        if (f[0:2] == 'm.') and (is_number(f[2:-2])):
            voltages.append(float(f[2:-2]))
    if len(voltages) == 0:
        stderr.write('Error: required files m*.d are not found\n')
        return None
    voltages.sort()
    print(voltages)
    nearest_num = find_nearest_num(voltages, voltage)
    # if nearest_num is an integer, then it needs to remove '.0'
    str_num = str(nearest_num)
    split_num = str_num.split('.')
    if split_num[1] == '0':
        str_num = split_num[0]

    table = read_file('m.' + str_num + '.d')
    if not is_existed(table):
        stderr.write('Error: data is incorrect\n')
        return None, None
    # get heads from file
    heads = get_heads(table[0])
    del table[0]
    # get numbers of cut columns
    cut_columns = get_head_nums(heads, names)
    data =  cut_data(table, cut_columns)

    # reshape data to delete last lines from table
    temp_data = join_columns(data)

    # delete last lines
    if len(cut_columns) == 7:
        temp_data = temp_data[:-2]
    elif len(cut_columns) == 10:
        temp_data = temp_data[:-4]
    elif len(cut_columns) == 13:
        temp_data = temp_data[:-8]
    else:
        stderr.write('Error: File is incorrect\n')
        return None, None

    data = join_columns(temp_data)
    print(__name__ + ": data is prepared")
    return nearest_num, data

#-------------------------------------------------------------------------------
def calc(cols):
    """ to calculate current vector J"""

    print(__name__ + ": calculating...")
    if not is_existed(cols):
        stderr.write("Data is incorrect\n")
        return None
    data = []
    dimension = None
    if len(cols) == 13:
        data = three_dimensional(cols)
        dimension = 3
    elif len(cols) == 10:
        data = two_dimensional(cols)
        dimension = 2
    elif len(cols) == 7:
        data = one_dimensional(cols)
        dimension = 1
    else:
        stderr.write('Error: data is incorrect')
        return None

    return dimension, data
#-------------------------------------------------------------------------------

def one_dimensional(cols):
    """to prepare tables for one-dimensional case """
    # table consists of x - col[0], Jnx - [1], Jny - cols[2], n - cols[3],
    # p - cols[4], S - cols[5], T - cols[6]
    xJnJp = join_columns([cols[0], cols[1], cols[2], addition(cols[1], cols[2])])
    xnp = join_columns([cols[0], cols[3], cols[4]])
    xST = join_columns([cols[0], cols[5], cols[6]])
    return [xJnJp, xnp, xST]

#-------------------------------------------------------------------------------

def two_dimensional(cols):
    """to prepare tables for two-dimensional case """
    # table consists of x - cols[0], y - cols[1], Jnx - cols[2], Jny - cols[3],
    # Jpx - cols[4], Jpy - cols[5], Jx = Jnx + Jpx, Jy = Jny + Jpy
    xyJnJp = join_columns([ cols[0], cols[1], cols[2], cols[3], cols[4],\
     cols[5], addition(cols[2], cols[4]), addition(cols[3], cols[5]) ])
    # table consists of x - cols[0], y - cols[1], n - cols[6], p - cols[7]
    xyznp = join_columns([cols[0], cols[1], cols[6], cols[7]])
    # table consists of x - cols[0], y - cols[1], S - cols[8], T - cols[9]
    xyzST = join_columns([ cols[0], cols[1], cols[8], cols[9] ])
    return [xyzJnJp, xyznp, xyzST]
#-------------------------------------------------------------------------------

def three_dimensional(cols):
    """to prepare tables for three-dimensional case """
    # table consists of x - cols[0], y - cols[1], z - cols[2], Jnx - cols[3],
    # Jny - cols[4], Jnz - cols[5], Jpx - cols[6], Jpy - cols[7], Jpz - cols[8],
    # Jx = Jnx + Jpx, Jy = Jny + Jpy, Jz = Jnz + Jpz
    xyzJnJp = join_columns([ cols[0], cols[1], cols[2], cols[3], cols[4],\
     cols[5], cols[6], cols[7], cols[8], addition(cols[3], cols[6]),\
     addition(cols[4], cols[7]), addition(cols[5], cols[8]) ])
    # table consists of x - cols[0], y - cols[1], z - cols[2], n - cols[9],
    #p - cols[10]
    xyznp = join_columns([cols[0], cols[1], cols[2], cols[9], cols[10]])
    # table consists of x - cols[0], y - cols[1], z - cols[2], S - cols[11],
    # T - cols[12]
    xyzST = join_columns([ cols[0], cols[1], cols[2], cols[11], cols[12] ])
    return [xyzJnJp, xyznp, xyzST]
#-------------------------------------------------------------------------------

def addition(a, b):
    """ addition a + b """
    if len(a) != len(b):
        return None
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i])
    return c
#-------------------------------------------------------------------------------

def write_data(path, data_name, voltage, data):
    """ To convert data to string and to write them in files """
    return write(path, data_name, voltage, data)
#-------------------------------------------------------------------------------

def main():
##    full_table = prepare_data(0.25)
####    print(full_table[0])
##    data = calc(full_table[1])
##    write_data('xJnJp', '# 1-x\t2-Jnx\t3-Jpx\t4-Jx\n', 'voltage ', data[1])
##    col1 = [1, 2, 3, 4]
##    col2 = [5, 6, 7, 8]
##    res = join_columns([col1, col2])
##    print(res)

    tt = [1, 2, 3, 4]
    tt = tt[:-2]
    print(tt)

if __name__ == '__main__':
    main()
