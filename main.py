import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from interface import QWidget_thermodynamics

application_ = QApplication(sys.argv)
desktop_widget_ = QDesktopWidget()

widget_ = QWidget_thermodynamics()
widget_.setMinimumWidth(int(desktop_widget_.width() * 0.25))
widget_.setMinimumHeight(int(desktop_widget_.height() * 0.65))
widget_.setWindowTitle('thermodynamics')
widget_.show()

application_.exec()
