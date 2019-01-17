

class Edge:

    def __init__(self, nodeA, nodeB):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.isDirected = False
        self.directedA = False
        self.directedB = False
        self.features = {}

    def getNodeA(self):
        return self.nodeA

    def getNodeB(self):
        return self.nodeB
    
    def setNodeA(self, node):
        self.nodeA = node
        
    def setNodeB(self, node):
        self.nodeB = node
    
    def isDirected(self):
        return self.isDirected

    def isDirectedA(self):
        return self.directedA

    def isDirectedB(self):
        return self.directedB

    def setDirected(self, isDirected, directedA, directedB):
        self.isDirected = isDirected
        self.directedA = directedA
        self.directedB = directedB

    def addFeature(self, feature, value):
        self.features[feature] = value

    def removeFeature(self, feature):
        del self.features[feature]

    def removeAllFeatures(self):
        self.features.clear()

    def getFeatures(self):
        return self.features

    def getFeature(self, feature):
        return self.features[feature]


