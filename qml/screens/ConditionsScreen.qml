import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import EulerSolver
import ExtraConditionsModel
import "../views"

Rectangle {
    id: root

    required property var solver

    property string coefToolTip: "Введите коэффициенты в виде<br>∑a<sub>i</sub>x<sup>i</sup>y<sup>(i)</sup>"
    
    SplitView {
        anchors.fill: parent

        ColumnLayout {
            id: coefColumn
            SplitView.fillWidth: true
            SplitView.minimumWidth: implicitWidth

            Label {
                Layout.fillWidth: true
                Layout.margins: 7
                horizontalAlignment: Label.AlignHCenter
                text: "Коэффициенты в виде<br>∑a<sub>i</sub>x<sup>i</sup>y<sup>(i)</sup>"
            }
            FormulaView {
                Layout.fillWidth: true
                Layout.margins: 7
                Layout.topMargin: 0
                htmlFormula: root.solver.coefficientsModel.htmlFormula
            }
            CoefficientsView {
                id: coefficientsView
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.margins: 7
                Layout.topMargin: 0
                model: root.solver.coefficientsModel
            }
        }

        ColumnLayout {
            SplitView.fillWidth: true
            SplitView.minimumWidth: implicitWidth
            
            Label {
                Layout.fillWidth: true
                Layout.margins: 7
                horizontalAlignment: Label.AlignHCenter
                text: "Дополнительные условия<br>для первого решения"
            }
            ExtraConditionsView {
                id: firstExtraView
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.margins: 7
                Layout.topMargin: 0
                model: root.solver.firstConditionModel
            }
        }

        ColumnLayout {
            SplitView.fillWidth: true
            SplitView.minimumWidth: implicitWidth
            
            Label {
                Layout.fillWidth: true
                Layout.margins: 7
                horizontalAlignment: Label.AlignHCenter
                text: "Дополнительные условия<br>для второго решения"
            }
            ExtraConditionsView {
                id: secondExtraView
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.margins: 7
                Layout.topMargin: 0
                model: root.solver.secondConditionModel
            }
        }
    }
}