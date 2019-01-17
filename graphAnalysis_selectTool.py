# -*- coding: utf-8 -*
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
from operator import itemgetter

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
from qgis.core import QgsPointXY, QgsGeometry, QgsWkbTypes
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand

from .graphAnalysis_layer import GraphAnalysisLayer

from .utils import tryfloat

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *

def isLayerVisible(iface, layer):
    # TODO Really ???? See if there is something simpler
    vl = iface.layerTreeView().layerTreeModel().rootGroup().findLayer(layer)
    return vl.itemVisibilityChecked()


def setLayerVisible(iface, layer, visible):
    vl = iface.layerTreeView().layerTreeModel().rootGroup().findLayer(layer)
    vl.setItemVisibilityChecked(visible)


class GraphSelectTool(QgsMapToolEmitPoint):

    mouseMove = pyqtSignal(QgsPointXY)
    mouseClicked = pyqtSignal(QgsPointXY)
    selectionChanged = pyqtSignal()

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self.canvas)

        self.rb = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.rb.setColor(QColor(255,0,0,50))
        self.rb.setFillColor(QColor(255,0,0,50))
        self.rb.setWidth(1)
        self.drawrubber = False
        self.rubberPointX = 0
        self.rubberPointY = 0
        self.layer = None

    def setLayer(self, layer):
        self.layer = layer

    def reset(self):
        self.rb.reset(QgsWkbTypes.PolygonGeometry)


    def canvasPressEvent(self, e):
        self.rubberPointX = e.x()
        self.rubberPointY = e.y()
        self.drawrubber= True


    def canvasReleaseEvent(self, e):

        myOriginalPoint = QgsPointXY(self.canvas.getCoordinateTransform().toMapCoordinates(e.x(), e.y()))
        self.mouseClicked.emit(myOriginalPoint)
        
        self.reset()
        self.drawrubber = False

        myOldPoint = QgsPointXY(self.canvas.getCoordinateTransform().toMapCoordinates(self.rubberPointX, self.rubberPointY))
        rect = QgsRectangle(myOldPoint, myOriginalPoint)

        if(self.layer.select(rect)): 
        
            self.selectionChanged.emit()

        self.canvas.refresh()


    def canvasMoveEvent(self, e):

        myOriginalPoint = QgsPointXY(self.canvas.getCoordinateTransform().toMapCoordinates(e.x(), e.y()))
        self.mouseMove.emit(myOriginalPoint)

        if(self.drawrubber):    
            myPoint1 = QgsPointXY(self.canvas.getCoordinateTransform().toMapCoordinates(e.x(),e.y()))
            myPoint2 = QgsPointXY(self.canvas.getCoordinateTransform().toMapCoordinates(self.rubberPointX,e.y()))
            myPoint3 = QgsPointXY(self.canvas.getCoordinateTransform().toMapCoordinates(self.rubberPointX,self.rubberPointY))
            myPoint4 = QgsPointXY(self.canvas.getCoordinateTransform().toMapCoordinates(e.x(),self.rubberPointY))


            self.reset()
            #convert screen coordinates to map coordinates
            self.rb.addPoint( myPoint1, False )
            self.rb.addPoint( myPoint2, False )
            self.rb.addPoint( myPoint3, False )
            self.rb.addPoint( myPoint4, True ) #true - update canvas
            self.rb.show()

