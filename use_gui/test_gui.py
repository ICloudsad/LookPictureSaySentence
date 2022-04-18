import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from predict import predict
from PyQt5 import QtGui


class SampleBar(QMainWindow):
    def __init__(self, parent=None):
        super(SampleBar, self).__init__(parent)
        self.setMinimumSize(400, 100)

        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet('QStatusBar::item {border: none;}')
        self.setStatusBar(self.statusBar)
        self.progressBar = QProgressBar()


        self.label = QLabel()
        self.label.setText("加载中，请稍后... ")

        # 进度条框
        self.statusBar.addPermanentWidget(self.label, stretch=2)
        self.statusBar.addPermanentWidget(self.progressBar, stretch=4)
        self.progressBar.setRange(0, 100)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = SampleBar()
    main.show()
    sys.exit(app.exec_())
