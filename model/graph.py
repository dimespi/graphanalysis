

class Graph:

    def _init_(self):
        #Dictionnaire des noeuds
        self.listNode = {}
        #Liste des arcs 
        self.listEdge = []
        #Dictionnaire des features
        self.listFeatures = {}
        
    def getListNode(self):
        return self.listNodes

    def getListEdge(self):
        return self.listEdges

    def setListNode(self, nodes):
        self.listNodes = nodes

    def setListEdge(self, edges):
        self.listEdges = edges

    def getListFeatures(self):
        return self.listFeatures