from dataclasses import dataclass
from enum import Enum

import numpy as np


@dataclass
class Coefficient:
    order: int
    value: float


@dataclass
class ExtraCondition:
    class Type(Enum):
        Point = 1
        Derivative = 2
        Constant = 3

    type: Type = Type.Point

    x: float = 0
    y: float = 0
    # derivative field
    order: int = 1
    # constant field
    constant: float = 1


@dataclass
class SolutionResult:
    Success = 0
    InvalidEquation = 1
    InvalidFirstPoint = 2
    InvalidSecondPoint = 3
    NoSolution = 4

    reason: int = Success
    description: str = ''

    @property
    def success(self):
        return self.reason == SolutionResult.Success

    def __bool__(self):
        return self.success


def stirling_matrix(order: int) -> np.ndarray:
    matrix = np.zeros((order + 1, order + 1)) + np.identity(order + 1)
    for m in range(2, order + 1):
        for k in range(1, m):
            matrix[m, k] = matrix[m - 1, k - 1] - (m - 1) * matrix[m - 1, k]
    return matrix
