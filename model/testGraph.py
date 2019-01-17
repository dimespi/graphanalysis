import unittest
from node import Node
from edge import Edge
from graph import Graph

class testNode(unittest.TestCase):

    """Test case utilisé pour tester les fonctions de la classe 'Graph'."""

    def test_init(self):
        """Test du __init__"""
        graph = Graph()        
        self.assertEqual({}, graph.getListNode())
        self.assertEqual([], graph.getListEdge())

    def test_setListNode(self):
        """Test le fonctionnement de la fonction setListNode()"""
        graph = Graph()        
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        listNode = {}
        listNode[nodeA.getId()] = nodeA
        listNode[nodeB.getId()] = nodeB
        graph.setListNode(listNode)
        #test changement listNode
        self.assertIs(listNode, graph.getListNode())
    
    def test_setListEdge(self):
        """Test le fonctionnement de la fonction setListEdge()"""
        graph = Graph()        
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        edge1 = Edge(nodeA, nodeB)
        edge2 = Edge(nodeB, nodeA)
        listEdge = []
        listEdge.append(edge1)
        listEdge.append(edge2)
        graph.setListEdge(listEdge)
        #test changement listEdge
        self.assertIs(listEdge, graph.getListEdge())


    

        

if __name__ == '__main__':
    unittest.main()

