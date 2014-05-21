# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        classGraphPlotData
# Purpose:
#
# Author:      Наталия
#
# Created:     01.10.2013
# Copyright:   (c) Наталия 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import exit, stderr

try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print("running with ElementTree")
                except ImportError:
                    stderr.write("Failed to import ElementTree from any known place")
                    exit()
#-------------------------------------------------------------------------------

class PlotDataXML(object):
    """ to create xml file for graph """
    def __init__(self):
        self.root = None
        self.xsi =  "http://www.w3.org/2001/XMLSchema-instance"
        self.xsd =  "grpaph_plot_data.xsd"
#-------------------------------------------------------------------------------

def setTitles(self, graph_title, x_name, y_name):
    """ to set Title in xml file: graph title, X title, Y title, Graph Name """
    ns = {"xmlns:xsi": self.xsi, "xmlns:xsd": self.xsd}
    for attr, uri in ns.items():
        etree.register_namespace(attr.split(":")[1], uri)

    self.root = etree.Element("GraphPlotData", {etree.QName(self.xsi, "noNamespaceSchemaLocation"): etree.QName(self.xsd)}) # put `**ns))` if xsi, xsd are unused

    title = etree.SubElement(self.root, "Title")
    title.text = graph_title
    axes = etree.SubElement(self.root, "Axes")

    x = etree.SubElement(axes, "X")
    x.set("type", "linear")
    x_title = etree.SubElement(x, "Title")
    x_title.text = x_name

    y = etree.SubElement(axes, "Y")
    y.set("type", "linear")
    y_title = etree.SubElement(y, "Title")
    y_title.text = y_name

#-------------------------------------------------------------------------------


def setData(self, xml_data, graph_name):
    """ to set Data in xml file and write xml file """
    if xml_data == None:
        return None
    table = []
    if type(xml_data[0]) == str:
        for line in xml_data:
            temp =line.split()
            table.append(temp)
    else:
        table = xml_data

    new_table = []
    for i in range(len(graph_name)):
        temp = []
##        print('Length = '+str(len(table)))
        for j in range(len(table)):
            temp.append([table[j][0], table[j][i + 1]])
        new_table.append(temp)
    data = etree.SubElement(self.root, "Data")
    plot = []
    for i in range(len(graph_name)):

        plot.append(etree.SubElement(data, "Plot"))
        plot[i].set("name", graph_name[i])
        plot[i].set("plot_type", "line")

        for line in new_table[i]:
            point = etree.SubElement(plot[i], "Point")
            point.set("y", str(line[1]))
            point.set("x", str(line[0]))

def writeXML(self, fileName):
    """ to write XML-file """
    tree = etree.ElementTree(self.root)
    tree.write(fileName + '.xml',
           xml_declaration=True,encoding='utf-8',
           method="xml")
    return tree
#-------------------------------------------------------------------------------

def main():
    xml_text = GraphPlotData()
    setTitles(xml_text, "Graph Title", "X name", "Y name")

    setData(xml_text, [[1,2,3],[4,5,6],[7,8,9]],  ["Graph Name1", "Graph Name2"])
    writeXML(xml_text, "test_xml")
##    s = etree.tostring(xml_text.root, pretty_print=True)

if __name__ == '__main__':
    main()
