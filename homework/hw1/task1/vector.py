from math import sqrt, acos
from typing import List


class Vector:
    def __init__(self, coordinates: List[float]):
        self.coordinates = coordinates
        self.dimension = len(coordinates)

    def dot(self, vector: 'Vector') -> float:
        if vector.dimension != self.dimension:
            raise ValueError("Passed a vector of inappropriate length")
        return sum([vector.coordinates[i] * self.coordinates[i] for i in range(self.dimension)])

    def norm(self) -> float:
        return sqrt(self.dot(self))

    def angle(self, vector: 'Vector') -> float:
        return acos(self.dot(vector) / (self.norm() * vector.norm()))
