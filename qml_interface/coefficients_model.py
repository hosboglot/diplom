from PySide6.QtCore import (
    QAbstractListModel, QModelIndex, QObject, Qt,
    Slot, Signal, QByteArray, Property
)
from PySide6.QtGui import QIntValidator
from PySide6.QtQml import QmlElement

from maths import Coefficient
from maths import printers

QML_IMPORT_NAME = "CoefficientsModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class CoefficientsModel(QAbstractListModel):

    formulaChanged = Signal()

    OrderRole = Qt.ItemDataRole.UserRole + 1
    ValueRole = OrderRole + 1

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._container: list[Coefficient] = []
        self.dataChanged.connect(self.formulaChanged)
        self.rowsInserted.connect(self.formulaChanged)
        self.rowsRemoved.connect(self.formulaChanged)
        self.modelReset.connect(self.formulaChanged)

    def container(self):
        return self._container.copy()

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._container)

    def roleNames(self):
        ret = super().roleNames()
        ret[CoefficientsModel.OrderRole] = QByteArray(b"order")
        ret[CoefficientsModel.ValueRole] = QByteArray(b"value")
        return ret

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None

        if role == self.ValueRole:
            return self._container[index.row()].value
        if role == self.OrderRole:
            return self._container[index.row()].order

    def setData(self, index: QModelIndex, value, role: int):
        if not index.isValid():
            return False

        if role == self.ValueRole:
            value = float(value)
            self._container[index.row()].value = float(value)
            self.dataChanged.emit(index, index)
            return True
        if role == self.OrderRole:
            if (value := int(value)) not in \
                    [i.order for i in self._container]:
                self._container[index.row()].order = value
                self.dataChanged.emit(index, index)
                return True

        return False

    @Slot(result=bool)
    def addNew(self):
        return self.insertRow(self.rowCount())

    @Slot(int, result=bool)
    def removeAt(self, row: int):
        return self.removeRow(row)

    def resetModel(self, data: list | None = None):
        if data is None:
            data = list()

        self.beginResetModel()
        self._container = data
        self.endResetModel()

        return True

    def insertRows(self, row: int, count: int, parent=QModelIndex()):
        if parent.isValid():
            return False

        self.beginInsertRows(parent, row, row + count - 1)

        maxIndex = max([i.order for i in self._container] or (-1,)) + 1
        for i in range(count):
            self._container.insert(row, Coefficient(maxIndex, 0))
            maxIndex += 1

        self.endInsertRows()

        return True

    def removeRows(self, row: int, count: int, parent=QModelIndex()):
        if parent.isValid():
            return False

        self.beginRemoveRows(parent, row, row + count - 1)
        self._container = self._container[:row] + \
            self._container[row + count:]
        self.endRemoveRows()

        return True

    @Property(str, notify=formulaChanged)
    def htmlFormula(self):
        return printers.coefficients_to_html(self.container())


@QmlElement
class OrderValidator(QIntValidator):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model: CoefficientsModel = None
        self._modelIndex = 0

    modelChanged = Signal(CoefficientsModel)

    @Property(CoefficientsModel, notify=modelChanged)
    def model(self):
        return self._model

    @model.setter
    def model(self, model: CoefficientsModel):
        if isinstance(model, CoefficientsModel):
            self._model = model
            self.modelChanged.emit(self._model)

    modelIndexChanged = Signal(int)

    @Property(int, notify=modelIndexChanged)
    def modelIndex(self):
        return self._modelIndex

    @modelIndex.setter
    def modelIndex(self, modelIndex: int):
        self._modelIndex = modelIndex
        self.modelIndexChanged.emit(self._modelIndex)

    def validate(self, arg__1, arg__2):
        result = super().validate(arg__1, arg__2)

        if self._model is None:
            return (QIntValidator.State.Invalid,) + result[1:]

        if result[0] == QIntValidator.State.Acceptable and \
                int(result[1]) in [
                    i.order for n, i in enumerate(self._model.container())
                    if self._modelIndex != n]:
            result = (QIntValidator.State.Intermediate,) + result[1:]

        return result
