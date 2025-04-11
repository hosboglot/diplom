from typing import Callable, Self
import numpy as np
from pathlib import Path
from shutil import rmtree

import pyqtgraph as pg
import pyqtgraph.exporters

# ffmpeg.exe -r 30 -i frames/frame_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p output.mp4

pg.setConfigOption('background', 'w')  # Устанавливаем светлую тему
pg.setConfigOption('foreground', 'k')

class Line:
    def __init__(self, x_range: np.ndarray, func: Callable | None = None, point: bool = False, pen: pg.QtGui.QPen | None = None,
                 after: Self | None = None):
        self.x_range = x_range
        self.func = func
        self.point = point
        self.pen = pen or pg.mkPen('b', width=3)
        self.finished = False
        self.after = after
        self.i = 0

    def init_plotter(self, plotter: 'Plotter'):
        self.plotter = plotter
        self.plotItem_i = len(plotter.plot.plotItem.dataItems)
        plotter.plot.plot(pen=None)
        if self.point:
            plotter.plot.plot([0], [0], symbolPen=None, symbolBrush=None, symbol='o')

    def __call__(self, x: np.ndarray):
        return self.func(x)

    def update(self):
        if (self.after is None or self.after.finished) and not self.finished:
            self.plotter.plot.plotItem.dataItems[self.plotItem_i].setPen(self.pen)
            self.plotter.plot.plotItem.dataItems[self.plotItem_i].setData(
                self.x_range[:self.i],
                self.__call__(self.x_range[:self.i])
            )
            if self.point and self.i > 0:
                self.plotter.plot.plotItem.dataItems[self.plotItem_i + 1].setSymbolBrush(self.pen.brush())
                self.plotter.plot.plotItem.dataItems[self.plotItem_i + 1].setData(
                    [self.x_range[self.i - 1]],
                    [self.__call__(self.x_range[self.i - 1])]
                )
            if self.i == len(self.x_range):
                self.finished = True
                self.plotter.plot.plotItem.dataItems[self.plotItem_i + 1].setSymbolBrush(None)
            self.i += 1


class Plotter:
    def __init__(self, ranges_lrdu: tuple[float, float, float, float], export: bool = False):
        self.left, self.right, self.down, self.up = ranges_lrdu
        self.export = export
        
        self.lines: list[Line] = []

        self.plot = pg.plot()

        self.plot.showGrid(x=True, y=True)
        self.plot.setXRange(self.left, self.right)
        self.plot.setYRange(self.down, self.up)

        if export:
            self.export_path = Path('frames')
            rmtree(self.export_path, ignore_errors=True)
            self.export_path.mkdir()

            self.exporter = pyqtgraph.exporters.ImageExporter(self.plot.plotItem)
            self.frame_i = 0

    def add_line(self, line: Line):
        line.init_plotter(self)
        self.lines.append(line)

    def add_point(self, pos: tuple[float, float], brush: pg.QtGui.QBrush | None = None):
        self.plot.plot([pos[0]], [pos[1]], symbolBrush=brush or pg.mkBrush(), symbol='o')

    def update(self):
        for line in self.lines:
            line.update()
        if self.export and not all([line.finished for line in self.lines]):
            self.exporter.export((self.export_path / f'frame_{self.frame_i:04d}.png').as_posix())
            self.frame_i += 1

    def start(self):
        app = pg.mkQApp()
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        return app.exec()
