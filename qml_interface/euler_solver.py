from PySide6.QtCore import (
    QObject, QPointF,
    Slot, Signal, Property
)
from PySide6.QtQml import QmlElement

from maths import Coefficient, SolutionResult
from maths.euler_equation import EulerEquation
import maths.printers as printer
from qml_interface.coefficients_model import CoefficientsModel
from qml_interface.extra_conditions_model import ExtraConditionsModel

QML_IMPORT_NAME = "EulerSolver"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class EulerSolver(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._first_point = QPointF()
        self._second_point = QPointF()

        self._equation: EulerEquation | None = None
        self._coefficients_model: CoefficientsModel | None = None
        self._first_cond_model: ExtraConditionsModel | None = None
        self._second_cond_model: ExtraConditionsModel | None = None

        self.coefficientsModel = CoefficientsModel(self)
        self.coefficientsModel.resetModel([
            Coefficient(0, -2),
            Coefficient(1, 1)
        ])
        self.firstConditionModel = ExtraConditionsModel(self)
        self.secondConditionModel = ExtraConditionsModel(self)

        self.coefficientsModelChanged.connect(self.parametersChanged)
        self.coefficientsModelChanged.connect(self.parametricEquationChanged)
        self.firstPointChanged.connect(self.parametersChanged)
        self.secondPointChanged.connect(self.parametersChanged)
        self.firstConditionModelChanged.connect(self.parametersChanged)
        self.secondConditionModelChanged.connect(self.parametersChanged)
        self.parametersChanged.connect(self.trySolve)

        self.solutionReady.connect(self.resultChanged)
        self.solutionFail.connect(self.resultChanged)

    parametersChanged = Signal()

    coefficientsModelChanged = Signal(CoefficientsModel)

    @Property(CoefficientsModel, notify=coefficientsModelChanged)
    def coefficientsModel(self):
        return self._coefficients_model

    @coefficientsModel.setter
    def coefficientsModel(self, new: CoefficientsModel):
        if self._coefficients_model != new:
            if self._coefficients_model is not None:
                self._coefficients_model \
                    .formulaChanged.disconnect(self.parametersChanged)
                self._coefficients_model \
                    .formulaChanged.disconnect(self.parametricEquationChanged)

            self._coefficients_model = new
            self._coefficients_model \
                .formulaChanged.connect(self.parametersChanged)
            self._coefficients_model \
                .formulaChanged.connect(self.parametricEquationChanged)

            self.coefficientsModelChanged.emit(new)

    firstConditionModelChanged = Signal(ExtraConditionsModel)

    @Property(ExtraConditionsModel, notify=firstConditionModelChanged)
    def firstConditionModel(self):
        return self._first_cond_model

    @firstConditionModel.setter
    def firstConditionModel(self, new):
        if self._first_cond_model != new:
            if self._first_cond_model is not None:
                self._first_cond_model \
                    .conditionsChanged.disconnect(self.parametersChanged)

            self._first_cond_model = new
            self._first_cond_model \
                .conditionsChanged.connect(self.parametersChanged)

            self.firstConditionModelChanged.emit(new)

    secondConditionModelChanged = Signal(ExtraConditionsModel)

    @Property(ExtraConditionsModel, notify=secondConditionModelChanged)
    def secondConditionModel(self):
        return self._second_cond_model

    @secondConditionModel.setter
    def secondConditionModel(self, new):
        if self._second_cond_model != new:
            if self._second_cond_model is not None:
                self._second_cond_model \
                    .conditionsChanged.disconnect(self.parametersChanged)

            self._second_cond_model = new
            self._second_cond_model \
                .conditionsChanged.connect(self.parametersChanged)

            self.secondConditionModelChanged.emit(new)

    firstPointChanged = Signal(QPointF)

    @Property(QPointF, notify=firstPointChanged)
    def firstPoint(self):
        return self._first_point

    @firstPoint.setter
    def firstPoint(self, val: QPointF):
        if self._first_point != val:
            self._first_point = val
            self.firstPointChanged.emit(val)

    secondPointChanged = Signal(QPointF)

    @Property(QPointF, notify=secondPointChanged)
    def secondPoint(self):
        return self._second_point

    @secondPoint.setter
    def secondPoint(self, val: QPointF):
        if self._second_point != val:
            self._second_point = val
            self.secondPointChanged.emit(val)

    parametricEquationChanged = Signal(list[Coefficient])
    solutionReady = Signal()
    solutionFail = Signal()
    resultChanged = Signal()

    @Property(str, notify=solutionReady)
    def solutionHtml(self):
        if self._equation is None:
            return ''
        return printer.solution_to_html(self._equation)

    @Property(str, notify=solutionFail)
    def failReasonHtml(self):
        if self._equation is None:
            return ''
        return self._equation.solutionResult().description

    @Property(str, notify=resultChanged)
    def resultHtml(self):
        if self._equation is None:
            return ''
        result = self._equation.solutionResult()
        if result:
            return printer.solution_to_html(self._equation)
        else:
            return result.description

    @Property(str, notify=parametricEquationChanged)
    def parametricHtml(self):
        if self._equation is None:
            return '0 = 0'
        return printer.parametric_to_html(self._equation)

    @Slot()
    def trySolve(self):
        self._equation = EulerEquation()

        self._equation.setCoefficientList(self._coefficients_model.container())
        self._equation.setFirstConditionList(
            self._first_cond_model.container())
        self._equation.setSecondConditionList(
            self._second_cond_model.container())
        self._equation.setFirstPoint(self._first_point.toTuple())
        self._equation.setSecondPoint(self._second_point.toTuple())

        result = self._equation.solve()

        self._processSolution(result)

    @Slot(float, float, result=list)
    def calculateFirstSolution(self, left: float, right: float):
        xs, ys = self._equation.calculateFirstSolution(left, right)
        result = []
        for x, y in zip(xs, ys):
            result.append(QPointF(x, y))
        return result

    @Slot(float, float, result=list)
    def calculateSecondSolution(self, left: float, right: float):
        xs, ys = self._equation.calculateSecondSolution(left, right)
        result = []
        for x, y in zip(xs, ys):
            result.append(QPointF(x, y))
        return result

    @Slot(str)
    def _processSolution(self, result: SolutionResult):
        if result:
            self.solutionReady.emit()
        else:
            self.solutionFail.emit()
