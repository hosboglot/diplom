import numpy as np
from scipy import signal
import pyqtgraph as pg

from pgplotter import Plotter, Line

# ffmpeg.exe -r 60 -i frames/frame_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p output.mp4

plotter = Plotter(
    (-0.5, 15, -3, 3),
    export=True
)

lim_f = lambda t: np.exp(-0.1 * (t // np.pi) * np.pi)
data = [
    lambda t: (np.sin(t) ** 2) * lim_f(t),
    lambda t: -(np.sin(t) ** 2) * lim_f(t),
    lambda t: (np.sin(t) ** 2) * signal.square(t) * 0.5 * lim_f(t)
]
colors = ['b', 'g', 'r']  # Разные цвета для графиков

plotter.add_line(zero_line := Line(
    np.arange(-1.5, 0, 0.02),
    lambda x: np.zeros_like(x),
    point=True, pen=pg.mkPen('orange', width=3)
))
for i, line in enumerate(data):
    plotter.add_line(Line(
        np.arange(0, 16, 0.02), line,
        point=True, pen=pg.mkPen(colors[i], width=3),
        after=zero_line
    ))

plotter.start()
