from typing import List


class Matrix:
    def __init__(self, values: List[List[float]]):
        if len(values) == 0 or len(values[0]) == 0:
            raise ValueError("Matrix is empty or has empty row")
        for index in range(1, len(values)):
            if len(values[index]) != len(values[index - 1]):
                raise ValueError("Matrix rows must have the same length")
        self.values = values
        self.dimension = (len(values), len(values[0]))

    def __eq__(self, other: object):
        if isinstance(other, self.__class__):
            if self.dimension != other.dimension:
                return False
            return self.values == other.values
        else:
            return False

    def transpose(self) -> "Matrix":
        new_values = []
        for i in range(self.dimension[0]):
            current_row = [self.values[j][i] for j in range(self.dimension[1])]
            new_values.append(current_row)
        return Matrix(new_values)

    def sum(self, matrix: "Matrix") -> "Matrix":
        new_values = []
        for i in range(self.dimension[0]):
            current_row = [self.values[i][j] + matrix.values[i][j] for j in range(self.dimension[1])]
            new_values.append(current_row)
        return Matrix(new_values)

    def dot(self, matrix: "Matrix") -> "Matrix":
        if self.dimension[1] != matrix.dimension[0]:
            raise ValueError("Matrix have different dimensions")
        new_values = []
        for i in range(self.dimension[0]):
            current_row = []
            for k in range(matrix.dimension[1]):
                current_row.append(sum([self.values[i][j] * matrix.values[j][k] for j in range(self.dimension[1])]))
            new_values.append(current_row)
        return Matrix(new_values)
