# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qgsgraphnewattributedialog_guibase.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewAttributeDialogGui(object):
    def setupUi(self, NewAttributeDialogGui):
        NewAttributeDialogGui.setObjectName("NewAttributeDialogGui")
        NewAttributeDialogGui.resize(423, 159)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewAttributeDialogGui)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(NewAttributeDialogGui)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(NewAttributeDialogGui)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(NewAttributeDialogGui)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(NewAttributeDialogGui)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(NewAttributeDialogGui)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(NewAttributeDialogGui)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewAttributeDialogGui)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewAttributeDialogGui)
        self.buttonBox.accepted.connect(NewAttributeDialogGui.accept)
        self.buttonBox.rejected.connect(NewAttributeDialogGui.reject)
        QtCore.QMetaObject.connectSlotsByName(NewAttributeDialogGui)

    def retranslateUi(self, NewAttributeDialogGui):
        _translate = QtCore.QCoreApplication.translate
        NewAttributeDialogGui.setWindowTitle(_translate("NewAttributeDialogGui", "Dialog"))
        self.label.setText(_translate("NewAttributeDialogGui", "Attribute name"))
        self.label_2.setText(_translate("NewAttributeDialogGui", "Attribute type"))
        self.comboBox.setItemText(0, _translate("NewAttributeDialogGui", "String"))
        self.comboBox.setItemText(1, _translate("NewAttributeDialogGui", "Integer"))
        self.comboBox.setItemText(2, _translate("NewAttributeDialogGui", "Real"))
        self.label_3.setText(_translate("NewAttributeDialogGui", "Default value"))

