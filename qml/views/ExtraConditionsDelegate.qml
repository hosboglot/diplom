import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import ExtraConditionsModel

Rectangle {
    id: root
    implicitWidth: col.implicitWidth
    implicitHeight: col.implicitHeight + col.anchors.margins * 2

    required property var model
    required property var type

    Rectangle {
        anchors.fill: parent
        border.color: "lightgray"
        border.width: 2
    }

    Column {
        id: col
        anchors.fill: parent
        anchors.margins: 5
        spacing: 3

        RowLayout {
            width: parent.width
            // implicitHeight: childrenRect.height

            ComboBox {
                id: typeComboBox
                Layout.fillWidth: true
                valueRole: "value"
                textRole: "text"
                model: [
                    { value: ExtraConditionsModel.Point, text: "Точка" },
                    { value: ExtraConditionsModel.Derivative, text: "Производная" },
                    { value: ExtraConditionsModel.Constant, text: "Константа" }
                ]
                Component.onCompleted: currentIndex = indexOfValue(root.type)
                currentIndex: indexOfValue(root.type)
                onActivated: root.model.type = currentValue
            }

            Column {
                Layout.preferredHeight: typeComboBox.height
                Layout.preferredWidth: Layout.preferredHeight

                Button {
                    width: parent.width
                    height: parent.height / 2

                    onClicked: root.ListView.view.model.moveItem(root.model.index, root.model.index - 1)

                    background: Canvas {
                        anchors.centerIn: parent
                        width: parent.width * 0.6
                        height: parent.height * 0.6
                        antialiasing: true
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.strokeStyle = "grey";
                            ctx.moveTo(0, height);
                            ctx.lineTo(width / 2, 0);
                            ctx.stroke();
                            ctx.lineTo(width, height);
                            ctx.stroke();
                        }
                    }
                }
                Button {
                    width: parent.width
                    height: parent.height / 2

                    onClicked: root.ListView.view.model.moveItem(root.model.index, root.model.index + 1)

                    background: Canvas {
                        anchors.centerIn: parent
                        width: parent.width * 0.6
                        height: parent.height * 0.6
                        antialiasing: true
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.strokeStyle = "grey";
                            ctx.moveTo(0, 0);
                            ctx.lineTo(width / 2, height);
                            ctx.stroke();
                            ctx.lineTo(width, 0);
                            ctx.stroke();
                        }
                    }
                }
            }
            Button {
                id: removeButton
                Layout.preferredHeight: typeComboBox.height
                Layout.preferredWidth: Layout.preferredHeight

                onClicked: root.ListView.view.model.removeAt(root.model.index)

                background: Canvas {
                    anchors.centerIn: parent
                    width: parent.width * 0.6
                    height: parent.height * 0.6
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

        Loader {
            id: delegateLoader
            width: parent.width

            property var model: root.model

            sourceComponent: switch (root.type) {
                case ExtraConditionsModel.Point: return pointFieldDelegate;
                case ExtraConditionsModel.Derivative: return derivativeFieldDelegate;
                case ExtraConditionsModel.Constant: return constantFieldDelegate;
                default: return;
            }
        }
    }

    Component {
        id: pointFieldDelegate
        Column {
            width: parent.width
            spacing: 3
            PointField {
                width: parent.width
                value: model.point
                onPointEdited: model.point = value
            }
            Label {
                textFormat: Label.RichText
                font.bold: true
                text: model.html
            }
        }
    }

    Component {
        id: derivativeFieldDelegate
        Column {
            width: parent.width
            spacing: 3
            Label {
                text: "Порядок производной"
            }
            TextField {
                width: parent.width
                validator: IntValidator {}
                color: acceptableInput ? "black" : "red"
                text: model.order
                onEditingFinished: if (acceptableInput) model.order = parseInt(text)
            }
            PointField {
                width: parent.width
                value: model.point
                onPointEdited: model.point = value
            }
            Label {
                textFormat: Label.RichText
                font.bold: true
                text: model.html
            }
        }
    }

    Component {
        id: constantFieldDelegate
        Column {
            width: parent.width
            spacing: 3
            Label {
                text: "Порядок"
            }
            TextField {
                width: parent.width
                validator: IntValidator {}
                color: acceptableInput ? "black" : "red"
                text: model.order
                onEditingFinished: if (acceptableInput) model.order = parseInt(text)
            }
            Label {
                text: "Значение"
            }
            TextField {
                width: parent.width
                validator: DoubleValidator { locale: "us" }
                color: acceptableInput ? "black" : "red"
                text: model.constant
                onEditingFinished: if (acceptableInput) model.constant = parseFloat(text)
            }
            Label {
                textFormat: Label.RichText
                font.bold: true
                text: model.html
            }
        }
    }
}