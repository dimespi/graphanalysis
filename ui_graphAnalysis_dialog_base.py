# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphAnalysis_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GraphAnalysisDialogBase(object):
    def setupUi(self, GraphAnalysisDialogBase):
        GraphAnalysisDialogBase.setObjectName("GraphAnalysisDialogBase")
        GraphAnalysisDialogBase.resize(482, 120)
        self.button_box = QtWidgets.QDialogButtonBox(GraphAnalysisDialogBase)
        self.button_box.setGeometry(QtCore.QRect(130, 80, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.label = QtWidgets.QLabel(GraphAnalysisDialogBase)
        self.label.setGeometry(QtCore.QRect(10, 30, 91, 16))
        self.label.setObjectName("label")
        self.lineEditGraphPath = QtWidgets.QLineEdit(GraphAnalysisDialogBase)
        self.lineEditGraphPath.setGeometry(QtCore.QRect(110, 30, 271, 20))
        self.lineEditGraphPath.setObjectName("lineEditGraphPath")
        self.pushButtonBrowse = QtWidgets.QPushButton(GraphAnalysisDialogBase)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(390, 30, 81, 23))
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")

        self.retranslateUi(GraphAnalysisDialogBase)
        self.button_box.accepted.connect(GraphAnalysisDialogBase.accept)
        self.button_box.rejected.connect(GraphAnalysisDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(GraphAnalysisDialogBase)

    def retranslateUi(self, GraphAnalysisDialogBase):
        _translate = QtCore.QCoreApplication.translate
        GraphAnalysisDialogBase.setWindowTitle(_translate("GraphAnalysisDialogBase", "Graph Analysis"))
        self.label.setText(_translate("GraphAnalysisDialogBase", "Graph path"))
        self.pushButtonBrowse.setText(_translate("GraphAnalysisDialogBase", "Browse..."))

