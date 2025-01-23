from PySide6.QtCore import (
    QAbstractListModel, QModelIndex, QObject, Qt,
    Slot, Signal, QByteArray, QEnum, QPointF
)
from PySide6.QtQml import QmlElement

from maths import ExtraCondition
from maths import printers

QML_IMPORT_NAME = "ExtraConditionsModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class ExtraConditionsModel(QAbstractListModel):

    conditionsChanged = Signal()

    QEnum(ExtraCondition.Type)

    TypeRole = Qt.ItemDataRole.UserRole + 1
    PointRole = TypeRole + 1
    OrderRole = PointRole + 1
    ConstantRole = OrderRole + 1
    HtmlRole = ConstantRole + 1

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._container: list[ExtraCondition] = []
        self.dataChanged.connect(self.conditionsChanged)
        self.rowsInserted.connect(self.conditionsChanged)
        self.rowsRemoved.connect(self.conditionsChanged)
        self.modelReset.connect(self.conditionsChanged)

    def container(self):
        return self._container.copy()

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._container)

    def roleNames(self):
        ret = super().roleNames()
        ret[ExtraConditionsModel.TypeRole] = QByteArray(b"type")
        ret[ExtraConditionsModel.PointRole] = QByteArray(b"point")
        ret[ExtraConditionsModel.OrderRole] = QByteArray(b"order")
        ret[ExtraConditionsModel.ConstantRole] = QByteArray(b"constant")
        ret[ExtraConditionsModel.HtmlRole] = QByteArray(b"html")
        return ret

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None

        if role == self.TypeRole:
            return self._container[index.row()].type.value
        if role == self.PointRole:
            return QPointF(
                self._container[index.row()].x,
                self._container[index.row()].y
            )
        if role == self.OrderRole:
            return self._container[index.row()].order
        if role == self.ConstantRole:
            return self._container[index.row()].constant
        if role == self.HtmlRole:
            match self._container[index.row()].type:
                case ExtraCondition.Type.Point:
                    return self.pointHtml(index)
                case ExtraCondition.Type.Derivative:
                    return self.derivativeHtml(index)
                case ExtraCondition.Type.Constant:
                    return self.constantHtml(index)

    def setData(self, index: QModelIndex, value, role: int):
        if not index.isValid():
            return False

        if role == self.TypeRole:
            self._container[index.row()].type = ExtraCondition.Type(value)
            self.dataChanged.emit(index, index)
            return True
        if role == self.PointRole:
            value: QPointF = value
            self._container[index.row()].x, \
                self._container[index.row()].y = value.toTuple()
            self.dataChanged.emit(index, index)
            return True
        if role == self.OrderRole:
            self._container[index.row()].order = int(value)
            self.dataChanged.emit(index, index)
            return True
        if role == self.ConstantRole:
            value = float(value)
            self._container[index.row()].constant = float(value)
            self.dataChanged.emit(index, index)
            return True

        return False

    @Slot(result=bool)
    def addNew(self):
        return self.insertRow(self.rowCount())

    @Slot(int, result=bool)
    def removeAt(self, row: int):
        return self.removeRow(row)

    @Slot(int, int)
    def moveItem(self, from_row: int, to_row: int):
        if 0 > from_row or from_row > self.rowCount() - 1 or \
                0 > to_row or to_row > self.rowCount() - 1:
            return False

        self.beginMoveRows(QModelIndex(), from_row, from_row, QModelIndex(),
                           to_row + 1 if to_row > from_row else to_row)
        self._container.insert(to_row, self._container.pop(from_row))
        self.endMoveRows()

        return True

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

        for i in range(count):
            self._container.insert(row, ExtraCondition(x=1, y=1))

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

    def pointHtml(self, index: QModelIndex):
        return printers.point_to_html(self._container[index.row()])

    def derivativeHtml(self, index: QModelIndex):
        return printers.derivative_to_html(self._container[index.row()])

    def constantHtml(self, index: QModelIndex):
        return printers.constant_to_html(self._container[index.row()])
