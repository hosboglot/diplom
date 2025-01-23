import QtQuick
import QtQuick.Layouts

import EulerSolver
import "../views"


Rectangle {
    id: root

    required property var solver

    Connections {
        target: root.solver
        function onSolutionReady() {
            graph.updateSolution();
        }
        function onSolutionFail() {
            graph.updateSolution();
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 7
        spacing: 5

        FormulaView {
            id: equationFormulaView
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: implicitWidth
            Layout.preferredHeight: implicitHeight
            name: "Исходное уравнение"
            htmlFormula: root.solver.coefficientsModel.htmlFormula
        }

        FormulaView {
            id: parametricFormulaView
            Layout.alignment: Qt.AlignHCenter
            Layout.minimumWidth: implicitWidth
            Layout.minimumHeight: implicitHeight
            name: "Параметрическое уравнение"
            htmlFormula: root.solver.parametricHtml
        }

        Graph {
            id: graph
            Layout.fillWidth: true
            Layout.fillHeight: true

            onMoved: updateSolution()
            function updateSolution() {
                firstSolution = root.solver.calculateFirstSolution(minX, maxX);
                secondSolution = root.solver.calculateSecondSolution(minX, maxX);
            }

            firstPoint: root.solver.firstPoint
            secondPoint: root.solver.secondPoint
        }

        RowLayout {
            Layout.preferredHeight: answerView.implicitHeight
            spacing: 7

            PointsView {
                id: pointsView
                Layout.minimumWidth: root.width / 4
                firstPoint: solver.firstPoint
                onFirstPointEdited: solver.firstPoint = firstPoint
                secondPoint: solver.secondPoint
                onSecondPointEdited: solver.secondPoint = secondPoint
            }

            AnswerView {
                id: answerView
                Layout.preferredHeight: pointsView.height
                Layout.fillWidth: true
                text: root.solver.resultHtml
            }
        }
    }
}