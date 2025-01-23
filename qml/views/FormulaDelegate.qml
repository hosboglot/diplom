import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    implicitWidth: row.implicitWidth
    implicitHeight: row.implicitHeight

    required property var model
    required property real value
    required property real order

    property bool isFirst: model.index === 0
    property bool isLast: model.index === ListView.view.count - 1

    Row {
        id: row
        anchors.fill: parent

        Label {
            id: signLabel
            text: root.value < 0 ? (root.isFirst ? "-" : "- ") :
                                   (root.isFirst ? "" : "+ ")
        }

        TextInput {
            id: coefField
            font.pointSize: 11.25
            
            validator: DoubleValidator { locale: "us" }
            color: acceptableInput ? "black" : "red"

            text: root.value
            onEditingFinished: root.model.value = text
            onFocusChanged: {
                if (text === "" && !focus) {
                    root.model.value = "0"
                }
            }
        }
    }
}