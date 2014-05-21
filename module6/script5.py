#-------------------------------------------------------------------------------
# Name:        script5
# Purpose:
#
# Author:      Nataliya
#
# Created:     09.10.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import stderr
from .tools import read_file, cut_column, is_existed
from .tools import write_data as write
#-------------------------------------------------------------------------------

def prepare_data(path):
    """ to prepare data for calculation:
        path - 'rta.d'
    """

    table = read_file(path)
    if not is_existed(table):
        stderr.write("Error: file " + path + " is not found\n")
        return None
    del table[0] # delete heads
    print(__name__ + ": data is prepared")
    return table

def calc(table):
    """ to calculate:
        1. T = w[2]/w[1]
        2. R = w[0]/w[1]
        3. A = 1 - T - R
    """
    print(__name__ + ": calculating...")
    if not is_existed(table):
        stderr.write("Data is incorrect\n")
        return None
    tra = []
    f = cut_column(table, 0)
    w0 = cut_column(table, 1)
    w1 = cut_column(table, 2)
    w2 = cut_column(table, 3)
    for i in range(len(table)):
        if w1[i]!=0:
            tra.append([1/f[i], w2[i]/w1[i], w0[i]/w1[i], 1.0 - w2[i]/w1[i]\
            - w0[i]/w1[i]])
    return tra
#-------------------------------------------------------------------------------

def write_data(path, data_name, data):
    """ To convert data to string and to write them in file """
    write(path, data_name, None, data)

#-------------------------------------------------------------------------------
def main():
    table = prepare_data('rta.d')
    res = calc(table)
    print(res)

if __name__ == '__main__':
    main()
