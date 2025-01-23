import numpy as np
import numpy.polynomial as npp
from loguru import logger

from maths import Coefficient, ExtraCondition, SolutionResult, stirling_matrix


class EulerEquation:
    def __init__(self):
        self._equation_poly: npp.Polynomial = npp.Polynomial(0)
        self._first_conditions: list[ExtraCondition] = []
        self._second_conditions: list[ExtraCondition] = []
        self._first_point: tuple[float, float] = (0, 0)
        self._second_point: tuple[float, float] = (0, 0)
        self.reset()

    def reset(self):
        self._param_poly: npp.Polynomial | None = None
        self._param_roots: list[float] | None = None
        self._first_variadics = None
        self._second_variadics = None

    def setCoefficientList(self, coefficient_list: list[Coefficient]):
        self._equation_poly = self._coefficients_list_to_poly(coefficient_list)
        self.reset()

    def setFirstConditionList(self, condition_list: list[ExtraCondition]):
        self._first_conditions = condition_list
        self.reset()

    def setSecondConditionList(self, condition_list: list[ExtraCondition]):
        self._second_conditions = condition_list
        self.reset()

    def setFirstPoint(self, point: tuple[float, float]):
        self._first_point = point

    def setSecondPoint(self, point: tuple[float, float]):
        self._second_point = point

    def order(self) -> int:
        result = (self._equation_poly.degree()
                  if self.validate()
                  else 0)
        return result

    def validate(self) -> SolutionResult:
        result = SolutionResult()
        if not self._equation_poly.degree() > 0:
            result.reason = SolutionResult.InvalidEquation
            result.description = 'Введите уравнение'

        elif 0 in self._first_point:
            result.reason = SolutionResult.InvalidFirstPoint
            result.description = 'Первая точка расположена на оси'

        elif 0 in self._second_point:
            result.reason = SolutionResult.InvalidSecondPoint
            result.description = 'Вторая точка расположена на оси'
        return result

    def solutionResult(self) -> SolutionResult:
        return self.solve()

    def parametricCoefficientsList(self) -> list[Coefficient]:
        return self._poly_to_coefficients_list(
            self.parametricCoefficientsPoly())

    def parametricCoefficientsPoly(self) -> npp.Polynomial:
        if self.validate() != SolutionResult.InvalidEquation:
            return self._calculate_parametric_poly().copy()
        return npp.Polynomial(0)

    def _calculate_parametric_poly(self):
        if self._param_poly is None:
            self._param_poly = self._equation_to_parametric_poly(
                                self._equation_poly)
        return self._param_poly

    def parametricRoots(self) -> list[float]:
        if self.validate():
            return self._calculate_parametric_roots().copy()
        return []

    def parametricRootsBiggerThanOrder(self) -> list[float]:
        roots = self.parametricRoots()
        return [root for root in roots
                if root.real > self._param_poly.degree()]

    def _calculate_parametric_roots(self) -> list[float]:
        if self._param_roots is None and self._param_poly is not None:
            self._param_roots = self._param_poly.roots().tolist()
        return self._param_roots or []

    def firstVariadics(self) -> list[float]:
        self._calculate_variadics()
        return self._first_variadics.tolist() or []

    def secondVariadics(self) -> list[float]:
        self._calculate_variadics()
        return self._second_variadics.tolist() or []

    def _calculate_variadics(
            self,
            point: tuple[float, float] = None,
            conditions: list[ExtraCondition] = None):
        if point is None or conditions is None:
            if self._first_variadics is None:
                logger.debug("- Calculating first variadics")
                self._first_variadics = self._calculate_variadics(
                    self._first_point, self._first_conditions)
                logger.debug(f"- Calculated {self._first_variadics}")
            if self._second_variadics is None:
                logger.debug("- Calculating second variadics")
                self._second_variadics = self._calculate_variadics(
                    self._second_point, self._second_conditions)
                logger.debug(f"- Calculated {self._second_variadics}")
            return

        valid_roots = np.asarray(self.parametricRootsBiggerThanOrder())
        X = np.reshape(point[0] ** valid_roots, (1, -1))
        Y = np.asarray([point[1]])

        for cond in conditions:
            rank = np.linalg.matrix_rank(X)
            logger.debug(f"System [{' '.join(
                [str(r) for r in X])}] rank {rank}")
            if rank >= len(valid_roots):
                return np.linalg.lstsq(X, Y)[0].flatten()

            match cond.type:
                case ExtraCondition.Type.Derivative:
                    roots = valid_roots.copy()
                    coefs = np.ones(len(roots))
                    for n in range(cond.order):
                        coefs *= roots
                        roots -= 1
                    coefs *= point[0] ** roots
                    X = np.vstack((X, coefs))
                    Y = np.vstack((Y, [point[1]]))
                case ExtraCondition.Type.Point:
                    X = np.vstack((X, cond.x ** valid_roots))
                    Y = np.vstack((Y, [cond.y]))
                case ExtraCondition.Type.Constant:
                    x = np.zeros(len(valid_roots))
                    x[cond.order] = 1
                    X = np.vstack((X, x))
                    Y = np.vstack((Y, [cond.constant]))

        rank = np.linalg.matrix_rank(X)
        logger.debug(f"System [{' '.join([str(r) for r in X])}] rank {rank}")
        if rank >= len(valid_roots):
            return np.linalg.lstsq(X, Y)[0].flatten()
        return None

    def solve(self) -> SolutionResult:
        result = self.validate()
        if not result:
            return result

        self._calculate_parametric_poly()
        self._calculate_parametric_roots()

        valid_roots = self.parametricRootsBiggerThanOrder()
        logger.debug(f"Calculated valid roots {valid_roots}")
        if len(valid_roots) == 0:
            result.reason = SolutionResult.NoSolution
            result.description = '''Нет решения<br>
            Отсутствуют корни параметрического уравнения больше, \
                чем порядок уравнения'''
            return result

        self._calculate_variadics()
        if self._first_variadics is None:
            result.reason = SolutionResult.NoSolution
        elif self._second_variadics is None:
            result.reason = SolutionResult.NoSolution

        return result

    def calculateFirstSolution(
            self, left: float, right: float,
            n_points=1000) -> tuple[np.ndarray, np.ndarray]:

        if not self.solve():
            return [np.ndarray(0), np.ndarray(0)]

        xs = np.linspace(left, right, n_points)
        result = 0
        for var, root in zip(
                self._first_variadics, self.parametricRootsBiggerThanOrder()):
            result += var * (xs ** root)
        return xs, np.nan_to_num(result)

    def calculateSecondSolution(
            self, left: float, right: float,
            n_points=1000) -> tuple[np.ndarray, np.ndarray]:

        if not self.solve():
            return [np.ndarray(0), np.ndarray(0)]

        xs = np.linspace(left, right, n_points)
        result = 0
        for var, root in zip(
                self._second_variadics, self.parametricRootsBiggerThanOrder()):
            result += var * (xs ** root)
        return xs, np.nan_to_num(result)

    @staticmethod
    def _coefficients_list_to_poly(
            coef_list: list[Coefficient]) -> npp.Polynomial:
        if len(coef_list) == 0:
            return npp.Polynomial(0)
        result = np.zeros(max([coef.order for coef in coef_list]) + 1)
        for coef in coef_list:
            result[coef.order] = coef.value
        return npp.Polynomial(result).trim()

    @staticmethod
    def _poly_to_coefficients_list(
            poly: npp.Polynomial) -> list[Coefficient]:
        return [Coefficient(order, coef)
                for order, coef
                in enumerate(poly)]

    @staticmethod
    def _equation_to_parametric_poly(
            poly: npp.Polynomial) -> npp.Polynomial:
        return npp.Polynomial(
            np.dot(poly.coef, stirling_matrix(poly.degree()))
            )
