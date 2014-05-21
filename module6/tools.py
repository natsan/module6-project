# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        tools
# Purpose:
#
# Author:      Nataliya
#
# Created:     18.09.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import stderr
from math import fabs, sin, radians

#-------------------------------------------------------------------------------
def open_file(path):
    """ to open file
        string path
        file f
    """
    f = None
    try:
        f = open(path, 'r', encoding='UTF-8')
        print(__name__ + ': ' + str(f))
    except IOError:
        stderr.write("Error: can\'t find file or read data\n")
        return None

    return f
#-------------------------------------------------------------------------------
def write_file(path, data):
    """to open file and to write data
       string path
       list data
    """
    if data == None:
        return
    f = None
    try:
        f = open(path, 'w', encoding='UTF-8')
        print(__name__ + ': ' + str(f))
    except IOError:
        stderr.write("Error: can\'t find file or read data\n")
        return None
    f.write(data)
    f.close()
    print(__name__ + ": written content in the file successfully")
#-------------------------------------------------------------------------------

def read_file(path):
    """ to read file using readlines """
    f = open_file(path)
    if f == None:
        return None
    table = f.readlines()
    # delete empty lines
##    print("read file: " + str(table))
    while '\n' in table:
        del table[table.index('\n')]
    f.close()
    return table
#-------------------------------------------------------------------------------

def write_data(path, data_name, header, data):
    """ To convert data to string and to write them in file """
    if data == None:
        return None
    temp_data = ''
    for i in range(len(data)):
        for j in range(len(data[0])):
            temp_data += str(data[i][j]) + '\t'
        temp_data += '\n'

    full_data = ''
    if header != None:
        full_data = header + '\n' + data_name + temp_data
    else:
        full_data = data_name + temp_data

    write_file(path+'.txt', full_data)
    print(__name__ + ": data is written")
#-------------------------------------------------------------------------------

def is_existed(table):
    """ to determite is that the array is existed and is no empty """
    if table == None:
        return False
    if len(table) == 0:
        return False
    return True
#-------------------------------------------------------------------------------

def get_heads(string):
    """ get heads from string """

    if '#' in string:
        string = string.replace('#', '')
    names = string.split()

    heads = []
    for name in names:
        if '-' in name:
            t = name.split('-')
            heads.append(t[1])
        else:
            heads.append(name)

    return heads
#-------------------------------------------------------------------------------

def get_head_nums(heads, names):
    """ to get head numbers from list of heads
        heads - heads from data
        names - set heads which need to calculate
    """
    cut_columns = []
    for name in names:
        if name in heads:
            cut_columns.append(heads.index(name))
    return cut_columns
#-------------------------------------------------------------------------------

def is_number(s):
    """To determine this string is float number or no"""
    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
#-------------------------------------------------------------------------------

def to_string(table):
    """ to convert list to string without symbols """
    str_table = str(table)
    str_table = str_table.replace('],', '\n')
    str_table = str_table.replace('[', '')
    str_table = str_table.replace(']', '')
    str_table = str_table.replace(',', '')
    return str_table.splitlines()
#-------------------------------------------------------------------------------

def cut_data(table, cut_columns):
    """ to cut set columns from the table """
    cols = []
    for i in range(len(cut_columns)):
        cols.append(cut_column(table, cut_columns[i]))
    return cols
#-------------------------------------------------------------------------------

def cut_column(table, column_num):
    """ to get set column from table """
    if table == None:
        return None
    if column_num>len(table):
        return None
    column = []
    if type(table[0]) == str:
        for i in range(len(table)):
            temp = table[i].split()
            if len(temp) != 0:
                column.append(float(temp[column_num]))
    else:
        for i in range(len(table)):
            column.append(table[i][column_num])
    return column
#-------------------------------------------------------------------------------

def cut_table(table, col_numbers, set_index, set_value):
    """ to cut set columns from table using set number of first set line
        string list table
        float list new_table
    """
    new_table = []
    for i in range(set_index, len(table)):
        temp = table[i].split()
        if len(temp) == 0:
            continue
        if set_value != float(temp[col_numbers[0]]):
            break
        temp_list = []
        for j in col_numbers[1:]:
            if j in col_numbers:
                temp_list.append(float(temp[j]))
        new_table.append(temp_list)
    return new_table
#-------------------------------------------------------------------------------

def prepare_data(path, wavelength, names):
    """ to prepare data for calculation (for 'far.d')

        output data:
            found wavelength
            table:  table[0] = theta
                    table[1] = phi
                    table[2] = P_norm
    """
    table = read_file(path)
    if not is_existed(table):
        stderr.write("Error: file " + path + " is not found\n")
        return None, None

    heads = get_heads(table[0])
    cut_columns = get_head_nums(heads, names)
    del table[0] # delete heads
    column = cut_column(table,cut_columns[0])
    # return [dictionary[value, index], list without duplicates]
    l = remove_duplicates(column)
    # l[0] - dictionary
    # l[1] - ordered list without duplicates
    found_wav = None
    if heads[0] == 'wavelength':
        desired_value = find_nearest_num(l[1], wavelength)
        found_wav = desired_value
    elif heads[0] == 'f':
        desired_value = find_nearest_num(l[1], 1/wavelength)
        found_wav = 1 / desired_value
    else:
        stderr.write('Error: File is incorrect\n')
        return None, None
    new_table = cut_table(table, cut_columns, l[0][desired_value], desired_value)
    #reshape data, data will be in the form of sparated columns
    new_table = cut_data(new_table, [i for i in range(len(cut_columns)-1)])
    return found_wav, new_table

