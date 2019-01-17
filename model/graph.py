

class Graph:

    def __init__(self):
        #Dictionnaire des noeuds
        self.listNodes = {}
        #Liste des arcs 
        self.listEdges = []
        
    def getListNode(self):
        return self.listNodes

    def getListEdge(self):
        return self.listEdges

    def setListNode(self, nodes):
        self.listNodes = nodes

    def setListEdge(self, edges):
        self.listEdges = edges
