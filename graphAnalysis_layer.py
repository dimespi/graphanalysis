# -*- coding: utf-8 -*-
"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import math
import os

from osgeo import gdal
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QSvgRenderer
from qgis.core import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets

from .graphReader import GraphReader
from .model import *
from .symbologyParser import SymbologyReader

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from .ui_graphAnalysis_dockwidget_base import Ui_GraphAnalysisDockWidgetBase

from . import utils


class GraphAnalysisLayer(QgsPluginLayer):

    LAYER_TYPE = "GraphAnalysisLayer"

    def __init__(self, plugin, filepath, title, screenExtent):
        QgsPluginLayer.__init__(self, GraphAnalysisLayer.LAYER_TYPE, title)

        self.plugin = plugin
        self.iface = plugin.iface
        self.screenExtent = screenExtent
        self.setValid(True)

        self.title = title
        self.filepath = filepath

        # set custom properties
        self.setCustomProperty("title", title)
        self.setCustomProperty("filepath", self.filepath)

        self.error = False
        self.initializing = False
        self.initialized = False
        self.initializeLayer(screenExtent)
        self._extent = None

        self.graphReader = GraphReader()

        self.symbo_reader = SymbologyReader()
        
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_GraphAnalysisDockWidgetBase()
        self.ui.setupUi(self.window)

        self.msgBox = QWidget()
        self.ui.selectionButton.clicked.connect(self.updateNodeFeatures)
        self.ui.addNodeFromLayerButton.clicked.connect(self.updateEdgeFeatures)

        self.provider = GraphAnalysisLayerProvider(self)

    def updateCrs(self):

        self.iface.mapCanvas().setExtent(self.extent())
        self.iface.mapCanvas().refresh()


    def dataProvider(self):
        # issue with DBManager if the dataProvider of the QgsLayerPlugin
        # returns None
        return self.provider


    def createMapRenderer(self, rendererContext):
        return GraphAnalysisLayerRenderer(self, rendererContext)

    
    # Read and create the GraphReader object from the model
    def readGraph(self):
        return self.graphReader.read(self.getAbsoluteFilepath())


    def draw(self, renderContext):
        qDebug("start drawing")
        painter = renderContext.painter()     
        painter.save()

        #if the graph imported is not testgen then it draws the graph without taking into account
        #the render.xml symbology
        if(self.title != "testgen"):
            self.drawGraph(renderContext)
        else:
             self.drawGraphSymbo(renderContext)

        painter.restore()
        return True

    """
    Fonctions de dessins
    """
    def drawGraph(self, renderContext):
        painter = renderContext.painter()
        mapToPixel = renderContext.mapToPixel()

        crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
        xform = QgsCoordinateTransform(self.crs(),crs,QgsProject.instance())
    

        nodes = self.readGraph().getListNode()

        for id in nodes:

            x = nodes[id].getX()
            y = nodes[id].getY()
            point = mapToPixel.transform(xform.transform((QgsPointXY(x,y))))
            painter.drawEllipse(point.x()-2,point.y()-2,4,4)


        edges = self.readGraph().getListEdge()

        for edge in edges:

            start = nodes[edge.getNodeA()]
            end = nodes[edge.getNodeB()]

            pointA = mapToPixel.transform(xform.transform((QgsPointXY(int(start.getX()),int(start.getY())))))
            pointB = mapToPixel.transform(xform.transform((QgsPointXY(int(end.getX()),int(end.getY())))))
            painter.drawLine(pointA.x(),pointA.y(),pointB.x(),pointB.y())

    def drawGraphSymbo(self, renderContext):

        painter = renderContext.painter()
        mapToPixel = renderContext.mapToPixel()

        crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
        xform = QgsCoordinateTransform(self.crs(),crs,QgsProject.instance())

        xml = self.symbo_reader.read(utils.resolve('render.xml'))

        pen = QPen()
        brush = QBrush()
        diameter = 0

        nodes = self.readGraph().getListNode()

        edges = self.readGraph().getListEdge()

        #Dessin des arcs
        for edge in edges:
            start = nodes[edge.getNodeA()]
            end = nodes[edge.getNodeB()]

            #Gestion des configurations de propriétés graphiques
            """
            Le fichier xml correspond à un dictionnaire de dictionnaire de rules:
            graphrenderer = {"node_rules": GraphRules, "edge_rules": GraphRules}
            """
            if 'edge_rules' in xml:

                #Récupération de la valeur par défaut de la rule du xml
                #Cas où il n'y a pas de ruleunit pour la rule en question
                for key,val in xml['edge_rules'].items():
                    rule_prop = key
                    graphRule = val
                    attribute_name = graphRule.getName() 
                    default_prop = graphRule.getDefaultProp().value()
                    list_ruleunit = graphRule.getRule()
                    if(len(list_ruleunit) == 0 ):  
                        if(rule_prop == "fgcolor"):
                            color = default_prop
                            pen.setColor( color )
                        elif(rule_prop == "linewidth"):
                            variant = default_prop
                            pen.setWidth(variant)
                        elif(rule_prop == "linestyle"):
                            variant = default_prop
                            pen.setStyle(Qt.PenStyle(variant))

            #Cas où il y a une ou plusieurs ruleunit dans le xml                
            dict_features = edge.getFeatures()
            for edge_att_name,edge_att_val in dict_features.items():
                if 'edge_rules' in xml:
                    for key,val in xml['edge_rules'].items():
                        rule_prop = key
                        graphRule = val
                        attribute_name = graphRule.getName()
                        default_prop = graphRule.getDefaultProp().value()
                        list_ruleunit = graphRule.getRule()

                        if(attribute_name == edge_att_name):
                            if(len(list_ruleunit) != 0 ):
                                #Permet d'affecter la prop_val à l'attr_val correspondant du fichier graph 
                                flag = 0
                                for index in range(len(list_ruleunit)):
                                    attribute_val = list_ruleunit[index].attr_val.value()
                                    prop_val = list_ruleunit[index].prop_val.value()
                                    if(str(edge_att_val) == str(attribute_val)):
                                        if(rule_prop == "fgcolor"):
                                            color = prop_val
                                            pen.setColor( color )
                                        elif(rule_prop == "linewidth"):
                                            variant = prop_val
                                            pen.setWidth(variant)
                                        elif(rule_prop == "linestyle"):
                                            variant = prop_val
                                            pen.setStyle(Qt.PenStyle(variant))
                                        flag = 1
                                        break
                                #Affecte la valeur par défaut à toutes les autres attr_val n'étant pas présentent dans la liste des rule_unit
                                if(flag == 0):
                                    if(rule_prop == "fgcolor"):
                                        color = default_prop
                                        pen.setColor( color )
                                    elif(rule_prop == "linewidth"):
                                        variant = default_prop
                                        pen.setWidth(variant)
                                    elif(rule_prop == "linestyle"):
                                        variant = default_prop
                                        pen.setStyle(Qt.PenStyle(variant))

            painter.setPen(pen)
            painter.setBrush(brush)

            pointA = mapToPixel.transform(xform.transform((QgsPointXY(int(start.getX()),int(start.getY())))))
            pointB = mapToPixel.transform(xform.transform((QgsPointXY(int(end.getX()),int(end.getY())))))
            painter.drawLine(pointA.x(),pointA.y(),pointB.x(),pointB.y())

        #Même chose pour le dessin des noeuds, avec des rule_prop différentes
        for id in nodes:
            x = nodes[id].getX()
            y = nodes[id].getY()
            if 'node_rules' in xml:

                #Récupération de la valeur par défaut de la rule du xml
                #Cas où il n'y a pas de ruleunit pour la rule en question
                for key,val in xml['node_rules'].items():
                    rule_prop = key
                    graphRule = val
                    attribute_name = graphRule.getName() 
                    default_prop = graphRule.getDefaultProp().value()
                    list_ruleunit = graphRule.getRule()
                    if(len(list_ruleunit) == 0 ):  
                        if(rule_prop == "bgcolor"):
                            color = default_prop
                            brush.setColor(color)
                            brush.setStyle( Qt.SolidPattern )
                        elif(rule_prop == "fgcolor"):
                            color = default_prop
                            pen.setColor( color )
                        elif(rule_prop == "linewidth"):
                            variant = default_prop
                            pen.setWidth(variant)
                        elif(rule_prop == "size"):
                            diameter = default_prop
                        elif(rule_prop == "shape"):
                            shape = default_prop                

            #Cas où il y a une ou plusieurs ruleunit dans le xml 
            dict_features = nodes[id].getFeatures()
            for node_att_name,node_att_val in dict_features.items():
                if 'node_rules' in xml:
                    for key,val in xml['node_rules'].items():
                        rule_prop = key
                        graphRule = val
                        attribute_name = graphRule.getName()
                        default_prop = graphRule.getDefaultProp().value()
                        list_ruleunit = graphRule.getRule()

                        if(attribute_name == node_att_name):
                            if(len(list_ruleunit) != 0 ):
                                #Permet d'affecter la prop_val à l'attr_val correspondant du fichier graph
                                flag = 0
                                for index in range(len(list_ruleunit)):
                                    attribute_val = list_ruleunit[index].attr_val.value()
                                    prop_val = list_ruleunit[index].prop_val.value()
                                    if(str(node_att_val) == str(attribute_val)):
                                        if(rule_prop == "bgcolor"):
                                            color = prop_val
                                            brush.setColor(color)
                                            brush.setStyle( Qt.SolidPattern )
                                        elif(rule_prop == "fgcolor"):
                                            color = prop_val
                                            pen.setColor( color )
                                        elif(rule_prop == "linewidth"):
                                            variant = prop_val
                                            pen.setWidth(variant)
                                        elif(rule_prop == "size"):
                                            diameter = prop_val
                                        elif(rule_prop == "shape"):
                                            shape = prop_val
                                        flag = 1
                                        break
                                #Affecte la valeur par défaut à toutes les autres attr_val n'étant pas présentent dans la liste des rule_unit
                                if(flag == 0):
                                    if(rule_prop == "bgcolor"):
                                        color = default_prop
                                        brush.setColor(color)
                                        brush.setStyle( Qt.SolidPattern )
                                    elif(rule_prop == "fgcolor"):
                                        color = default_prop
                                        pen.setColor( color )
                                    elif(rule_prop == "linewidth"):
                                        variant = default_prop
                                        pen.setWidth(variant)
                                    elif(rule_prop == "size"):
                                        diameter = default_prop
                                    elif(rule_prop == "shape"):
                                        shape = default_prop                                        

            painter.setPen(pen)
            painter.setBrush(brush)
            point = mapToPixel.transform(xform.transform((QgsPointXY(x,y))))


            #Différentes formes possibles pour la rule shape
            if(shape != ""): 
                if(shape == "circle"):
                    painter.drawEllipse(point.x()-diameter/2,point.y()-diameter/2,diameter,diameter)
                elif(shape == "rectangle"):
                    painter.drawRect(point.x()-diameter/2,point.y()-diameter/2,diameter,diameter)
                elif(shape == "cross"):
                    painter.drawLine(point.x()-diameter/2,point.y()-diameter/2,point.x()+diameter/2,point.y()+diameter/2)
                    painter.drawLine(point.x()-diameter/2,point.y()+diameter/2,point.x()+diameter/2,point.y()-diameter/2)
                else:
                    #Draw SVG Node
                    svgr = QSvgRenderer(shape)
                    if( svgr.isValid() ):
                        svgr.render(painter, QRectF(point.x()-diameter/2,point.y()-diameter/2,diameter,diameter))
                    else:
                        painter.drawEllipse(point.x()-diameter/2,point.y()-diameter/2,diameter,diameter)
            else:
                #default is circle
                painter.drawEllipse(point.x()-diameter/2,point.y()-diameter/2,diameter,diameter)



    def initializeLayer(self, screenExtent=None):
        if self.error or self.initialized or self.initializing:
            return
        self.setupCrs()

        self.initialized = True
        self.initializing = False


    def resetTransformParametersToNewCrs(self):
        """
        Attempts to keep the layer on the same region of the map when
        the map CRS is changed
        """
        oldCrs = self.crs()
        newCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        self.reprojectTransformParameters(oldCrs, newCrs)
        self.commitTransformParameters()

    def setupCrsEvents(self):
        layerId = self.id()

        def removeCrsChangeHandler(layerIds):
            if layerId in layerIds:
                try:
                    self.iface.mapCanvas().destinationCrsChanged.disconnect(
                        self.resetTransformParametersToNewCrs)
                except Exception:
                    pass
                try:
                    QgsProject.instance().disconnect(
                        removeCrsChangeHandler)
                except Exception:
                    pass

        self.iface.mapCanvas().destinationCrsChanged.connect(
            self.resetTransformParametersToNewCrs)
        QgsProject.instance().layersRemoved.connect(
            removeCrsChangeHandler)

    def setupCrs(self):
        mapCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        self.setCrs(mapCrs)

        self.setupCrsEvents()

    def getAbsoluteFilepath(self):
        if not os.path.isabs(self.filepath):
            # relative to QGS file
            qgsPath = QgsProject.instance().fileName()
            qgsFolder, _ = os.path.split(qgsPath)
            filepath = os.path.join(qgsFolder, self.filepath)
        else:
            filepath = self.filepath

        return filepath

    #Permet de zoomer directement sur le graphe
    def extent(self):
        if not self.initialized:
            qDebug("Not Initialized")
            return QgsRectangle(0, 0, 0, 0)

        if self._extent:
            return self._extent

        #Récupération de la liste des noeuds du graphe
        listNode = self.readGraph().getListNode()
        listX = []
        listY = []
        for id in listNode:
            listX.append(listNode[id].getX())
            listY.append(listNode[id].getY())

        #Permet de récupérer les coordonnées des 4 noeuds les plus éloignés du centre
        xMin = min(listX)
        xMax = max(listX)
        yMin = min(listY)
        yMax = max(listY)

        # recenter + create rectangle
        self._extent = QgsRectangle(xMin, yMin, xMax, yMax)
        return self._extent

    #Lecture/enregistrement du projet Qgis (.qgs) contenant le/les graphe(s) importé(s)
    def readXml(self, node, context):
        self.readCustomProperties(node)
        #Lecture de la balise customproperties du .qgs contenant l'emplacement du graph 
        self.filepath = self.customProperty("filepath", "")
        return True

    def writeXml(self, node, doc, context):
        element = node.toElement()
        #Ecriture du chemin du graph importé dans les customproperties du .qgs
        self.writeCustomProperties(node, doc)
        element.setAttribute("type", "plugin")
        element.setAttribute(
            "name", GraphAnalysisLayer.LAYER_TYPE)
        return True


    #Modification des attributs d'un noeud
    def updateNodeFeatures(self):
        ids = [self.ui.tbl_NodeAttributes.item(row, 0).text() for row in range(self.ui.tbl_NodeAttributes.rowCount())]
        atts = [self.ui.tbl_NodeAttributes.item(row, 1).text() for row in range(self.ui.tbl_NodeAttributes.rowCount())]
        values = [self.ui.tbl_NodeAttributes.item(row, 2).text() for row in range(self.ui.tbl_NodeAttributes.rowCount())]

        numNodes = 0
        for elt in ids:
            if elt != ' ':
                numNodes += 1

        if  numNodes > 1:
            QMessageBox.about(self.msgBox, 'Update aborted', 'ERROR : Select one single node when updating. Operation aborted!')

        else:
            graphFileReading = open(self.filepath,"r")
            lines = graphFileReading.readlines()
            graphFileReading.close()
            nodes = self.readGraph().getListNode()
            for key,val in nodes.items():
                if val.getId() == ids[0]:
                    node = Node(ids[0], val.getX(), val.getY())
                    val.removeAllFeatures()
                    for j in range(1,len(atts)):
                        val.addFeature(atts[j], values[j])
                    node = val

            graphFileWriting = open(self.filepath, "w")
            for line in lines:
                tokens = line.split()
                if tokens[0] == 'v' and tokens[1] == node.getId():
                    graphFileWriting.write(self.graphReader.nodeToGraphFormat(node))
                else:
                    graphFileWriting.write(line)
            graphFileReading.close()

    #Modification des attributs d'un arc
    def updateEdgeFeatures(self):
        nodeA = [self.ui.tbl_EdgeAttributes.item(row, 0).text() for row in range(self.ui.tbl_EdgeAttributes.rowCount())]
        nodeB = [self.ui.tbl_EdgeAttributes.item(row, 1).text() for row in range(self.ui.tbl_EdgeAttributes.rowCount())]
        atts = [self.ui.tbl_EdgeAttributes.item(row, 2).text() for row in range(self.ui.tbl_EdgeAttributes.rowCount())]
        values = [self.ui.tbl_EdgeAttributes.item(row, 3).text() for row in range(self.ui.tbl_EdgeAttributes.rowCount())]

        numEdges = 0
        for elt in nodeA:
            if elt != ' ':
                numEdges += 1

        if  numEdges > 1:
            QMessageBox.about(self.msgBox, 'Update aborted', 'ERROR : Select one single edge when updating. Operation aborted!')

        else:
            graphFileReading = open(self.filepath,"r")
            lines = graphFileReading.readlines()
            graphFileReading.close()
            edges = self.readGraph().getListEdge()
            for e in edges:
                if e.getNodeA() == nodeA[0] and e.getNodeB() == nodeB[0]:
                    edge = Edge(e.getNodeA(), e.getNodeB())
                    e.removeAllFeatures()
                    for j in range(1,len(atts)):
                        e.addFeature(atts[j], values[j])
                    edge = e

            graphFileWriting = open(self.filepath, "w")
            for line in lines:
                tokens = line.split()
                if tokens[0] == 'u' and tokens[1] == edge.getNodeA() and tokens[2] == edge.getNodeB():
                    graphFileWriting.write(self.graphReader.edgeToGraphFormat(edge))
                else:
                    graphFileWriting.write(line)
            graphFileReading.close()




