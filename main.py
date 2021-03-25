import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QSize

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy
import sympy


def univariate(sympy_expression_str_: str, x_: numpy.ndarray) -> numpy.ndarray:
    try:
        sympy_expression_ = sympy.sympify(sympy_expression_str_)
    except sympy.SympifyError:
        return numpy.zeros_like(x_)

    if len(sympy_expression_.free_symbols) < 1:
        return numpy.ones_like(x_) * sympy.N(sympy_expression_)
    elif len(sympy_expression_.free_symbols) == 1:
        independent_symbol_ = sympy_expression_.free_symbols.pop()
    else:
        return numpy.zeros_like(x_)

    settings_ = numpy.seterr(all='raise')
    try:
        result_ = sympy.lambdify(independent_symbol_, sympy_expression_, modules='numpy')(x_)

        numpy.seterr(**settings_)
        return result_
    except FloatingPointError:
        numpy.seterr(**settings_)
        return numpy.zeros_like(x_)


class QWidget_FigureCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, figure_size_: QSize = QSize(4, 3), grid_size_: QSize = QSize(1, 1), dpi_=100):
        self.figure = Figure(figsize=(figure_size_.width(), figure_size_.height()), dpi=dpi_)

        self.axes = dict()

        self.grid_size = grid_size_

        super().__init__(self.figure)

    def get_figure(self):
        return self.figure

    def index(self, x_: int, y_: int):
        return (y_ - 1) * self.grid_size.width() + x_

    def add_subplot(self, name_: str, start_: tuple, end_: tuple) -> Figure.axes:
        if name_ not in self.axes:
            axes_ = self.figure.add_subplot(self.grid_size.width(), self.grid_size.height(), (self.index(start_[0], start_[1]), self.index(end_[0], end_[1])))
            self.axes[name_] = axes_

        return self.axes[name_]

    def get_subplot(self, name_: str):
        return self.axes[name_]


def thermodynamics_energy(heat_rate_: numpy.ndarray, power_: numpy.ndarray, interval_: numpy.ndarray) -> numpy.ndarray:
    energy_ = numpy.zeros_like(interval_)

    energy_rate_ = heat_rate_ - power_

    for i_ in numpy.arange(0, energy_.shape[0]):
        energy_[i_] = numpy.trapz(energy_rate_[:(i_ + 1)], interval_[:(i_ + 1)])

    return energy_


def thermodynamics_energy_sympy(heat_rate_sympy_expression_str_: str, power_sympy_expression_str_: str, interval_: numpy.ndarray):
    return thermodynamics_energy(univariate(heat_rate_sympy_expression_str_, interval_), univariate(power_sympy_expression_str_, interval_), interval_)


application_ = QApplication(sys.argv)

widget_ = QWidget()
widget_.show()

application_.exec()
