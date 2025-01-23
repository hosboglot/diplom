pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

import EulerSolver
import "screens"

ApplicationWindow {
    id: root
    width: 640
    height: 640
    visible: true
    title: qsTr("Euler Equations")
    minimumWidth: 640
    minimumHeight: 640

    EulerSolver {  // qmllint disable
        id: solver
    }

    header: TabBar {
        id: tabBar

        Repeater {
            model: ["График", "Условия"]

            TabButton {
                required property string modelData
                text: modelData
            }
        }
    }

    StackLayout {
        id: stackView
        anchors.fill: parent
        currentIndex: tabBar.currentIndex

        PlotScreen {
            solver: solver
        }

        ConditionsScreen {
            solver: solver
        }
    }
}
