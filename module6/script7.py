# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        script7
# Purpose:
#
# Author:      Nataliya
#
# Created:     04.10.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from .tools import read_file, cut_column, find_nearest_num, write_file,\
linear_interpolation, element_multiply, is_existed
from sys import stderr
from os.path import exists
from math import fabs
#-------------------------------------------------------------------------------

def prepare_data(path_jsc = 'j_sc.d', path_j = 'j.d'):
    """ to prepare data for calculation
        path_jsc - 'j-sc.d' - solar cell
        path_j - 'j.d' - OLED
    """

    jsc_table = None
    j_table = None
    if exists(path_jsc):
        jsc_table = read_file(path_jsc)
##        print('Prepare jsc table ' + str(jsc_table))
        if is_existed(jsc_table):
            del jsc_table[0] # delete heads
    if exists(path_j):
        j_table = read_file(path_j)
        if is_existed(j_table):
            del j_table[0] # delete heads
    if (not is_existed(jsc_table)) and (not is_existed(j_table)):
        stderr.write("Error: files " + path_j + ' and ' + path_jsc + " is not found\n")
        return None, None
    print(__name__ + ": data is prepared")
    return jsc_table, j_table
#-------------------------------------------------------------------------------

def calc(jsc_table):
    """ to calculate:
        1. Short circuit current
        2. Open circuit voltage
        3. The point of maximum power
        4. Filling factor
    """
    print(__name__ + ": calculating...")
##    print("JSC Table: " + str(jsc_table))
    if not is_existed(jsc_table):
        stderr.write("Data is incorrect\n")
        return None

    voltage = cut_column(jsc_table, 0)
    current = cut_column(jsc_table, 1)
    short_circuit_current = None
    open_circuit_voltage = None
    max_power_point = None
    filling_factor = None
    # find short circuit current
    if min(voltage) == 0:
         short_circuit_current = current[voltage.index(0)]
    else:
        if min(voltage) < 0:
            prep_data = fit_data(current, voltage, 0)
            short_circuit_current = linear_interpolation(prep_data)
        else:
            stderr.write("Error: Voltage-current characteristic is not valid for a solar cell")
    #find open circuit voltage
    if is_correct_data(current):
        last = sign(current[-1])
        prev = sign(current[-2])
        if last  != 0 and prev != 0:
            open_circuit_voltage = linear_interpolation([current[-1], current[-2], voltage[-1], voltage[-2], 0])
        elif last == prev == 0:
            stderr.write("Error: Voltage-current characteristic is not valid for a solar cell")
    else:
        stderr.write("Error: Voltage-current characteristic is not valid for a solar cell")

    #find the point of maximum power
    power = element_multiply(current, voltage)
    max_power = max(power)
    max_power_point = voltage[power.index(max_power)]
    #find filling factor
    if short_circuit_current != 0 and open_circuit_voltage != 0 and\
    short_circuit_current != None and open_circuit_voltage != None:
        filling_factor = max_power/(short_circuit_current*open_circuit_voltage)

    return [short_circuit_current, open_circuit_voltage, max_power_point,
            filling_factor]
#-------------------------------------------------------------------------------

def is_correct_data(col):
    """ To check whether the data is decreasing
        and to test sign changing in the last two values
    """
    b = False
    index = 0
    for i in range(len(col)-2):
        if (fabs(col[i]) - fabs(col[i+1]))<0:
##            print('Decreasing is failure. False')
            return False
    if sign(col[-1]) != sign(col[-2]) != 0:
##        print('Different sings. True')
        return True
    elif sign(col[-1]) == sign(col[-2]) != 0:
        if fabs(col[-1]) < fabs(col[-2]):
##            print('Same sings, decreasing. True')
            return True
        else:
##            print('Same sings, increasing. False')
            return False
    return False
#-------------------------------------------------------------------------------

def sign(x):
    """ get sign of set value"""
    if x==0.0:
        return 0.0
    elif x > 0.0:
        return 1.0
    else:
        return -1.0
#-------------------------------------------------------------------------------

def fit_data(fx, xi, set_x):
    """ To determite x0, x1, f0, f1 for linear interpolation """
    nearest_x = find_nearest_num(xi, set_x)
    index_x = xi.index(nearest_x)
    x0 = 0
    x1 = 0
    f0 = 0
    f1 = 0
    if xi[index_x] < set_x:
        x0 = xi[index_x]
        x1 = xi[index_x + 1]
        f0 = fx[index_x]
        f1 = fx[index_x + 1]
    else:
        x0 = xi[index_x - 1]
        x1 = xi[index_x]
        f0 = fx[index_x - 1]
        f1 = fx[index_x]
    return [x0, x1, f0, f1, set_x]

#-------------------------------------------------------------------------------

def write_data(path, data):
    """ To convert data to string and to write them in file """
    if data == None:
        return None

    str_data = ''
    if data[0] != None:
        str_data += 'short-circuit current:\t' + str(data[0]) + '\n'
    if data[1] != None:
        str_data += 'open-circuit voltage:\t' + str(data[1]) + '\n'
    if data[2] != None:
        str_data += 'the point of power maximum:\t' + str(data[2]) + '\n'
    if data[3] != None:
        str_data += 'filling factor:\t' + str(data[3]) + '\n'

    write_file(path + '.txt', str_data)
    print(__name__ + ": data is written")

def main():
    table = prepare_data()
    res = calc(table)
    print(res)
    write_data('CVC_sc', res)
    #test of element multiply
##    col1 = [1, 2, 3]
##    col2 = [1, 2, 3]
##    res = element_multiply(col1, col2)
##    print(res)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
