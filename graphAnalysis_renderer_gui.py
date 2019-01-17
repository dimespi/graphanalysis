import os.path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from .graphReader import GraphReader

from qgis.core import *
from qgis.gui import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from .ui_graphAnalysis_renderer_gui import Ui_GraphAnalysisRendererGuiBase
from .ui_qgsgraphnewattributedialog_guibase import Ui_NewAttributeDialogGui

from .graphAnalysis_layer import GraphAnalysisLayer

class GraphAnalysisRendererGui(QDialog, Ui_GraphAnalysisRendererGuiBase):
    def __init__(self, layer):
        QDialog.__init__(self)
        # set up the user interface
        self.setupUi(self)
        self.setWindowTitle("%s - %s" %
                            (self.tr("Layer Properties"), layer.name()))
        self.layer = layer


        self.leSpatialRefSys.setText( layer.crs().authid() + " - " + layer.crs().description() )
        self.leSpatialRefSys.setCursorPosition( 0 )
        self.leLayerSource.setText(layer.filepath)

        self.mLayerTitleLineEdit.setText(layer.title)

        self.graphReader = GraphReader()
        self.graph = self.graphReader.read(layer.getAbsoluteFilepath())
        self.nodeAttributesTypes()
        self.edgeAttributesTypes()

        self.dialogNewAttribute = AddNewAttributeDialog(self.layer.filepath, self.graph)
        self.pushButton_AddNodeAttribute.clicked.connect(self.showAttributeDialog)


    def showAttributeDialog(self):
        dialog = AddNewAttributeDialog(self.layer.filepath, self.graph)
        dialog.exec_()

    def nodeAttributesTypes(self):
        nodes = self.graph.getListNode()
        for key,val in nodes.items():
            features = nodes[key].getFeatures()
            break
        i = 0
        for key,val in features.items():
            self.tblNodeAttributes.insertRow(i)
            self.tblNodeAttributes.setItem(i,0,QtWidgets.QTableWidgetItem(key))
            t = 'string'
            if val.isdigit():
                t = 'int'
            tokens = val.split('.')
            if len(tokens) == 2 and tokens[0].isdigit() and tokens[1].isdigit():
                t = 'float'
            self.tblNodeAttributes.setItem(i,1,QtWidgets.QTableWidgetItem(t))
            i += 1

    def edgeAttributesTypes(self):
        edges = self.graph.getListEdge()
        features = edges[0].getFeatures()
        i = 0
        for key,val in features.items():
            self.tblEdgeAttributes.insertRow(i)
            self.tblEdgeAttributes.setItem(i,0,QtWidgets.QTableWidgetItem(key))
            t = 'string'
            if val.isdigit():
                t = 'int'
            tokens = val.split('.')
            if len(tokens) == 2 and tokens[0].isdigit() and tokens[1].isdigit():
                t = 'float'
            self.tblEdgeAttributes.setItem(i,1,QtWidgets.QTableWidgetItem(t))
            i += 1



class AddNewAttributeDialog(QDialog, Ui_NewAttributeDialogGui):
    def __init__(self, filepath, graph, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.filepath = filepath
        self.graph = graph

        

    def addNodeAttribute(self):
        nodes = self.graph.getListNode()
        for key in nodes.items():
            features = nodes[key].getFeatures()
            break
        if (self.attNode in features) == False:
            graphFileReading = open(self.filepath,"r")
            lines = graphFileReading.readlines()
            graphFileReading.close()
            fileContent = ''
            graphFileWriting = open(self.filepath, "w")
            for line in lines:
                tokens = line.split()
                if tokens[0] == 'v':
                    fileContent = fileContent + line[:-2] + ',' + self.attNode + '=' +self.addedNode + ']\n'
                else:
                    fileContent = fileContent + line
            graphFileWriting.write(fileContent)
            graphFileWriting.close()

        for key,val in nodes.items():
            val.addFeature(self.attNode, self.addedNode)
        return self.accept()

    def addEdgeAttribute(self, name, defaultVal):
        attNode = self.lineEdit.text()
        addedNode = self.lineEdit_2.text()
        edges = self.graph.getListEdge()
        features = edges[0].getFeatures()
        if (self.attNode in features) == False:
            graphFileReading = open(self.filepath,"r")
            lines = graphFileReading.readlines()
            graphFileReading.close()
            fileContent = ''
            graphFileWriting = open(self.filepath, "w")
            for line in lines:
                tokens = line.split()
                if tokens[0] == 'u':
                    fileContent = fileContent + line[:-2] + ',' + attNode + '=' +addedNode + ']\n'
                else:
                    fileContent = fileContent + line
            graphFileWriting.write(fileContent)
            graphFileWriting.close()

        for edge in edges:
            edge.addFeature(attNode, addedNode)