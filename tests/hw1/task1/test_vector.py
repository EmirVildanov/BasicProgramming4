import unittest
from math import pi

from homework.hw1.task1.vector import Vector


class VectorTestCase(unittest.TestCase):
    def test_should_dot_two_vectors(self):
        self.assertEqual(1, Vector([1, 1, 1]).dot(Vector([0, 0, 1])))

    def test_should_norm_vector(self):
        self.assertEqual(5, Vector([4, 3, 0]).norm())

    def test_should_find_angle_between_two_vectors(self):
        self.assertEqual(pi / 2, Vector([1, 0, 0]).angle(Vector([0, 1, 0])))
