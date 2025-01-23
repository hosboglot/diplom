import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    implicitWidth: col.implicitWidth
    implicitHeight: col.implicitHeight

    property alias htmlFormula: formulaLabel.text
    property alias name: nameLabel.text

    FontMetrics {
        id: fontMetrics
    }

    Column {
        id: col
        width: parent.width
        Label {
            id: nameLabel
            anchors.horizontalCenter: parent.horizontalCenter
            visible: text != ""
            text: ""
        }
        Label {
            id: formulaLabel
            anchors.horizontalCenter: parent.horizontalCenter
            // text: root.model.htmlFormula
            textFormat: Label.RichText
        }
    }

    // INTERACTIVE
    // implicitHeight: fontMetrics.height * 5 / 3
    // ListView {
    //     id: lv
    //     anchors.fill: parent

    //     ScrollBar.horizontal: ScrollBar { height: 7 }
    //     boundsBehavior: Flickable.StopAtBounds

    //     orientation: Qt.Horizontal
    //     focus: true
    //     clip: true
    //     delegate: FormulaDelegate {}
    // }
}