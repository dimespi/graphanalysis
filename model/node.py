from qgis.core import QgsPointXY

class Node:
    
    id
    x = 0.00
    y = 0.00
    features = {}

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.features = {}

    def getId(self):
        return self.id

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def addFeature(self, feature, value):
        self.features[feature] = value

    def getFeatures(self):
        return self.features

    def getFeature(self, feature):
        return self.features[feature]

    def removeFeature(self, feature):
        del self.features[feature]

    def removeAllFeatures(self):
        self.features.clear()

    def getPoint(self):
        #Localisation exprimée dans le système de coordonnées du graphe auquel il appartient
        return  QgsPointXY(self.x,self.y)

