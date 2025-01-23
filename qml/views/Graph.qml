pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls
import QtGraphs

Item {
    id: root
    implicitWidth: view.implicitWidth
    implicitHeight: view.implicitHeight
    
    property alias minX: valueAxisX.min
    property alias maxX: valueAxisX.max
    signal moved()

    required property point firstPoint
    required property point secondPoint
    property alias firstSolution: firstSolutionSeries.points
    property alias secondSolution: secondSolutionSeries.points

    GraphsView {
        id: view
        anchors.fill: parent
        theme: GraphsTheme {
            backgroundVisible: false
            colorScheme: GraphsTheme.Light  // qmllint disable
        }
        axisX: ValueAxis {
            id: valueAxisX
            onMinChanged: root.moved()
            onMaxChanged: root.moved()
            min: -10
            max: 10
        }
        axisY: ValueAxis {
            id: valueAxisY
            min: -10
            max: 10
        }

        ScatterSeries {
            pointDelegate: Rectangle {
                property bool pointSelected
                property color pointColor
                property real pointValueX
                property real pointValueY
                property bool isValid: pointValueX != 0 && pointValueY != 0

                width: Math.min(root.width, root.height) / 30
                height: width
                radius: width / 2
                color: isValid ? "blue" : "red"
            }
            property list<point> points: [root.firstPoint, root.secondPoint]
            onPointsChanged: {
                clear();
                append(points);
            }
        }
        LineSeries {
            id: firstSolutionSeries
            color: "blue"
            property list<point> points: []
            onPointsChanged: {
                console.log("updated 1");
                clear();
                append(points);
            }
        }
        LineSeries {
            id: secondSolutionSeries
            color: "green"
            property list<point> points: []
            onPointsChanged: {
                console.log("updated 2");
                clear();
                append(points);
            }
        }
    }
}