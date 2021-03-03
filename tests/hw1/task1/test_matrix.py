import unittest

from homework.hw1.task1.matrix import Matrix


class MatrixTestCase(unittest.TestCase):
    def test_should_raise_error_when_creating_matrix_consisting_of_rows_of_different_length(
        self,
    ):
        with self.assertRaises(ValueError) as context:
            Matrix([[1, 1, 1], [1, 1]])

        self.assertTrue(
            "Matrix rows must have the same length" in str(context.exception)
        )

    def test_should_raise_error_when_creating_empty_matrix(
        self,
    ):
        with self.assertRaises(ValueError) as context:
            Matrix([])

        self.assertTrue("Matrix is empty or has empty row" in str(context.exception))

    def test_should_raise_error_when_creating_matrix_with_empty_row(
        self,
    ):
        with self.assertRaises(ValueError) as context:
            Matrix([[], [1, 2, 3]])

        self.assertTrue("Matrix is empty or has empty row" in str(context.exception))

    def test_should_raise_error_when_dot_matrices_of_different_dimensions(self):
        matrix1 = Matrix([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]])
        matrix2 = Matrix([[5, 5, 5, 5], [6, 6, 6, 6]])
        with self.assertRaises(ValueError) as context:
            matrix1.dot(matrix2)

        self.assertTrue(
            "These dimensions are incompatible for multiplication"
            in str(context.exception)
        )

    def test_should_transpose_matrix(self):
        initial_matrix_values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        actual_matrix_values = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        self.assertEqual(
            Matrix(actual_matrix_values), Matrix(initial_matrix_values).transpose()
        )

    def test_should_transpose_matrix_2x3(self):
        initial_matrix_values = [[1, 2, 3], [4, 5, 6]]
        actual_matrix_values = [[1, 4], [2, 5], [3, 6]]
        self.assertEqual(
            Matrix(actual_matrix_values), Matrix(initial_matrix_values).transpose()
        )

    def test_should_sum_two_matrices(self):
        first_matrix_values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        second_matrix_values = [[1, 1, 0], [5, 5, 5], [3, 3, 3]]
        actual_matrix_values = [[2, 3, 3], [9, 10, 11], [10, 11, 12]]
        self.assertEqual(
            Matrix(actual_matrix_values),
            Matrix(first_matrix_values).sum(Matrix(second_matrix_values)),
        )

    def test_should_dot_two_matrices_2x2(self):
        first_matrix_values = [[1, 2], [4, 5]]
        second_matrix_values = [[1, 1], [5, 5]]
        actual_matrix_values = [[11, 11], [29, 29]]
        self.assertEqual(
            Matrix(actual_matrix_values),
            Matrix(first_matrix_values).dot(Matrix(second_matrix_values)),
        )

    def test_should_dot_two_matrices_2x3_and_3x4(self):
        first_matrix_values = [[1, 2, 3], [4, 5, 6]]
        second_matrix_values = [[1, 1, 0, 1], [1, 0, 0, 0], [0, 1, 0, 1]]
        actual_matrix_values = [[3, 4, 0, 4], [9, 10, 0, 10]]
        self.assertEqual(
            Matrix(actual_matrix_values),
            Matrix(first_matrix_values).dot(Matrix(second_matrix_values)),
        )
