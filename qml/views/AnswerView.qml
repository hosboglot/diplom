import QtQuick
import QtQuick.Controls

Item {
    implicitWidth: fontMetrics.averageCharacterWidth * 100
    implicitHeight: fontMetrics.lineSpacing * 4 + textArea.topPadding + textArea.bottomPadding

    property alias text: textArea.text

    TextArea {
        id: textArea
        anchors.fill: parent
        textMargin: 5
        readOnly: true
        textFormat: TextArea.RichText
        text: ""
        wrapMode: TextArea.WordWrap
    }

    FontMetrics {
        id: fontMetrics
    }
}