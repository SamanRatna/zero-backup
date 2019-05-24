from matplotlib.figure import Figure
import sys
import time
import numpy as np
import PyQt5
import webview
import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

from matplotlib.backends.qt_compat import QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Initialize
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        # Plot static graph
        static_canvas = FigureCanvas(Figure(figsize=(3, 3)))
        layout.addWidget(static_canvas)
        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        # Plot dynamic graph
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()

        # Display image
        label = QLabel(self)
        pixmap = QPixmap('B - images/render_bike.png')
        label.setPixmap(pixmap)
        layout.addWidget(label)

        # Display map
        omap = QWebEngineView()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "901_map.html"))
        local_url = QUrl.fromLocalFile(file_path)
        omap.load(local_url)
        layout.addWidget(omap)

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()


# Execute
if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
