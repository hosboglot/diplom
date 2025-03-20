import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters

# y = C1*x^2 + C2*x^3
A = (-3, 1)
B = (-2, 2)
C = (2, 1.5)
C3s = [0, -1, -0.5]

C2 = (A[0]**2 * B[1] - A[1] * B[0]**2) / (A[0]**2 * B[0]**2 * (B[0] - A[0]))
C1 = (A[1] - C2*A[0]**3) / A[0]**2
left_f = lambda x: C1*x**2 + C2*x**3
right_f = lambda x, C3: ((C[1] - C3*C[0]**3) / C[0]**2)*x**2 + C3*x**3

app = pg.mkQApp()
pg.setConfigOption('background', 'w')  # Устанавливаем светлую тему
pg.setConfigOption('foreground', 'k')

class Plotter:
    def __init__(self):
        self.left, self.right = -4, 4
        self.down, self.up = -5, 5
        self.step = 0.02

        self.x_range_left = np.hstack((np.arange(self.left, 0, self.step), [0]))
        self.x_range_right = np.arange(0, self.right, self.step)
        self.x_range = np.hstack((self.x_range_left, self.x_range_right))
        
        self.left_printed = False
        self.right_printed = [False for _ in range(len(C3s))]
        self.i = 0
        self.I = 0

        self.plot = pg.plot()
        colors = ['c', 'g', 'b', 'r']  # Разные цвета для графиков

        for i in range(1 + len(C3s)):
            self.plot.plot(pen=pg.mkPen(colors[i], width=3))
            self.plot.plot([0], [0], pen=None, symbol='o')

        self.plot.showGrid(x=True, y=True)
        self.plot.setXRange(self.left, self.right)
        self.plot.setYRange(self.down, self.up)
        
        # Добавляем статичные точки A, B, C
        self.plot.plot([A[0]], [A[1]], pen=None, symbol='o', symbolBrush='k')
        self.plot.plot([B[0]], [B[1]], pen=None, symbol='o', symbolBrush='k')
        self.plot.plot([C[0]], [C[1]], pen=None, symbol='o', symbolBrush='k')

    def update(self):
        if not self.left_printed:
            self.plot.plotItem.dataItems[0].setData(
                self.x_range_left[:self.i],
                left_f(self.x_range_left[:self.i])
            )
            self.plot.plotItem.dataItems[1].setData(
                [self.x_range_left[self.i]],
                [left_f(self.x_range_left[self.i])]
            )
            if self.i + 1 == len(self.x_range_left):
                self.left_printed = True
                self.i = 0
        else:
            self.plot.plotItem.dataItems[0].setData(
                self.x_range_left,
                left_f(self.x_range_left)
            )
        
            for i in range(len(C3s)):
                if not self.right_printed[i]:
                    self.plot.plotItem.dataItems[2 + 2*i].setData(
                        self.x_range_right[:self.i],
                        right_f(self.x_range_right[:self.i], C3s[i])
                    )
                    self.plot.plotItem.dataItems[2 + 2*i + 1].setData(
                        [self.x_range_right[self.i]],
                        [right_f(self.x_range_right[self.i], C3s[i])],
                        pen=None, symbol='o'
                    )
                    if self.i + 1 == len(self.x_range_right):
                        self.right_printed[i] = True
                        # self.i = 0
                    # break
                else:
                    self.plot.plotItem.dataItems[2 + 2*i].setData(
                        self.x_range_right,
                        right_f(self.x_range_right, C3s[i])
                    )
        # exporter = pyqtgraph.exporters.ImageExporter(self.plot.plotItem)
        # exporter.export(f'frames/frame_{self.I:04d}.png')
        self.i += 1
        self.I += 1

plotter = Plotter()

timer = pg.QtCore.QTimer()
timer.timeout.connect(plotter.update)
timer.start(10)
app.exec()
