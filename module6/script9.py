# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        script9
# Purpose:
#
# Author:      Nataliya
#
# Created:     11.10.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from .tools import cut_column, remove_duplicates, cut_table, read_file,\
write_file, find_nearest_num, linear_interpolation, double_integral,\
rectangle_fun, join_columns, element_multiply, del_char, get_heads,\
get_head_nums, is_existed, cut_head, cut_tail, fit_grid
from .tools import write_data as write
from math import fabs, pow
from sys import stderr
from .constants import X0, Y0

#-------------------------------------------------------------------------------

def prepare_data(path = ['spectr.dat', 'far.d', 'power.d', 'chrom_curves.txt'],\
                 names = None):
    """ to prepare data for calculation
        path[0] - 'spectr.dat'
        path[1] - 'far.d'
        path[2] - 'power.d'
        path[3] - 'chrom_curves.txt'

        output:
            [0] - wav1 (wavelength, nm)
            [1] -  i_g (point source spectrum calculated FDTD)
            [2] - far_table (spectrum and angular distribution of the released radiation)
            [3] - wav2 (wavelength, nm)
            [4] - spectrum (spectrum of emitting sources)
            [5] - wav3 (wavelength, nm)
            [6] - xyz (curves of addition)
    """
    # get table from 'far.d'
    table = read_file(path[1])
    if not is_existed(table):
        stderr.write("Error: file " + path[1] + " is not found\n")
        return None
    heads = get_heads(table[0])
    cut_columns = get_head_nums(heads, names)
    del table[0] # delete heads
    column = cut_column(table,cut_columns[0])
    # return [dictionary[value, index], list without duplicates]
    dct, col = remove_duplicates(column)
    # dct - dictionary
    # col - ordered list without duplicates
    far_table = []
    for i in range(len(col)):
        value = col[i]
        temp_table = cut_table(table, cut_columns, dct[value], value)
        far_table.append(temp_table)

    # read file 'power.d', get Ig
    p_table = read_file(path[2])
    if not is_existed(p_table):
        stderr.write("Error: file " + path[2] + " is not found\n")
        return None
    del p_table[0] # delete heads

    wav1 = cut_column(p_table, 0) # f = 1/wavelength or wavelength in mkm
    if heads[0] == 'f':
        # convert f (1/mkm) to wavelength (mkm)
        for i in range(len(wav1)):
            wav1[i] = 1/wav1[i]
        wav1.reverse()
    # convert wavelength (mkm) to wavelength (nm)
    convertMKMtoNM(wav1)
    i_g = cut_column(p_table, 1)
    i_g.reverse()

    # read file "spectr.dat", get spectrum
    spectrum = read_file(path[0])
    if not is_existed(spectrum):
        stderr.write("Error: file " + path[0] + " is not found\n")
        return None
    # delete ';' from table
    spectrum = del_char(spectrum, ';')

    # get wavelength, nm
    wav2 = cut_column(spectrum, 0)
    spectrum = cut_column(spectrum, 1)
    wav2.reverse()
    spectrum.reverse()

    #read chrom_curves.txt, get x, y z
    curves = read_file(path[3])
    if not is_existed(curves):
        stderr.write("Error: file " + path[3] + " is not found\n")
        return None

    wav3 = cut_column(curves, 0) #get wavelength, nm
    x = cut_column(curves, 1)
    y = cut_column(curves, 2)
    z = cut_column(curves, 3)
    xyz = join_columns([x, y, z])

    # cut set range of wavelength
    if wav2[0] > wav1[0] and wav2[0] >wav3[0]:
        res = cut_head(wav2[0], wav1, [wav1, i_g, far_table])
        wav1 = res[0]
        i_g = res[1]
        far_table = res[2]

        res = cut_head(wav2[0], wav3, [wav3, xyz])
        wav3 = res[0]
        xyz = res[1]

    elif wav1[0] > wav2[0] and wav1[0] > wav3[0]:
        res = cut_head(wav1[0], wav2, [wav2, spectrum])
        wav2 = res[0]
        spectrum = res[1]

        res = cut_head(wav1[0], wav3, [wav3, xyz])
        wav3 = res[0]
        xyz = res[1]

    elif wav3[0] > wav2[0] and wav3[0] > wav1[0]:
        res = cut_head(wav3[0], wav2, [wav2, spectrum])
        wav2 = res[0]
        spectrum = res[1]

        res = cut_head(wav3[0], wav1, [wav1, i_g, far_table])
        wav1 = res[0]
        i_g = res[1]
        far_table = res[2]

    if wav2[-1] < wav1[-1] and wav2[-1] < wav3[-1]:
        res = cut_tail(wav2[-1], wav1, [wav1, i_g, far_table])
        wav1 = res[0]
        i_g = res[1]
        far_table = res[2]

        res = cut_tail(wav2[-1], wav3, [wav3, xyz])
        wav3 = res[0]
        xyz = res[1]

    elif wav1[-1] < wav2[-1] and wav1[-1] < wav3[-1]:
        res = cut_tail(wav1[-1], wav2, [wav2, spectrum])
        wav2 = res[0]
        spectrum = res[1]

        res = cut_tail(wav1[-1], wav3, [wav3, xyz])
        wav3 = res[0]
        xyz = res[1]

    elif wav3[-1] < wav2[-1] and wav3[-1] < wav1[-1]:
        res = cut_tail(wav3[-1], wav2, [wav2, spectrum])
        wav2 = res[0]
        spectrum = res[1]

        res = cut_tail(wav3[-1], wav1, [wav1, i_g, far_table])
        wav1 = res[0]
        i_g = res[1]
        far_table = res[2]

    if (len(wav1) <= 1) or (len(wav2) <= 1) or (len(wav3) <= 1):
        if (len(wav1) <= 1):
            stderr.write("Error: the number of wavelengths is insufficient in files "\
             + path[1] +" и "+ path[2] + ". Number of wavelengths is required more than one.\n")
            return None
        if (len(wav2) <= 1):
            stderr.write("Error: the number of wavelengths is insufficient in file "\
             + path[0] + ". Number of wavelengths is required more than one.\n")
            return None
        if (len(wav3) <= 1):
            stderr.write("Error: the number of wavelengths is insufficient in file "\
             + path[3] + ". Number of wavelengths is required more than one.\n")
            return None
    print(__name__ + ": data is prepared")
    return [wav1, i_g, far_table, wav2, spectrum, wav3, xyz]
