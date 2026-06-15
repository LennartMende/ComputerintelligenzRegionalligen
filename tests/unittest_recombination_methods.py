import unittest

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.Population import Population


class TestCrossover(unittest.TestCase):

    def setUp(self):
        self.pop = Population(pop_size=0)

    def test_ox(self):

        parent1 = [1,2,3,4,5,6,7,8]
        parent2 = [4,1,2,8,7,6,5,3]

        cut1 = 3
        cut2 = 5

        child1, child2 = self.pop.ox(parent1, parent2, cut1=cut1, cut2=cut2)

        # zu erwartendes Ergebnis vorgeben
        expected_child1 = [1,2,3,4,5,8,7,6]
        expected_child2 = [1,3,2,8,7,4,5,6]

        self.assertEqual(child1, expected_child1)
        self.assertEqual(child2, expected_child2)

    def test_ox_large(self):

        parent1 = list(range(1, 21))
        parent2 = list(reversed(parent1))

        # Crossover Punkte
        cut1 = 5
        cut2 = 12

        child1, child2 = self.pop.ox(parent1, parent2, cut1=cut1, cut2=cut2)

        # zu erwartendes Ergebnis vorgeben
        expected_child1 = [20,19,18,17,5,6,7,8,9,10,11,12,16,15,14,13,4,3,2,1]
        expected_child2 = [1,2,3,4,16,15,14,13,12,11,10,9,5,6,7,8,17,18,19,20]

        # Segment prüfen (wichtigster OX-Test!)
        self.assertEqual(child1, expected_child1)
        self.assertEqual(child2, expected_child2)

    def test_pmx(self):
    
        parent1 = [1,2,3,4,5,6,7,8]
        parent2 = [5,7,2,1,8,4,3,6]

        cut1 = 3
        cut2 = 6

        child1, child2 = self.pop.pmx(parent1, parent2, cut1=cut1, cut2=cut2)

        # zu erwartendes Ergebnis vorgeben
        expected_child1 = [8,7,3,4,5,6,2,1]
        expected_child2 = [6,3,2,1,8,4,7,5]

        self.assertEqual(child1, expected_child1)
        self.assertEqual(child2, expected_child2)



if __name__ == '__main__':
    unittest.main()
