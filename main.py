import sys

from PyQt5.QtWidgets import QApplication, QWidget

import sympy
import numpy
import matplotlib

application_ = QApplication(sys.argv)

for i_ in range(0, 121):
    print(i_)

widget_ = QWidget()
widget_.show()



application_.exec()
