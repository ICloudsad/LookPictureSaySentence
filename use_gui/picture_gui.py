import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from predict import predict
from PyQt5 import QtGui


class PictureGui(QWidget):
    url = ''

    def __init__(self):
        super().__init__()
        self.show_wind_list = []
        self.path = './'
        self.setUI()

    def setUI(self):
        # set main window information
        self.setWindowIcon(QIcon("./ico/total.ico"))
        self.setWindowTitle(u"看图说话")
        self.setToolTip("<b>看图说话</b>")

        # add button to GUI
        btn_load = QPushButton("导入照片", self)
        btn_load.setToolTip("点击导入需要描述的图片")
        btn_load.setDisabled(False)
        btn_inference = QPushButton("描述图片", self)
        btn_inference.setToolTip("点击开始描述导入的图片")
        btn_inference.setDisabled(True)

        # add checkbox to GUI
        cbx_auto_open = QCheckBox("自动打开", self)
        cbx_auto_open.setToolTip("自动显示检测结果图片")
        cbx_auto_open.setChecked(True)

        # add list
        self.debug_info = QListWidget()
        self.debug_info.setToolTip("日志窗口")

        # add statusBar
        # statusBar = QStatusBar()
        # statusBar.setStyleSheet('QStatusBar::item {border: none;}')
        # self.setStatusBar(statusBar)
        # progressBar = QProgressBar()

        # horizon
        h_box = QHBoxLayout()
        h_box.addWidget(btn_load)
        h_box.addWidget(btn_inference)
        h_box.addWidget(cbx_auto_open)

        # 增添进度条
        # h_box.addWidget(statusBar)
        # h_box.addWidget(progressBar)

        # vertical
        # 设置垂直布局
        v_box = QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addWidget(self.debug_info)

        self.setLayout(v_box)
        self.resize(QSize(500, 400))
        # 设置背景图片
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('../back_ground_img/demo3.png')))
        self.setPalette(window_pale)

        # 设置导入图片按钮点击事件
        btn_load.clicked.connect(self.load_image)
        # 设置描述图片事件
        btn_inference.clicked.connect(self.describe_img)
        self.btn_inference = btn_inference
        self.btn_load = btn_load
        self.cbx_auto_open = cbx_auto_open
        self.center()
        self.show()
        self.debug_info.addItem('Status: BUSY : Please choice you picture...')

    def describe_img(self):
        # 进度条框
        # self.statusBar.addPermanentWidget(self.label, stretch=2)
        # self.statusBar.addPermanentWidget(self.progressBar, stretch=4)
        # self.progressBar.setRange(0, 100)
        # self.progressBar.setMinimum(0)
        # self.progressBar.setMaximum(0)

        self.debug_info.addItem('Status: BUSY :The program is processing images,please wait... ')
        print("input img " + self.url)
        res = predict.lookimage(self.url)
        self.debug_info.addItem('******describe ' + res + '******')
        self.debug_info.addItem('Status:IDLE :images finish !')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # self.move(cp)

    def load_image(self):
        filenames, _ = QFileDialog.getOpenFileNames(self,
                                                    "选取文件",
                                                    self.path,
                                                    "Images (*.jpeg;*.jpg;*.png);;All Files (*)")

        if not filenames:
            return
        self.url = filenames[0]
        # filenames list 类型
        self.path = filenames[0].split(filenames[0].split('/')[-1])[0]
        for filename in filenames:
            # 图片类型辨别
            file_type = filename.split('/')[-1].split('.')[-1]
            if file_type in ['jpg', 'jpeg', 'png']:
                self.debug_info.addItem('Status: BUSY :Load image: ' + filename.split('/')[-1])
                # 正在进行图片类型的判断，未成功时，不会显示 描述图片按钮
                self.btn_inference.setDisabled(False)
            elif file_type:
                # QMessageBox.information(self, "提示", "不支持的格式")
                self.debug_info.addItem('Not support file type of loaded file:' + filename.split('/')[-1])

        self.debug_info.addItem('Status: IDLE :Load images done!')
        # 文件路径标准化转化
        self.url = self.url.replace('/', '\\')

    # def inference(self):
    #     # update gui
    #     self.btn_inference.setDisabled(True)
    #     self.debug_info.addItem('Status: BUSY :The program is processing images,please wait... ')
    # create thread
    # self.infThread = inference_thread(self._filenames, self.vehicle_detector)
    # self.infThread.statusSignal.connect(self.inference_process)
    # self.infThread.start()

    # def inference_process(self, result):
    #     if result[0] == 1:
    #         self.debug_info.addItem(
    #             'Status:BUSY : {}/{},{} proceed done'.format(result[2] + 1, self.im_num, result[1].split('/')[-1]))
    #         if self.cbx_auto_open.isChecked():
    #             result[3].show()
    #     elif result[0] == -1:
    #         self.debug_info.addItem(
    #             'Status:BUSY : {}/{},{} proceed done. No car in this image '.format(result[2] + 1, self.im_num,
    #                                                                                 result[1].split('/')[-1]))
    #     elif result[0] == 0:
    #         self.btn_inference.setDisabled(False)
    #         self.debug_info.addItem('Status:IDLE : All images proceed ')


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建一个应用
    look_picture = PictureGui()
    look_picture.show()
    sys.exit(app.exec_())  # 将app的退出信号传给程序进程，让程序进程退出
