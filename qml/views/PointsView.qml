import QtQuick

Item {
    id: root
    implicitWidth: col.implicitWidth
    implicitHeight: col.implicitHeight

    property alias firstPoint: firstPointField.value
    signal firstPointEdited()
    property alias secondPoint: secondPointField.value
    signal secondPointEdited()

    Column {
        id: col
        anchors.fill: parent

        PointField {
            id: firstPointField
            width: parent.width
            labelText: "Первая точка"
            onPointEdited: root.firstPointEdited()
        }
        PointField {
            id: secondPointField
            width: parent.width
            labelText: "Вторая точка"
            onPointEdited: root.secondPointEdited()
        }
    }
}