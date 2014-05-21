# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        script10
# Purpose:
#
# Author:      Наталия
#
# Created:     25.11.2013
# Copyright:   (c) Наталия 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from .script4 import prepare_data as prepare_nu
from .script4 import calc as calc_nu
from .tools import read_file, cut_column, del_char, is_existed, rectangle_fun,\
element_multiply, join_columns, cut_head, cut_tail, fit_grid, join_columns
from .constants import CHARGE
#-------------------------------------------------------------------------------

def prepare_data(cone_angle, path, names):
    """ to prepare data for calculation
        path[0] - 'j.d'
        path[1] - 'R.d'
        path[2] - 'spectr.dat'
        path[3] - 'spectra.d'
        path[4] - 'far.d'
        path[5] - 'power.d'

    """
    # read file 'j.d'
    j_data = read_file(path[0])
    if not is_existed(j_data):
        stderr.write("Error: file " + path[0] + " is not found\n")
        return None
    del j_data[0]
    v = cut_column(j_data, 0)
    j = cut_column(j_data, 1)
    # read file 'R.d'
    r_data = read_file(path[1])
    if not is_existed(r_data):
        stderr.write("Error: file " + path[1] + " is not found\n")
        return None
    del r_data[0]
    z = cut_column(r_data, 0)
    r = cut_column(r_data, 1)
    # read file 'spectr.dat'
    spectrum = read_file(path[2])
    if not is_existed(spectrum):
        stderr.write("Error: file " + path[2] + " is not found\n")
        return None
    # delete ';' from spectrum table
    spectrum = del_char(spectrum, ';')
    wav = cut_column(spectrum, 0)
    spectrum = cut_column(spectrum, 1)
    # convert wav (nm) to f (1/mkm)
    for i in range(len(wav)):
        wav[i] = wav[i]/1000

    nu_data = prepare_nu(cone_angle, path[3:6], names)
    print(__name__ + ": data is prepared")
    return [v, j, z, r, spectrum, wav, nu_data]
#-------------------------------------------------------------------------------

def calc(cone_angle, table, eps = 0.05):
    """ input data:
        wav_nu - wavelength
        nu(wav_nu) - spectral efficiency of light emission
        v - voltage
        j - current
        z
        r(z) - distribution of recombination
        spectrum(wav) - luminescence spectrum
        wav - wavelength
        eps - epsilon for grid step of wavelength
        to calculate:
        1. dependence of the efficiency on the voltage
            s = spectrum(wavelength)/Integral(spectrum(wavelength))
            e - elementary charghe
            gamma = e*Integral(R(z))/j(v)
            efficiency = gamma(v)*Integral(s*nu(wavelength))
        2. dependence of the heat losses on the voltage
            heat_losses = j*v*(1-efficiency)
    """
    print(__name__ + ": calculating...")
    if not is_existed(table):
        stderr.write("Data is incorrect\n")
        return None, None
    # calculate spectral efficiency of light emission
    nu = join_columns(calc_nu(cone_angle, table[-1]))
    wav_nu = nu[0] # wavelength
    nu = nu[1] # spectral efficiency of light emission
    v = table[0] # voltage
    j = table[1] # current
    z = table[2]
    r = table[3] # distribution of recombination
    spectrum = table[4] # luminescence spectrum
    wav = table[5] # wavelength

    # It needs to reverse wavelengths, spectrum and nu before integration
    spectrum.reverse()
    wav.reverse()
    nu.reverse()
    wav_nu.reverse()
    # 1) to normalize spectrum: norm_spectrum = spectrum[i]/Integral(spectrum(wav))
    integrated_spectrum = rectangle_fun(spectrum, wav)
    norm_spectrum = []
    for i in range(len(spectrum)):
        norm_spectrum.append(spectrum[i]/integrated_spectrum)

    # 2) gamma = e*Integral(r(z))/j[i], where e - elementary charge
    integrated_r = rectangle_fun(r, z)

    gamma = []
    for i in range(len(j)):
        gamma.append(CHARGE*integrated_r/j[i])

    # 3) efficiency = gamma[i]*Integral(norm_spectrum[i]*nu[i](wav))
    # cut set range of wavelength
    if wav[0] < wav_nu[0]:
        res = cut_head(wav_nu[0], wav, [wav, norm_spectrum])
        wav = res[0]
        norm_spectrum = res[1]
    elif wav_nu[0] < wav[0]:
        res = cut_head(wav[0], wav_nu, [wav_nu, nu])
        wav_nu = res[0]
        nu = res[1]

    if wav[-1] > wav_nu[-1]:
        res = cut_tail(wav_nu[-1], wav, [wav, norm_spectrum])
        wav = res[0]
        norm_spectrum = res[1]

    elif wav_nu[-1] > wav[-1]:
        res = cut_tail(wav[-1], wav_nu, [wav_nu, norm_spectrum])
        wav_nu = res[0]
        nu = res[1]

    # fit grid step of wavelength
    result = fit_grid(wav_nu, wav, [nu], [norm_spectrum], eps)
    if (len(result[0]) == 0):
        stderr.write("Error: the interpolation of wavelengths is failed. The number of wavelengths is insufficient\n")
        return None

    new_wav = result[0]
    new_nu = cut_column(result[1], 0)
    new_spectr =cut_column(result[2], 0)

    # multiply new_nu * new_spectrum
    new_nu = element_multiply(new_nu, new_spectr)

    # Integrate result
    integrated_nu = rectangle_fun(new_nu, new_wav)

    efficiency = []
    for i in range(len(gamma)):
        efficiency.append(gamma[i]*integrated_nu)
    heat_losses = []
    for i in range(len(efficiency)):
        heat_losses.append(1-efficiency[i])
    heat_losses = element_multiply(heat_losses, v)
    heat_losses = element_multiply(heat_losses, j)

    return join_columns([v, efficiency]), join_columns([v, heat_losses])
#-------------------------------------------------------------------------------

def write_data():
    print(__name__ + ": data is written")
#-------------------------------------------------------------------------------

def main():
    path = ['j.d', 'R.d', 'spectr.dat', 'spectra.d', 'far.d','power.d']
    names = ['f', 'wavelength', 'theta', 'phi', 'P_norm', 'r']
    table = prepare_data(40, path, names)
    calc(40, table)

if __name__ == '__main__':
    main()
