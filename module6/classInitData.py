# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        initial data
# Purpose:

#scriptNum - script number
#wavelen - wavelength
#azAngle - azimuth angle
#conAngle - cone angle
#
# Author:      Nataliya
#
# Created:     18.09.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class InitData(object):
    """ class containing initial data to setup module 6
        scriptNum - script number
        wavelen - wavelength
        azAngle - azimuth angle
        conAngle - cone angle
    """
    def __init__(self, scriptNum = [],  wavelen = None, azAngle = None,\
    conAngle = None, voltage = None):
        self.scriptNum = scriptNum
        self.wavelen = wavelen
        self.azAngle = azAngle
        self.conAngle = conAngle
        self.voltage = voltage
#-------------------------------------------------------------------------------

def main():
    initData = InitData([1, 2, 3], 1, 0, 5)
    print(InitData([1, 2, 3], 1, 0, 5).scriptNum)

if __name__ == '__main__':
    main()
