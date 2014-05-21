#-------------------------------------------------------------------------------
# Name:        script6
# Purpose:
#
# Author:      Nataliya
#
# Created:     09.10.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import stderr
from .tools import read_file, cut_column, remove_duplicates, find_nearest_num,\
cut_table, is_existed
from .tools import write_data as write
#-------------------------------------------------------------------------------

def prepare_data(path, wavelength, cut_columns):
    """ to prepare data for calculation:
        path - 'detectors.d'
    """
    table = read_file(path)
    if not is_existed(table):
        stderr.write("Error: file " + path + " is not found\n")
        return None, None
    del table[0] # delete heads
    column = cut_column(table,cut_columns[0])
    # return [dictionary[value, index], list without duplicates]
    dct, col = remove_duplicates(column)
    # dct - dictionary
    # col - ordered list without duplicates
    desired_value = find_nearest_num(col, 1/wavelength)
    new_table = cut_table(table, cut_columns, dct[desired_value], desired_value)
    print(__name__ + ": data is prepared")
    return 1/desired_value, new_table
#-------------------------------------------------------------------------------

def calc(table):
    """ to calculate the field intensity I(r, wavelength) = Ex^2 + Ey^2 + Ez^2
    """
    print(__name__ + ": calculating...")
    if not is_existed(table):
        stderr.write("Data is incorrect\n")
        return None
    Ixyz = []
    for i in range(len(table)):
        I = table[i][3]*table[i][3] + table[i][4]*table[i][4] + table[i][5]*table[i][5]
        Ixyz.append([table[i][0], table[i][1], table[i][2], I])
    return Ixyz
#-------------------------------------------------------------------------------

def write_data(path, data_name, header, data):
    """ To convert data to string and to write them in file """
    write(path, data_name, header, data)
#-------------------------------------------------------------------------------

def main():
    table = prepare_data("detectors.d", 0.15, [0, 2-1, 3-1, 4-1, 5-1, 6-1, 7-1])
    res = calc(table)
    print(res)

if __name__ == '__main__':
    main()