#-------------------------------------------------------------------------------

def remove_duplicates(col):
    """ remove duplicates from column
        output:
        dct - dictionary, where
        dct[0] - key (value from col),
        dct[1] - value (index from col)
        col2 - ordered list without duplicates
    """
    # dictionary where key is value of current col[i] and
    # value is key of current col[i]
    dct = {}
    col2 = []
    for i in range(len(col)):
        if col[i] not in col2:
            dct[col[i]] = i
            col2.append(col[i])
    return dct, col2
#-------------------------------------------------------------------------------

def find_nearest_num(l, set_value):
    """ to find nearest value to set value """
    dist1 = fabs(l[0] - set_value)
##    print('dist 1 = ' + str(dist1))
    desired_value = l[0]

    for x in l[1:]:
        dist2 = fabs(x - set_value)
##        print('dist 2 = ' + str(dist2))
        if dist2 <= dist1:
            dist1 = dist2
            desired_value = x
        else:
            break
    return desired_value
#-------------------------------------------------------------------------------

def del_char(str_list, ch):
    """ delete set char from string list """
    for i in range(len(str_list)):
        str_list[i] = str_list[i].replace(ch, '')
    return str_list
#-------------------------------------------------------------------------------

def rectangle_fun(f, x):
    """ to integrate using method of rectangles
        F(x) = Sum(  (f(i) + f(i+1)) * (x(i+1) - x(i))  )/2
    """
    s = sum((f[i]+f[i+1])*(radians(x[i+1])-radians(x[i]))/2 for i in range(len(f)-1))
    return s
#-------------------------------------------------------------------------------

def double_integral(table, cone_angle):
    """ for i in theta:
        for j in phi:
        Iup += (  ( (P_norm(i,j) + P_norm(i, j+1))*sin(theta(i)) +
        (P_norm(i+1, j) + P_norm(i+1, j+1))*sin(theta(i+1)) )
        *( theta(i+1) - theta(i)*(phi(j+1) - phi(j)/4
    """
    str_table = to_string(table)

    theta_col = cut_column(str_table, 0)
    temp = remove_duplicates(theta_col)
    theta_col = temp[1]

    phi_col = cut_column(str_table, 1)
    temp = remove_duplicates(phi_col)
    phi_col = temp[1]

    p_norm = cut_column(str_table, 2)
    desired_theta = find_nearest_num(theta_col, cone_angle)

    i_up = 0.0

    for i in range(len(theta_col) - 1):
        if theta_col[i] >= desired_theta:
            continue
        for k in range(len(phi_col) - 1):
            i_up += ((p_norm[len(phi_col)*i + (k + 0)] + p_norm[len(phi_col)*i + (k + 1)])\
            *sin(radians(theta_col[i])) +\
            (p_norm[len(phi_col)*(i+1) + (k+0)] + p_norm[len(phi_col)*(i+1) + (k+1)])\
            *sin(radians(theta_col[i + 1])))*\
            (radians(theta_col[i+1]) - radians(theta_col[i]))*(radians(\
            phi_col[k+1]) - radians(phi_col[k]))/4.0

    return i_up
#-------------------------------------------------------------------------------

def join_columns(columns):
    """ to join data """
    table = []
    for i in range(len(columns[0])):
        temp = []
        for j in range(len(columns)):
            temp.append(columns[j][i])
        table.append(temp)

    return table
#-------------------------------------------------------------------------------

def linear_interpolation(data):
    """ to find y for x in interval [x0, x1]
        y = f(x0) + (f(x1) - f(x0))*(x - x0)/(x1 - x0)
    """
    x0 = data[0]
    x1 = data[1]
    f0 = data[2]
    f1 = data[3]
    set_x = data[4]
    return f0 + (f1-f0)*(set_x - x0)/(x1-x0)
#-------------------------------------------------------------------------------

def element_multiply(col1, col2):
    """ To do element-wise multiplication of arrays """
    if len(col1) != len(col2):
        return None
    res = []
    for i in range(len(col1)):
        res.append(col1[i]*col2[i])
    return res
#-------------------------------------------------------------------------------

def cut_head(set_value, set_list, cut_lists):
    """ determine set range and cut list head using set value """
    first_value = find_nearest_num(set_list, set_value)
##    print('head: set value = ' + str(set_value) + '; found value = ' + str(first_value))
    first_index = set_list.index(first_value)
    for i in range(len(cut_lists)):
        cut_lists[i] = cut_lists[i][first_index -1 :]
    return cut_lists
