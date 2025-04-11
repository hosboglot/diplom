import numpy as np
import pyqtgraph as pg

from pgplotter import Plotter, Line

# ffmpeg.exe -r 30 -i frames/frame_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p output.mp4

# y = C1*x^2 + C2*x^3
A = (-3, 1)
Bs = [(1., -0.4), (0.75, 1.), (1.4, 0.8)]
C = (2., 1.5)

class EulerLine(Line):
    def __init__(self, B: tuple[float, float], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.B = B
        self.C = C

        self.C2 = (self.B[0]**2 * self.C[1] - self.B[1] * self.C[0]**2) / \
                (self.B[0]**2 * self.C[0]**2 * (self.C[0] - self.B[0]))
        self.C1 = (self.B[1] - self.C2*self.B[0]**3) / self.B[0]**2

    def make_right(self, *args, **kwargs):
        line = EulerLine(self.B, *args, **kwargs)
        line.C1 = self.C1
        line.C2 = (A[1] - self.C1*A[0]**2) / A[0]**3
        return line

    def __call__(self, x: float):
        return self.C1 * x**2 + self.C2 * x**3

plotter = Plotter((-4, 4, -5, 5), export=False)

colors = ['g', 'b', 'r', 'c']
right_lines = [
    EulerLine(B, np.arange(0, 4, 0.02), point=True, pen=pg.mkPen(colors[i], width=3))
    for i, B in enumerate(Bs)
]
left_line = right_lines[2].make_right(
    np.arange(-4, 0, 0.02),
    point=True, pen=pg.mkPen(colors[-1], width=3)
)

plotter.add_line(left_line)
for line in right_lines:
    line.after = left_line
    plotter.add_line(line)

plotter.add_point(A, pg.mkBrush('k'))
for i, B in enumerate(Bs):
    plotter.add_point(B, pg.mkBrush(colors[i]))
plotter.add_point(C, pg.mkBrush('k'))

plotter.start()
