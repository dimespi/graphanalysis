import unittest
from edge import Edge
from node import Node

class testEdge(unittest.TestCase):

    """Test case utilisé pour tester les fonctions de la classe 'Edge'."""

    def test_init(self):
        """Test du __init__"""
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        edge = Edge(nodeA, nodeB)      
        self.assertIs(nodeA, edge.getNodeA())
        self.assertIs(nodeB, edge.getNodeB())
        self.assertFalse(edge.isDirected())
        self.assertFalse(edge.isDirectedA())
        self.assertFalse(edge.isDirectedB())
        self.assertEqual({}, edge.getFeatures())

    def test_setNodeA(self):
        """Test le fonctionnement de la fonction setNodeA()"""
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        edge = Edge(nodeA, nodeB)      
        nodeC = Node(3, 7, 20) 
        edge.setNodeA(nodeC)
        #test changement nodeA
        self.assertIs(nodeC, edge.getNodeA())

    def test_setNodeB(self):
        """Test le fonctionnement de la fonction setNodeB()"""
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        edge = Edge(nodeA, nodeB)      
        nodeC = Node(3, 7, 20) 
        edge.setNodeB(nodeC)
        #test changement nodeB
        self.assertIs(nodeC, edge.getNodeB())

    def test_setDirected(self):
        """Test le fonctionnement de la fonction setDirected()"""
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        edge = Edge(nodeA, nodeB)      
        edge.setDirected(True, True, True)
        #test changement dirrected
        self.assertTrue(edge.isDirected())
        self.assertTrue(edge.isDirectedA())
        self.assertTrue(edge.isDirectedB())


    def test_addFeature(self):
        """Test le fonctionnement de la fonctions addFeature"""
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        edge = Edge(nodeA, nodeB)       
        #test features vide      
        self.assertEqual({}, edge.getFeatures())
        edge.addFeature('test','value')
        #test ajout d'une feature
        self.assertIn('test', edge.getFeatures())
        #test contenue feature 'test
        self.assertEqual('value', edge.getFeature('test'))

    def test_removeFeature(self):
        """Test le fonctionnement de la fonctions removeFeature"""
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        edge = Edge(nodeA, nodeB)            
        #test features vide      
        self.assertEqual({}, edge.getFeatures())
        edge.addFeature('test1','value')
        #test ajout d'une feature
        self.assertIn('test1', edge.getFeatures())
        #test contenue feature 'test
        self.assertEqual('value', edge.getFeature('test1'))
        edge.addFeature('test2','value2')
        #test ajout nouvelle feature
        self.assertIn('test1', edge.getFeatures())
        self.assertIn('test2', edge.getFeatures())
        #test remove test1
        edge.removeFeature('test1')
        self.assertNotIn('test1', edge.getFeatures())
        #test remove test2
        edge.removeFeature('test2')
        self.assertNotIn('test2', edge.getFeatures())
        self.assertEqual({}, edge.getFeatures())
    
    def test_removeAllFeature(self):
        """Test le fonctionnement de la fonctions removeFeature"""
        nodeA = Node(1, 5, 10) 
        nodeB = Node(2, 6, 8) 
        edge = Edge(nodeA, nodeB)   
        #test features vide      
        self.assertEqual({}, edge.getFeatures())
        edge.addFeature('test1','value')
        #test ajout d'une feature
        self.assertIn('test1', edge.getFeatures())
        #test contenue feature 'test
        self.assertEqual('value', edge.getFeature('test1'))
        edge.addFeature('test2','value2')
        #test ajout nouvelle feature
        self.assertIn('test1', edge.getFeatures())
        self.assertIn('test2', edge.getFeatures())
        #test removeAll
        edge.removeAllFeatures()
        self.assertEqual({}, edge.getFeatures())
        
            

if __name__ == '__main__':
    unittest.main()
