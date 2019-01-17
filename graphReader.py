from .model import *
import ast

from qgis.core import QgsMessageLog

class GraphReader:


    def read(self, path):
        nodes = {}
        edges = []  

        graphDoc = open(path, 'r')
        lines = graphDoc.readlines()
        for line in lines:
            tabData = line.split( )
            if(tabData[0] == 'v'):
                id = tabData[1]
                coord = tabData[2]
                x,y = ast.literal_eval(coord)
                node = Node(id, x, y)
                features = self.parseFeatures(tabData[3])
                if(bool(features)):
                    for feature in features:
                        node.addFeature(feature[0], feature[1])

                nodes[node.getId()] = node
            if(tabData[0] == 'u'):
                node1 = tabData[1]
                node2 = tabData[2]
                edge = Edge(node1, node2)
                features = self.parseFeatures(tabData[3])
                for feature in features:
                    edge.addFeature(feature[0], feature[1])
                edges.append(edge)
        graph = Graph()
        graph.setListNode(nodes)
        graph.setListEdge(edges)
        return graph

    def parseFeatures(self, features):

        res = []
        if(features != '[]'):
            features = features.replace("[", "")
            features = features.replace("]", "")
            list_feature = features.split(",")
            for i in range(len(list_feature)):
                res.append(list_feature[i].split("="))
        return res

    def nodeToGraphFormat(self, node):
        coords = ' ('+ str(node.getX()) + ',' + str(node.getY()) + ') '
        features = '['
        for key,val in node.getFeatures().items():
            features = features + key + '=' + val + ','
        features = features[:-1] + ']'
        return 'v ' + node.getId() + coords + features + '\n'
    
    def edgeToGraphFormat(self, edge):
        features = '['
        for key,val in edge.getFeatures().items():
            features = features + key + '=' + val + ','
        features = features[:-1] + ']'
        return 'u ' + edge.getNodeA() + ' ' + edge.getNodeB () + ' ' + features + '\n'

    def setNodeToFile(self, node, filepath):
        graphFileReading = open(filepath,"r")
        lines = graphFileReading.readlines()
        graphFileReading.close()
        fileContent = ''
        graphFileWriting = open(filepath, "w")
        for line in lines:
                tokens = line.split()
                if tokens[0] == 'v' and tokens[1] == node.getId():
                    fileContent = fileContent + self.nodeToGraphFormat(node)
                else:
                    fileContent = fileContent + line
        graphFileWriting.write(fileContent)
        graphFileWriting.close()

    def setEdgeToFile(self, edge, filepath):
        graphFileReading = open(filepath,"r")
        lines = graphFileReading.readlines()
        graphFileReading.close()
        fileContent = ''
        for line in lines:
                tokens = line.split()
                if tokens[0] == 'u' and tokens[1] == edge.getNodeA() and tokens[2] == edge.getNodeB():
                    fileContent = fileContent + self.edgeToGraphFormat(edge)
                else:
                    fileContent = fileContent + line
        graphFileWriting = open(filepath, "w")
        graphFileWriting.write(fileContent)
        graphFileWriting.close()

def main():
    graph_reader = GraphReader()
    graph = graph_reader.read("testgen.graph")
    

if __name__ == "__main__":
    main()