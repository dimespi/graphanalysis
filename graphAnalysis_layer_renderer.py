# -*- coding: utf-8 -*-
"""
/***************************************************************************
 *                                                                         *
 *   This program is free software you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import (QgsPluginLayer, QgsPointXY, QgsProject, Qgis,
                       QgsCoordinateTransform, QgsRectangle,
                       QgsCoordinateReferenceSystem, QgsPluginLayerType,
                       QgsDataProvider, QgsMapLayerRenderer, QgsMessageLog)

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

        self.mNodeProperties = rendererContext.mNodeProperties
        self. mEdgeProperties = rendererContext.mEdgeProperties
        self.layer_transparency = 255

        self.pr = GraphRules().rule_set
        self.attribute = QString("none")

        #Par défaut, il n'y a aucune attribut de noeud utilisé pour définir les propriétés de dessin
        self.pr.default_prop_value=QVariant(1)
        self.mNodeProperties["size"]= self.pr
        self.pr.default_prop_value= QColor(0,0,0,255)
        self.mNodeProperties["fgcolor"]= self.pr
        self.pr.default_prop_value= QColor(255,255,255,255)
        self.mNodeProperties["bgcolor"]= self.pr
        self.pr.default_prop_value= QVariant(1)
        self.mNodeProperties["linewidth"]= self.pr
        self.pr.default_prop_value= QVariant(QString(""))
        self.mNodeProperties["shape"]= self.pr


        #Par défaut, il n'y a aucune attribut d'arc utilisé pour définir les propriétés de dessin
        self.pr.default_prop_value= QVariant(1)
        self.mEdgeProperties["linestyle"]= self.pr
        self.pr.default_prop_value= QColor(0,0,0,255)
        self.mEdgeProperties["fgcolor"]= self.pr
        self.pr.default_prop_value= QVariant(1)
        self.mEdgeProperties["linewidth"]= self.pr

        self.layer_transparency=255
    
#     def remove(property, type, r):
#         property_ruleset pr = getRuleSet(property, type)
#         QList<rule>.iterator it=pr.ruleset.begin()

#         while(it!=pr.ruleset.end()) {
#             if( (*it).attribute_val==r.attribute_val && (*it).proprety_val==r.proprety_val ) {
#                 it=pr.ruleset.erase(it)
#             } else {
#                 it++
#             }
#         }

# void QgsGraphLayerRenderer::remove(QString property, PROP_TYPE type, rule r)
# {

# }

    def render(self):
        # same implementation as for QGIS2
        return self.layer.draw(self.rendererContext)
