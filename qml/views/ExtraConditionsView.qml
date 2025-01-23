import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import ExtraConditionsModel

Rectangle {
    id: root
    implicitWidth: addCoefButton.width

    property alias model: view.model
    property alias currentIndex: view.currentIndex

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        ListView {
            id: view
            Layout.fillHeight: true
            Layout.fillWidth: true

            ScrollBar.vertical: ScrollBar { width: 7 }
            // boundsBehavior: Flickable.StopAtBounds

            spacing: 7
            focus: true
            clip: true
            delegate: ExtraConditionsDelegate {
                width: ListView.view.width
            }
        }

        Button {
            id: addCoefButton
            Layout.alignment: Qt.AlignHCenter

            text: "Добавить"
            onClicked: view.model.addNew()
        }
    }
}
