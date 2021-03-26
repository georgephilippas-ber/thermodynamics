from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy
import thermodynamics

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


from PyQt5.QtWidgets import QLabel, QLineEdit, QDial, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt


class QWidget_thermodynamics(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout_ = QGridLayout()

#
        self.duration_QVBoxLayout = QVBoxLayout()

        self.duration_title_QLabel = QLabel("duration")
        self.duration_title_QLabel.setAlignment(Qt.AlignCenter)
        self.duration_QDial = QDial()
        duration_QDial_properties_ = {'minimum': 20, 'maximum': 5 * 60, 'singleStep': 1, 'pageStep': 5, 'value': 2 * 60}
        for property_name_ in duration_QDial_properties_:
            self.duration_QDial.setProperty(property_name_, duration_QDial_properties_[property_name_])
        self.duration_QDial.valueChanged.connect(lambda: self.duration_QLabel.setText(str(self.duration_QDial.value()) + ' s'))

        self.duration_QLabel = QLabel()
        self.duration_QLabel.setText(str(self.duration_QDial.value()) + ' s')
        self.duration_QLabel.setAlignment(Qt.AlignCenter)

        self.duration_QVBoxLayout.addWidget(self.duration_title_QLabel)
        self.duration_QVBoxLayout.addWidget(self.duration_QLabel)
        self.duration_QVBoxLayout.addWidget(self.duration_QDial)
#
        self.step_QVBoxLayout = QVBoxLayout()

        self.step_title_QLabel = QLabel("step")
        self.step_title_QLabel.setAlignment(Qt.AlignCenter)
        self.step_QDial = QDial()
        step_QDial_properties_ = {'minimum': 1, 'maximum': 10, 'singleStep': 1, 'pageStep': 1, 'value': 5}
        for property_name_ in step_QDial_properties_:
            self.step_QDial.setProperty(property_name_, step_QDial_properties_[property_name_])
        self.step_QDial.valueChanged.connect(lambda: self.step_QLabel.setText(str(self.step_QDial.value()) + ' s'))

        self.step_QLabel = QLabel()
        self.step_QLabel.setText(str(self.step_QDial.value()) + ' s')
        self.step_QLabel.setAlignment(Qt.AlignCenter)

        self.step_QVBoxLayout.addWidget(self.step_title_QLabel)
        self.step_QVBoxLayout.addWidget(self.step_QLabel)
        self.step_QVBoxLayout.addWidget(self.step_QDial)

#
        self.heat_rate_QHBoxLayout = QHBoxLayout()

        self.heat_rate_QLabel = QLabel("heat rate (kW - s)")
        self.heat_rate_QLineEdit = QLineEdit('0 * t')

        self.heat_rate_QHBoxLayout.addWidget(self.heat_rate_QLabel)
        self.heat_rate_QHBoxLayout.addWidget(self.heat_rate_QLineEdit)
#
        self.power_QHBoxLayout = QHBoxLayout()

        self.power_QLabel = QLabel("power (kW - s)")
        self.power_QLineEdit = QLineEdit('0 * t')

        self.power_QHBoxLayout.addWidget(self.power_QLabel)
        self.power_QHBoxLayout.addWidget(self.power_QLineEdit)
#
        self.figure_QVBoxLayout = QVBoxLayout()

        self.figure_QWidget_FigureCanvas = QWidget_FigureCanvas(grid_size_=QSize(3, 1))
        self.figure_QVBoxLayout.addWidget(self.figure_QWidget_FigureCanvas)
        self.update_QPushButton = QPushButton('&Update')
        self.update_QPushButton.clicked.connect(self.update_figure)
        self.figure_QVBoxLayout.addWidget(self.update_QPushButton)
#
        self.composite_list_ = []

        composite_ = QHBoxLayout()
        composite_.addLayout(self.duration_QVBoxLayout)
        composite_.addLayout(self.step_QVBoxLayout)
        self.composite_list_.append([composite_, 1, 1, 1, 1])

        composite_ = QVBoxLayout()
        composite_.addLayout(self.heat_rate_QHBoxLayout)
        composite_.addLayout(self.power_QHBoxLayout)
        self.composite_list_.append([composite_, 1, 2, 1, 1])

        composite_ = self.figure_QVBoxLayout
        self.composite_list_.append([composite_, 2, 1, 1, 2])

        for layout_ in self.composite_list_:
            self.layout_.addLayout(layout_[0], layout_[1], layout_[2], layout_[3], layout_[4])

        self.setLayout(self.layout_)

        self.update_figure()

    def update_figure(self):
        interval_ = numpy.arange(0, self.duration_QDial.value(), self.step_QDial.value())

        heat_rate_plot_ = self.figure_QWidget_FigureCanvas.add_subplot('heat_rate', (1, 1), (1, 1))
        heat_rate_plot_.cla()
        heat_rate_plot_.set_title('$\Delta{E}_t = \int_{0}^{t} \dot{Q}(s) - \dot{W}(s) \,ds$')
        heat_rate_plot_.set_xlim(0.0, self.duration_QDial.maximum())
        heat_rate_plot_.set_ylabel('$\dot{Q}$ (kW)')
        heat_rate_plot_.plot(interval_, thermodynamics.univariate(self.heat_rate_QLineEdit.text(), interval_), color='red')

        power_plot_ = self.figure_QWidget_FigureCanvas.add_subplot('power', (2, 1), (2, 1))
        power_plot_.cla()
        power_plot_.set_xlim(0.0, self.duration_QDial.maximum())
        power_plot_.set_ylabel('$\dot{W}$ (kW)')
        power_plot_.plot(interval_, thermodynamics.univariate(self.power_QLineEdit.text(), interval_), color='green')

        energy_plot_ = self.figure_QWidget_FigureCanvas.add_subplot('energy', (3, 1), (3, 1))
        energy_plot_.cla()
        energy_plot_.set_xlim(0.0, self.duration_QDial.maximum())
        energy_plot_.set_xlabel('$t$ (s)')
        energy_plot_.set_ylabel('$\Delta{E}$ (kJ)')
        energy_plot_.plot(interval_, thermodynamics.thermodynamics_energy_sympy(self.heat_rate_QLineEdit.text(), self.power_QLineEdit.text(), interval_), color='blue')

        self.figure_QWidget_FigureCanvas.get_figure().canvas.draw_idle()
