from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from .graphReader import GraphReader

from qgis.core import *
from qgis.gui import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from .ui_qgsgraphnewattributedialog_guibase import Ui_NewAttributeDialogGui
from .ui_graphAnalysis_renderer_gui import Ui_GraphAnalysisRendererGuiBase


class AddNewAttribute(QDialog, Ui_NewAttributeDialogGui):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

