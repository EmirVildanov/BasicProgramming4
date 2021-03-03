from typing import List

from homework.hw1.task1.vector import Vector


class Matrix:
    def __init__(self, values: List[List[float]]):
        if len(values) == 0 or len(values[0]) == 0:
            raise ValueError("Matrix is empty or has empty row")
        if any([len(row) != len(values[0]) for row in values]):
            raise ValueError("Matrix rows must have the same length")
        self.values = values
        self.dimension = (len(values), len(values[0]))

    def __eq__(self, other: object):
        if isinstance(other, self.__class__):
            return self.values == other.values
        else:
            return False

    def transpose(self) -> "Matrix":
        return Matrix(
            [
                [self.values[j][i] for j in range(self.dimension[0])]
                for i in range(self.dimension[1])
            ]
        )

    def sum(self, matrix: "Matrix") -> "Matrix":
        return Matrix(
            [
                [
                    self.values[i][j] + matrix.values[i][j]
                    for j in range(self.dimension[1])
                ]
                for i in range(self.dimension[0])
            ]
        )

    def dot(self, matrix: "Matrix") -> "Matrix":
        if self.dimension[1] != matrix.dimension[0]:
            raise ValueError("These dimensions are incompatible for multiplication")
        return Matrix(
            [
                [
                    self_vector.dot(other_vector)
                    for other_vector in (
                        Vector([element for element in row])
                        for row in matrix.transpose().values
                    )
                ]
                for self_vector in (
                    Vector([element for element in row]) for row in self.values
                )
            ]
        )
