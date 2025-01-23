import QtQuick
import QtQuick.Controls

import CoefficientsModel

Rectangle {
    id: root
    implicitWidth: col.implicitWidth
    implicitHeight: col.implicitHeight

    required property var model
    required property real value
    required property real order
            
    Column {
        id: col
        anchors.fill: parent

        Item {
            implicitWidth: coefLabel.implicitWidth
            implicitHeight: childrenRect.height

            Label {
                id: coefLabel
                text: "a"
            }

            TextInput {
                id: orderField

                anchors.left: coefLabel.right
                y: coefLabel.y + coefLabel.height / 3
                font.underline: true

                text: root.order
                validator: OrderValidator {
                    bottom: 0
                    model: root.ListView.view.model
                    modelIndex: root.model.index
                }
                color: acceptableInput ? "black" : "red"
                onEditingFinished: root.model.order = text
            }

            Button {
                id: removeButton
                anchors.left: orderField.right
                anchors.leftMargin: 7
                anchors.verticalCenter: coefLabel.verticalCenter
                height: coefLabel.height / 1.5
                width: height

                onClicked: root.ListView.view.model.removeAt(root.model.index)

                background: Canvas {
                    anchors.fill: parent
                    anchors.margins: 2.5

                    antialiasing: true
                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.strokeStyle = "red";
                        ctx.moveTo(0, 0);
                        ctx.lineTo(width, height);
                        ctx.stroke();
                        ctx.moveTo(0, height);
                        ctx.lineTo(width, 0);
                        ctx.stroke();
                    }
                }
            }
        }

        TextField {
            id: valueField
            width: parent.width
            implicitWidth: coefTextMetrics.width
            
            placeholderText: "0"
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

        TextMetrics {
            id: coefTextMetrics
            text: "0.000000"
        }
    }
}