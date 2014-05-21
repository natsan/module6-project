# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        setup
# Purpose: start of module 5
#
# Author:      Nataliya
#
# Created:     18.09.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import module6

#-------------------------------------------------------------------------------
def init(path = 'initial_data.txt'):
    """To read file "initial_data.txt" from PATH"""
    f = module6.open_file(path)
    if f == None:
        return None
    table = f.readlines()
    initData = None
    if 0<len(table)<6:
        sortData = []
        for line in table:
            temp = line.split()
            for n in temp:
                if module6.is_number(n):
                    sortData.append(float(n))
        # delete duplicates from the scripts
        dct, scripts = module6.remove_duplicates(sortData[0:-4])
        if (11 in scripts) and (12 in scripts):
            del scripts[scripts.index(12)] # script 11 and script 12 make one fucntion
        initData = module6.InitData(scripts,sortData[-4],sortData[-3],
        sortData[-2], sortData[-1])
    else:
        module6.stderr.write("Error: initial data is incorrect\n")
        exit()
    return initData
#-------------------------------------------------------------------------------

def start_script(script, init_data):
    """ to start script """

    if script == 1:
        found_wavelen, table = module6.script1.prepare_data('far.d', init_data.wavelen,\
        ['f', 'wavelength', 'theta', 'phi', 'P_norm', 'r'])
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 1 has failed\n")
            return

        # if table has a distance, the distance have to be deleted, to no write in file
        if len(table) == 4:
            module6.script1.write_data('angular','# 1-theta\t2-phi\t3-P_norm\n',
         'wavelength ' + str(found_wavelen), module6.join_columns(table[:-1]))
        else:
            module6.script1.write_data('angular','# 1-theta\t2-phi\t3-P_norm\n',
         'wavelength ' + str(found_wavelen), module6.join_columns(table))
        data = module6.script1.calc(table)
        module6.script1.write_data('angular_xy','# 1-x\t2-y\t3-P_norm\n',
         'wavelength ' + str(found_wavelen), module6.join_columns(data))

        surf = module6.PyPlotHTML()
        module6.setLegend(surf, 'Wavelength = ' + str(found_wavelen))
                              # x,     y,    intensity, phi,     theta
        module6.Surfe(surf, data[0], data[1], data[2], table[1], table[0])
        plot_name = module6.SavePng(surf, 'pic')
        module6.SaveHtml(surf, 'intensity', 1000, 1000)

    elif script == 2:
        found_wavelen, table = module6.script2.prepare_data('far.d', init_data.wavelen,
        ['f', 'wavelength', 'theta', 'phi', 'P_norm', 'r'])
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 2 has failed\n")
            return

        data = module6.script2.calc(table)
        module6.script2.write_data('intensity_polar_angle',
         '# 1-theta\t2-I_theta\n', 'wavelength ' + str(found_wavelen), data)

        xml_data = module6.PlotDataXML()
        module6.setTitles(xml_data, 'Angular intensity intergated over azimutal angles',
         "Polar angle, grad", "Intencity, arb")
        module6.setData(xml_data, data, ["Wavelength " + str(found_wavelen) + ', mkm'])
        module6.writeXML(xml_data, "intensity_polar_angle")

    elif script == 3:
        found_wavelen, found_angle, table = module6.script3.prepare_data('far.d', init_data.wavelen,
        init_data.azAngle, ['f', 'wavelength', 'theta', 'phi', 'P_norm', 'r'])
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 3 has failed\n")
            return

        module6.script3.write_data('intensity_azimuth_angle',
        '#1-theta\t3-P_norm\n', 'wavelength ' + str(found_wavelen), table)

        xml_data = module6.PlotDataXML()
        module6.setTitles(xml_data, 'Angular intensity at fixed azimutal angle',
         "Polar angle, grad", "Intencity, arb")
        module6.setData(xml_data, table, ["Wavelength "
          + str(found_wavelen) + ', mkm; Azimuth angle '
          + str(found_angle) + ', grad'])
        module6.writeXML(xml_data, "intensity_azimuth_angle")

    elif script == 4:
        table = module6.script4.prepare_data(init_data.conAngle,
        ['spectra.d', 'far.d', 'power.d'], ['f', 'wavelength', 'theta', 'phi',\
        'P_norm', 'r'])
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 4 has failed\n")
            return
        data = module6.script4.calc(init_data.conAngle, table)
        module6.script4.write_data('efficiency', \
        '#1-wavelength\t2-efficiency\n', None, data)

        xml_data = module6.PlotDataXML()
        module6.setTitles(xml_data, 'Efficiency', "Wavelength, mkm",\
         "Efficiency, arb")
        module6.setData(xml_data, data, ["Efficiency"])
        module6.writeXML(xml_data, "efficiency")
    elif script == 5:
        table = module6.script5.prepare_data('rta.d')
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 5 has failed\n")
            return
        data = module6.script5.calc(table)
        module6.script5.write_data('tra', '#1-wavelen\t2-T\t3-R\t4-A\n',
        data)

        xml_data = module6.PlotDataXML()
        module6.setTitles(xml_data, 'T, R, A', "Wavelength, mkm", "Coefficients, arb")
        module6.setData(xml_data, data, ['Transmission', 'Reflection',\
        'Absorption'])
        module6.writeXML(xml_data, "tra")
    elif script == 6:
        found_wavelen, table = module6.script6.prepare_data('detectors.d',\
        init_data.wavelen, [0, 2-1, 3-1, 4-1, 5-1, 6-1, 7-1])
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 6 has failed\n")
            return

        data = module6.script6.calc(table)
        module6.script6.write_data('field_intensity',\
        '#1-x\t2-y\t3-z\t4-Ixyz\n', 'wavelength ' + str(found_wavelen), data)
    elif script == 7:
        jsc_table, j_table = module6.script7.prepare_data('j_sc.d', 'j.d')
        if (not module6.is_existed(jsc_table)) and (not module6.is_existed(j_table)):
            module6.stderr.write("\nError: script 7 has failed\n")
            return
        data = module6.script7.calc(jsc_table)
        module6.script7.write_data('CVC_sc', data)

        if module6.is_existed(j_table):
            xml_data = module6.PlotDataXML()
            module6.setTitles(xml_data, 'Current-Voltage Characteristic',\
            "U, Volts", "I, A/сm^2")
            module6.setData(xml_data, j_table, ["Current-Voltage Characteristic"])
            module6.writeXML(xml_data, "cvc")

        if module6.is_existed(jsc_table):
            xml_data_jc = module6.PlotDataXML()
            module6.setTitles(xml_data_jc, 'Current-Voltage Characteristic',\
            "U, Volts", "I, A/сm^2")
            module6.setData(xml_data_jc, jsc_table,\
            ["Current-Voltage Characteristic"])
            module6.writeXML(xml_data_jc, "cvc_sc")

    elif script == 8:
        found_voltage, table = module6.script8.prepare_data(init_data.voltage,\
         ['x', 'y', 'z', 'Jnx[A/cm2]', 'Jny[A/cm2]', 'Jnz[A/cm2]', 'Jpx[A/cm2]',\
          'Jpy[A/cm2]', 'Jpz[A/cm2]', 'n[1/cm3]', 'p[1/cm3]', 'S', 'T'])
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 8 has failed\n")
            return

        dimension, data = module6.script8.calc(table)

        if dimension == 1:
            module6.script8.write_data('xJnJp', '# 1-x\t2-Jnx\t3-Jpx\t4-Jx\n',\
             'voltage ' + str(found_voltage), data[0])
            module6.script8.write_data('xnp', '# 1-x\t2-n\t3-p\n', 'voltage '\
             + str(found_voltage), data[1])
            module6.script8.write_data('xST', '# 1-x\t2-S\t3-T\n',\
            'voltage ' + str(found_voltage), data[2])

            xml_data1 = module6.PlotDataXML()
            module6.setTitles(xml_data1, 'xJ', "x, arb", "J, A/cm2")
            module6.setData(xml_data1, data[0], ['Jnx, voltage ' + \
            str(found_voltage) + ' V', 'Jpx, voltage ' + str(found_voltage)\
             + ' V', 'Jx, voltage ' + str(found_voltage) + ' V'])
            module6.writeXML(xml_data1, "xJnJp")

            xml_data2 = module6.PlotDataXML()
            module6.setTitles(xml_data2, 'xnp', "x, arb", "n, p, 1/cm3")
            module6.setData(xml_data2, data[1], ['n, voltage ' + \
            str(found_voltage) + ' V', 'p, voltage ' + str(found_voltage) + ' V'])
            module6.writeXML(xml_data2, "xnp")

            xml_data3 = module6.PlotDataXML()
            module6.setTitles(xml_data3, 'xST', "x", "S, T")
            module6.setData(xml_data3, data[2], ['S, voltage ' + \
            str(found_voltage) + ' V', 'T, voltage ' + str(found_voltage) + ' V'])
            module6.writeXML(xml_data3, "xST")

        if dimension == 2:
            module6.script8.write_data('xyJnJp',\
            '# 1-x\t2-y\t3-Jnx\t4-Jny\t5-Jpx\t6-Jpy\t7-Jx\t8-Jy\n',\
             'voltage ' + str(found_voltage), data[0])
            module6.script8.write_data('xynp', '# 1-x\t2-y\t3-n\t4-p\n',\
            'voltage ' + str(found_voltage), data[1])
            module6.script8.write_data('xyST', '# 1-x\t2-y\t3-S\t4-T\n',\
            'voltage ' + str(found_voltage), data[2])
        if dimension == 3:
            module6.script8.write_data('xyzJnJp',\
            '# 1-x\t2-y\t3-z\t4-Jnx\t5-Jny\t6-Jnz\t7-Jpx\t8-Jpy\t9-Jpz\t10-Jx\t11-Jy\t12-Jz\n',\
             'voltage ' + str(found_voltage), data[0])
            module6.script8.write_data('xyznp', '# 1-x\t2-y\t3-z\t4-n\t5-p\n',\
            'voltage ' + str(found_voltage), data[1])
            module6.script8.write_data('xyzST', '# 1-x\t2-y\t3-z\t4-S\t5-T\n',\
            'voltage ' + str(found_voltage), data[2])

    elif script == 9:
        table = module6.script9.prepare_data(['spectr.dat', 'far.d', 'power.d',\
         'chrom_curves.txt'], ['f', 'wavelength', 'theta', 'phi', 'P_norm'])
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 9 has failed\n")
            return
        data = module6.script9.calc(init_data.conAngle, table)
        module6.script9.write_data('chromaticity_temperatura', data)

    elif (script == 11) or (script == 12) :
        table = module6.script11.prepare_data(init_data.conAngle, ['j.d', 'R.d',\
         'spectr.dat', 'spectra.d', 'far.d','power.d'], ['f', 'wavelength',\
          'theta', 'phi', 'P_norm', 'r'])
        if not module6.is_existed(table):
            module6.stderr.write("\nError: script 11 has failed\n")
            return
        efficiency, heat_losses = module6.script11.calc(init_data.conAngle, table)
        xml_data1 = module6.PlotDataXML()
        module6.setTitles(xml_data1, 'Dependence of the efficiency on the voltage',\
        "Voltage, V", "Efficiency, arb")
        module6.setData(xml_data1, efficiency, ["Efficiency, cone angle " +\
        str(init_data.conAngle) + ', grad'])
        module6.writeXML(xml_data1, "efficacy")

        xml_data2 = module6.PlotDataXML()
        module6.setTitles(xml_data2, 'Dependence of the heat losses on the voltage',\
        "Voltage, V", "Heat Losses, W/cm^2")
        module6.setData(xml_data2, heat_losses, ["Heat Losses, cone angle " +\
        str(init_data.conAngle) + ', grad'])
        module6.writeXML(xml_data2, "heat_losses")
        module6.script11.write_data()

#-------------------------------------------------------------------------------

def main():
    inp = init()
    print("Script number: " + str(inp.scriptNum) + "; wavelength: " +
     str(inp.wavelen))
    print("Azimuth angle: " + str(inp.azAngle) + "; Cone angle: "
     + str(inp.conAngle))
    print('Voltage: '+ str(inp.voltage) + '\n')
    for script in inp.scriptNum:
        start_script(script, inp)

if __name__ == '__main__':
    main()