#-------------------------------------------------------------------------------

def calc(cone_angle, table, eps = 0.5):
    """ to calculate color temperature:
        1. calculate Efficiency(wav):
        for i in theta:
        for j in phi:
        Iup += (  ( (P_norm(i,j) + P_norm(i, j+1))*sin(theta(i)) +
        (P_norm(i+1, j) + P_norm(i+1, j+1))*sin(theta(i+1)) )
        *( theta(i+1) - theta(i)*(phi(j+1) - phi(j)/4

        Efficiency(wav)[i] = Iup[i] / Ig[i]

        2. fit grid step and calculate emission spectrum
        E(wav) = A(wav)[i] * Efficiency(wav)[i]
        3. fit grid step and calculate chromaticity coordinates:
            X = Sum( (E(wav)[i]*x(wav)[i] + E(wav)[i+1]*x(wav)[i+1])*
            (wav[i+1] - wav[i])/2 in range wav from 380 to 800 nm
            Y = --"--
            Z = --"--

            x = X/(X + Y + Z)
            y = Y/(X + Y + Z)
        4. calculate chromaticity temperatura
        n = (x - x0)/(y - y0), where x0 = 0.329, y0 = 0.187
        Tc = 669*n^4 - 779*n^3 + 3660*n^2 - 7047*n + 5652

        *wav == wavelength
    """
    print(__name__ + ": calculating...")
    if not is_existed(table):
        stderr.write("Data is incorrect\n")
        return None
    for i in range(len(table)):
        if not is_existed(table[i]):
            stderr.write("Data is incorrect\n")
            return None

    wav1 = table[0]
    i_g = table[1]
    far_table = table[2]

    wav2 = table[3]
    spectrum = table[4]

    wav3 = table[5]
    xyz = table[6]

    #calculate efficiency
    efficiency = []
    for i in range(len(far_table)):
        efficiency.append(double_integral(far_table[i], cone_angle)/i_g[i])
    i = 1
    j = 1
    emis_spectr = []
    wav = []
    new_eff = []
    new_spectr = []

    # fit grid step and calculate emission spectrum
    result = fit_grid(wav1, wav2, [efficiency], [spectrum], eps)
    if (len(result[0]) == 0):
        stderr.write("Error: the interpolation of wavelengths is failed. The number of wavelengths is insufficient\n")
        return None

    wav = result[0]
    new_eff = cut_column(result[1], 0)
    new_spectr =cut_column(result[2], 0)

    emis_spectr = element_multiply(new_eff, new_spectr)

    # cut set range of wavelength from 380 to 800 nm
    if wav[0] < 380:
        res = cut_head(380, wav, [wav, emis_spectr])
        wav = res[0]
        emis_spectr = res[1]

    if wav3[0] < 380:
        res = cut_head(380, wav3, [wav3, xyz])
        wav3 = res[0]
        xyz = res[1]

    if wav[-1] > 800:
        res = cut_tail(800, wav, [wav, emis_spectr])
        wav = res[0]
        emis_spectr = res[1]

    if wav3[-1] > 800:
        res = cut_tail(800, wav3, [wav3, xyz])
        wav3 = res[0]
        xyz = res[1]

    # fit grid step of E(wav) and x(wav), y(wav), z(wav)
    x = cut_column(xyz,0)
    y = cut_column(xyz,1)
    z = cut_column(xyz,2)
    result = fit_grid(wav, wav3, [emis_spectr], [x, y, z], eps)
    if (len(result[0]) == 0):
        stderr.write("Error: the interpolation of wavelengths is failed. The number of wavelengths is insufficient\n")
        return None

    final_wav = result[0]
    emis_spectr2 = cut_column(result[1], 0)
    x = cut_column(result[2], 0)
    y = cut_column(result[2], 1)
    z = cut_column(result[2], 2)

    # multiply E(wav)[i]*x(wav)[i]
    # multiply E(wav)[i]*y(wav)[i]
    # multiply E(wav)[i]*z(wav)[i]
    temp_x = []
    temp_y = []
    temp_z = []
    temp_x = element_multiply(emis_spectr2, x)
    temp_y = element_multiply(emis_spectr2, y)
    temp_z = element_multiply(emis_spectr2, z)

    # calculate chromaticity temperatura
    X = rectangle_fun(temp_x, final_wav)
    Y = rectangle_fun(temp_y, final_wav)
    Z = rectangle_fun(temp_z, final_wav)

    chromaticity_x = X/(X + Y + Z)
    chromaticity_y = Y/(X + Y + Z)

    n = (chromaticity_x - X0)/(chromaticity_y - Y0)
    tc = 669*pow(n, 4) - 779*pow(n, 3) + 3660 * n * n - 7047*n + 5652
    return [chromaticity_x, chromaticity_y, tc]
#-------------------------------------------------------------------------------

def convertMKMtoNM(f):
    """ convert mircometers to nanometers """
    for i in range(len(f)):
        f[i] = f[i]*1000
#-------------------------------------------------------------------------------

def write_data(path, data):
    """ To convert data to string and to write them in file """
    if data == None:
        return None

    str_data = ''
    str_data += 'x\t' + str(data[0]) + '\n'
    str_data += 'y\t' + str(data[1]) + '\n'
    str_data += 'Tc\t' + str(data[2]) + '\n'

    write_file(path + '.txt', str_data)
    print(__name__ + ": data is written")
#-------------------------------------------------------------------------------

def main():
    table = prepare_data(['spectr.dat', 'far.d', 'power.d', 'chrom_curves.txt'],\
    [0, 3 - 1, 4 - 1, 11 - 1])
    data = calc(40, table)
    write_data('chromaticity_temperatura', data)
    print(data)
##    print(table[0])
##    print(table[5])
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