# Gestion de la selection des noeuds ! 
 
# Fonction de selection des noeuds dans le rectangle
# Les arcs sont dans la sélection lorsque leurs deux
# extremitées sont dans la sélection des noeuds.
 
    def select(self, rect):

        nodes = self.readGraph().getListNode()
        m_selected_nodes = {}
        m_selected_edges = []

        for key,val in nodes.items():
            if(rect.contains(val.getPoint())):
                m_selected_nodes[key] = val

        edges = self.readGraph().getListEdge()
        for edge in edges:
            if(rect.contains(nodes[edge.getNodeA()].getPoint()) & rect.contains(nodes[edge.getNodeB()].getPoint())):
                m_selected_edges.append(edge)

        i = 0
        self.ui.tbl_NodeAttributes.setRowCount(0)
        for key, val in m_selected_nodes.items():
            # displaying the node's id row (NodeA and NodeB)
            self.ui.tbl_NodeAttributes.insertRow(i)
            self.ui.tbl_NodeAttributes.setItem(i,0,QtWidgets.QTableWidgetItem(val.getId()))
            self.ui.tbl_NodeAttributes.setItem(i,1,QtWidgets.QTableWidgetItem(" "))
            self.ui.tbl_NodeAttributes.setItem(i,2,QtWidgets.QTableWidgetItem(" "))
            # Setting a light blue bg for the edge's id row
            self.ui.tbl_NodeAttributes.item(i, 0).setBackground(QtGui.QColor(149,200,216))
            self.ui.tbl_NodeAttributes.item(i, 1).setBackground(QtGui.QColor(149,200,216))
            self.ui.tbl_NodeAttributes.item(i, 2).setBackground(QtGui.QColor(149,200,216))
            i = i + 1
            # displaying the node's features
            nFeatures = val.getFeatures()
            for key1, val1 in nFeatures.items():
                self.ui.tbl_NodeAttributes.insertRow(i)
                self.ui.tbl_NodeAttributes.setItem(i,0,QtWidgets.QTableWidgetItem(" "))
                self.ui.tbl_NodeAttributes.setItem(i,1,QtWidgets.QTableWidgetItem(key1))
                self.ui.tbl_NodeAttributes.setItem(i,2,QtWidgets.QTableWidgetItem(val1))
                i = i + 1

        j = 0
        self.ui.tbl_EdgeAttributes.setRowCount(0)
        for edge in m_selected_edges:
            # displaying the edge's id row (NodeA and NodeB)
            self.ui.tbl_EdgeAttributes.insertRow(j)
            self.ui.tbl_EdgeAttributes.setItem(j,0,QtWidgets.QTableWidgetItem(edge.getNodeA()))
            self.ui.tbl_EdgeAttributes.setItem(j,1,QtWidgets.QTableWidgetItem(edge.getNodeB()))
            self.ui.tbl_EdgeAttributes.setItem(j,2,QtWidgets.QTableWidgetItem(" "))
            self.ui.tbl_EdgeAttributes.setItem(j,3,QtWidgets.QTableWidgetItem(" "))
            # Setting a light blue bg for the edge's id row
            self.ui.tbl_EdgeAttributes.item(j, 0).setBackground(QtGui.QColor(149,200,216))
            self.ui.tbl_EdgeAttributes.item(j, 1).setBackground(QtGui.QColor(149,200,216))
            self.ui.tbl_EdgeAttributes.item(j, 2).setBackground(QtGui.QColor(149,200,216))
            self.ui.tbl_EdgeAttributes.item(j, 3).setBackground(QtGui.QColor(149,200,216))
            j = j + 1

            # displaying the edge's features
            eFeatures = edge.getFeatures()
            for key, val in eFeatures.items():
                self.ui.tbl_EdgeAttributes.insertRow(j)
                self.ui.tbl_EdgeAttributes.setItem(j,0,QtWidgets.QTableWidgetItem(" "))
                self.ui.tbl_EdgeAttributes.setItem(j,1,QtWidgets.QTableWidgetItem(" "))
                self.ui.tbl_EdgeAttributes.setItem(j,2,QtWidgets.QTableWidgetItem(key))
                self.ui.tbl_EdgeAttributes.setItem(j,3,QtWidgets.QTableWidgetItem(val))
                j = j + 1

        self.window.show()

class GraphAnalysisLayerType(QgsPluginLayerType):

    def __init__(self, plugin):
        QgsPluginLayerType.__init__(self, GraphAnalysisLayer.LAYER_TYPE)
        self.plugin = plugin

    def createLayer(self):
        return GraphAnalysisLayer(self.plugin, None, "", None)
    


    def showLayerProperties(self, layer):
        from .graphAnalysis_renderer_gui import GraphAnalysisRendererGui
        dialog = GraphAnalysisRendererGui(layer)

        dialog.exec_()
        return True


class GraphAnalysisLayerProvider(QgsDataProvider):
    def __init__(self, layer):
        QgsDataProvider.__init__(
            self, "dummyURI")

    def name(self):
        # doesn't matter
        return "GraphAnalysisLayerProvider"


class GraphAnalysisLayerRenderer(QgsMapLayerRenderer):
    """
    Custom renderer: in QGIS3 no implementation is provided for
    QgsPluginLayers
    """

    def __init__(self, layer, rendererContext):
        QgsMapLayerRenderer.__init__(
            self, layer.id())
        self.layer = layer
        self.rendererContext = rendererContext

    def render(self):
        # same implementation as for QGIS2
        return self.layer.draw(self.rendererContext)
