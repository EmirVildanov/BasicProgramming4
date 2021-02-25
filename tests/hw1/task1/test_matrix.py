import unittest
from math import pi

from homework.hw1.task1.matrix import Matrix


class MatrixTestCase(unittest.TestCase):
    def test_should_transpose_matrix(self):
        initial_matrix_values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        actual_matrix_values = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        self.assertEqual(Matrix(actual_matrix_values), Matrix(initial_matrix_values).transpose())

    def test_should_sum_two_matrices(self):
        first_matrix_values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        second_matrix_values = [[1, 1, 0], [5, 5, 5], [3, 3, 3]]
        actual_matrix_values = [[2, 3, 3], [9, 10, 11], [10, 11, 12]]
        self.assertEqual(Matrix(actual_matrix_values), Matrix(first_matrix_values).sum(Matrix(second_matrix_values)))

    def test_should_dot_two_matrices(self):
        first_matrix_values = [[1, 2], [4, 5]]
        second_matrix_values = [[1, 1], [5, 5]]
        actual_matrix_values = [[11, 11], [29, 29]]
        self.assertEqual(Matrix(actual_matrix_values), Matrix(first_matrix_values).dot(Matrix(second_matrix_values)))
