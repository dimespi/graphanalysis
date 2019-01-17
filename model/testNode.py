import unittest
from node import Node

class testNode(unittest.TestCase):

    """Test case utilisé pour tester les fonctions de la classe 'Graph'."""

    def test_init(self):
        """Test du __init__"""
        node = Node(1, 5, 10)        
        self.assertEqual(1, node.getId())
        self.assertEqual(5, node.getX())
        self.assertEqual(10, node.getY())
        self.assertEqual({}, node.getFeatures())

    def test_setX(self):
        """Test le fonctionnement de la fonction setX()"""
        node = Node(1, 5, 10)        
        node.setX(6)
        self.assertEqual(6, node.getX())

    def test_setY(self):
        """Test le fonctionnement de la fonction setY()"""
        node = Node(1, 5, 10)        
        node.setY(6)
        self.assertEqual(6, node.getY())

    def test_addFeature(self):
        """Test le fonctionnement de la fonctions addFeature"""
        node = Node(1, 5, 10)  
        #test features vide      
        self.assertEqual({}, node.getFeatures())
        node.addFeature('test','value')
        #test ajout d'une feature
        self.assertIn('test', node.getFeatures())
        #test contenue feature 'test
        self.assertEqual('value', node.getFeature('test'))

    def test_removeFeature(self):
        """Test le fonctionnement de la fonctions removeFeature"""
        node = Node(1, 5, 10)  
        #test features vide      
        self.assertEqual({}, node.getFeatures())
        node.addFeature('test1','value')
        #test ajout d'une feature
        self.assertIn('test1', node.getFeatures())
        #test contenue feature 'test
        self.assertEqual('value', node.getFeature('test1'))
        node.addFeature('test2','value2')
        #test ajout nouvelle feature
        self.assertIn('test1', node.getFeatures())
        self.assertIn('test2', node.getFeatures())
        #test remove test1
        node.removeFeature('test1')
        self.assertNotIn('test1', node.getFeatures())
        #test remove test2
        node.removeFeature('test2')
        self.assertNotIn('test2', node.getFeatures())
        self.assertEqual({}, node.getFeatures())
    
    def test_removeAllFeature(self):
        """Test le fonctionnement de la fonctions removeAllFeature"""
        node = Node(1, 5, 10)  
        #test features vide      
        self.assertEqual({}, node.getFeatures())
        node.addFeature('test1','value')
        #test ajout d'une feature
        self.assertIn('test1', node.getFeatures())
        #test contenue feature 'test
        self.assertEqual('value', node.getFeature('test1'))
        node.addFeature('test2','value2')
        #test ajout nouvelle feature
        self.assertIn('test1', node.getFeatures())
        self.assertIn('test2', node.getFeatures())
        #test removeAll
        node.removeAllFeatures()
        self.assertEqual({}, node.getFeatures())
        
            


        

if __name__ == '__main__':
    unittest.main()

