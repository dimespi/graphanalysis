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

import os.path

from PyQt5.QtCore import qDebug
from qgis.core import QgsProject


# constants for saving data inside QGS
SETTINGS_KEY = "graphanalysis"
SETTING_BROWSER_GRAPH_DIR = "browseGraphDir"


def toRelativeToQGS(graphPath):
    if os.path.isabs(graphPath):
        # Make it relative to current project if graph below QGS
        graphFolder, graphName = os.path.split(graphPath)
        qgsPath = QgsProject.instance().fileName()
        qgsFolder, _ = os.path.split(qgsPath)
        graphFolder = os.path.abspath(graphFolder)
        qgsFolder = os.path.abspath(qgsFolder)

        if graphFolder.startswith(qgsFolder):
            # relative
            graphFolderRelPath = os.path.relpath(graphFolder, qgsFolder)
            graphPath = os.path.join(graphFolderRelPath, graphName)
            qDebug(graphPath.encode())

    return graphPath

#Fonction permettant de récupérer un fichier présent dans le répertoire du plugin
def resolve(name, basepath=None):
    if not basepath:
      basepath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(basepath, name)

def tryfloat(strF):
    try:
        f = float(strF)
        return f
    except ValueError:
        return None
