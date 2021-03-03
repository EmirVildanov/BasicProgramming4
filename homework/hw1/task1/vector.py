from math import sqrt, acos
from typing import List


class Vector:
    def __init__(self, coordinates: List[float]):
        self.coordinates = coordinates
        self.dimension = len(coordinates)

    def dot(self, vector: "Vector") -> float:
        if vector.dimension != self.dimension:
            raise ValueError("Passed a vector of inappropriate length")
        return sum(x * y for x, y in zip(self.coordinates, vector.coordinates))

    def norm(self) -> float:
        return sqrt(self.dot(self))

    def angle(self, vector: "Vector") -> float:
        return acos(self.dot(vector) / (self.norm() * vector.norm()))
