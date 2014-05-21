# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        classPyPlotHTML
# Purpose:
#
# Author:      Nataliya
#
# Created:     15.11.2013
# Copyright:   (c) Nataliya 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from .tools import remove_duplicates, write_file
from pylab import figure, savefig, title
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm
from math import radians, sin, cos
#-------------------------------------------------------------------------------

class PyPlotHTML(object):
    """ to create surface and save it in png """

    def __init__(self):
      self.pngName = 'pic'
      self.title = None
      self.axesTitle = None
#-------------------------------------------------------------------------------

def MakeSurfeData (x, y, intensity, phi, theta):
    """ reshape data to plot surface:
        1. prepare grid:
            x = sin(teta)*cos(phi)
            y = sin(teta)*sin(phi)
            z = cos(phi)
        2. reshape x, y, z
        3. prepare color map:
            find intensity maximum
            intensity = intesity/(intensity maximum)
        4. reshape intensity
    """
    # get all angles of phi removing duplicates
    temp = remove_duplicates(phi)
    phi = temp[1]
##    print('phi len ' + str(len(phi)))
    # get all angles of theta removing duplicates
    temp = remove_duplicates(theta)
    theta = temp[1]
##    print('theta len ' + str(len(theta)))

    xgrid = ReshapeData(x, int(len(x)/len(phi)), len(phi))
    ygrid = ReshapeData(y, int(len(y)/len(phi)), len(phi))

    zgrid = []
    for i in range(len(theta)):
        temp = []
        for j in range(int(len(y)/len(theta))):
            temp.append(cos(radians(theta[i])))
        zgrid.append(temp)

    max_intensity = max(intensity)

    for i in range(len(intensity)):
        intensity[i] = intensity[i]/max_intensity

    intensity = ReshapeData(intensity, int(len(intensity)/len(phi)), len(phi))

    return xgrid, ygrid, zgrid, intensity
#-------------------------------------------------------------------------------

def Surfe(self, x, y, intensity, phi, theta):
    """ to create surface """

    x, y, z, intensity = MakeSurfeData(x, y, intensity, phi, theta)

    fig = figure()
    axes = Axes3D(fig)
    axes.view_init(100, 0)
    surf = axes.plot_surface(x, y, z, rstride=1, cstride=1,\
    facecolors=cm.jet(intensity), linewidth=0, antialiased=False, shade=False)
    if self.title != None:
        title(self.title)
##    show()
#-------------------------------------------------------------------------------
def setLegend(self, name):
    self.title = name


def SavePng(self, title):
    """ save picture.png with title """
    title = title + '.png'
    savefig(title)
    self.pngName = title
    return title
#-------------------------------------------------------------------------------

def SaveHtml(self, path, width, height):
    """ write html file contained picture.png with path """
    string = '<html>\n<body>\n<img src=\'' + self.pngName + '\' alt="plot" width="'\
    + str(width) + '" height="' + str(height) + '"/>\n</body>\n</html>'
    write_file(path + '.html', string)

#-------------------------------------------------------------------------------

def ReshapeData(data, columns, rows):
    """ to reshape data
        for example:
            input data:
                data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                columns = 3
            output data:
                new_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    begin = 0
    end = 0
    new_data = []

    for i in range(columns):
        end = rows*(i+1)
        temp = data[begin:end]
        new_data.append(temp)
        begin = end
    return new_data
#-------------------------------------------------------------------------------

def main():
    pass
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