#-------------------------------------------------------------------------------

def cut_tail(set_value, set_list, cut_lists):
    """ determine set range and cut list tail using set value """
    last_value = find_nearest_num(set_list, set_value)
##    print('tail: set value = ' + str(set_value) + '; found value = ' + str(last_value))
    last_index = set_list.index(last_value)
    for i in range(len(cut_lists)):
        cut_lists[i] = cut_lists[i][:last_index + 1]
    return cut_lists
#-------------------------------------------------------------------------------

def fit_grid(x1, x2, y1, y2, eps):
    """ fit grid step """
    i = 1
    j = 1
    new_y1 = []
    new_y2 = []
    x = []
    while True:
        # exit from infinity loop
        if i >= len(x2) or j >= len(x1):
            break
        if (i == len(x2)) and (x2[i]>x1[j] and fabs(x2[i] - x1[j]) > eps):
            break
        if (j == len(x1)) and (x2[i]<x1[j] and fabs(x2[i] - x1[j]) > eps):
            break
        # decide on what kind of grid to go
        if (x2[i]>x1[j]) and fabs(x2[i] - x1[j]) > eps:
            temp1 = []
            temp2 = []
            # interpolate
            for dd in y2:
                res = linear_interpolation([x2[i-1], x2[i], dd[i-1], dd[i], x1[j]])
                temp2.append(res)

            new_y2.append(temp2)

            for dd in y1:
                temp1.append(dd[j])

            new_y1.append(temp1)
            x.append(x1[j])

            j = j+1

        elif  x1[j]>x2[i] and fabs(x2[i] - x1[j]) > eps:
            temp1 = []
            temp2 = []
            for dd in y1:
                res = linear_interpolation([x1[j-1], x1[j], dd[j-1], dd[j], x2[i]])
                temp1.append(res)
            new_y1.append(temp1)

            for dd in y2:
                temp2.append(dd[i])
            new_y2.append(temp2)
            x.append(x2[i])

            i = i+1
        elif fabs(x2[i] - x1[j])<eps:
            temp1 = []
            temp2 = []
            for dd in y1:
                temp1.append(dd[j])
            new_y1.append(temp1)

            for dd in y2:
                temp2.append(dd[i])
            new_y2.append(temp2)
            x.append(x1[j])
            i = i+1
            j = j+1

    y1 = []
    y2 = []

    y1 = reshape_data(new_y1)
    y2 = reshape_data(new_y2)

    return [x, y1, y2]

#-------------------------------------------------------------------------------
def reshape_data(data):
    """ to reshape data
        for example [[1,2],[3,4],[5,6]] --> [[1,3,5],[2,4,6]]
    """
    new_data = []
    for i in range(len(data)):
        temp = []
        for j in range(len(data[0])):
            temp.append(data[i][j])
        new_data.append(temp)
    return new_data
#-------------------------------------------------------------------------------

def main():
    # test get_value()
##    table = read_file("spectra.d")
##    print(table)
##    t = get_value(table, 1.75)
##    print(t)
    #test method of rectangles
##    table = read_file('for_integrate.txt')
##    x = cut_column(table, 0)
##    f = cut_column(table, 1)
##    print(x)
##    print(f)
##    res = rectangle_fun(f, x)
##    print('Result = ' + str(res))
    #test is_number()
##    print(is_number(0.5))
##    print(is_number('skj'))
##    print(is_number('0.5'))
    #test prepare_data()
##    table = read_file('far.d')
##    column = cut_column(table,0)
##    print(len(table))
##    print(len(column))
##    print(column)
##    # return [dictionary[value, index], list without duplicates]
##    l = remove_duplicates(column)
##    print(l[0]) # dictionary
##    print[l[1]] # ordered list without duplicates
##    desiredValue = find_nearest_num(l[1], 1.42)
##    print('Desired value = ' + str(desiredValue))
##    print(l[0][desiredValue])
##    new_table = cut_table(table, [0, 3 - 1, 4 - 1, 11 - 1], l[0][desiredValue], desiredValue)
##    print(table)
##    print(new_table)
##    print(len(new_table))
##    print(len(new_table[0]))
    # test listmerge
##    table1 = ['ab', 'bc', 'cd']
##    table2 = ['text']
##    tt = [table2, table1]
##    print(tt)
##    res = listmerge(tt)
##    print(res)
    # test prepare_data
##    table = prepare_data('far.d', 1.42, [0, 3 - 1, 4 - 1, 11 - 1])
##    print(len(table))
##    write_data('output1','# 1-theta\t2-phi\t3-P_norm\n', 1.42, table)
    # test split in columns
##    res = connect_columns([[1,2,3], [4, 5, 6]])
##    print(res)
    # test cut_columns
##    res = cut_column([[1,2,3],[4,5,6]],1)
##    print(res)
    # test new function 'prepare_data
    pass

if __name__ == '__main__':
    main()