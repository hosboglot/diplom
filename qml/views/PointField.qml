import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    implicitWidth: col.implicitWidth
    implicitHeight: col.implicitHeight

    property alias labelText: pointLabel.text
    property point value

    signal pointEdited()
    property bool acceptableInput: xField.acceptableInput && yField.acceptableInput

    function checkValidity() {
        if (xField.acceptableInput) {
            root.value.x = parseFloat(xField.text);
        }
        if (yField.acceptableInput) {
            root.value.y = parseFloat(yField.text);
        }
        if (xField.acceptableInput && yField.acceptableInput) {
            pointEdited();
        }
    }

    Column {
        id: col
        width: parent.width
        Label {
            id: pointLabel
            height: visible ? implicitHeight : 0
            visible: text != ""
        }

        RowLayout {
            id: inputLayout
            width: parent.width // bad idea, use layout
            spacing: 5
            Label {
                text: "x"
            }
            TextField {
                id: xField
                Layout.fillWidth: true
                placeholderText: "x"
                validator: DoubleValidator {
                    locale: "us"
                }
                color: acceptableInput ? "black" : "red"
                text: root.value.x
                onEditingFinished: root.checkValidity()
            }
            Label {
                text: "y"
            }
            TextField {
                id: yField
                Layout.fillWidth: true
                placeholderText: "y"
                validator: DoubleValidator {
                    locale: "us"
                }
                color: acceptableInput ? "black" : "red"
                text: root.value.y
                onEditingFinished: root.checkValidity()
            }
        }
    }

    TextMetrics {
        id: pointValueTextMetrics
        text: "0.0000"
    }
}
