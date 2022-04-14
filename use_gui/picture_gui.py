import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from predict import predict


# class inference_thread(QThread):
# inference 线程
# statusSignal = pyqtSignal(list)

# def __init__(self, parent=None):
#     super(inference_thread, self).__init__(parent)
# self._filenames = filenames
# self.vehicle_detector = vehicle_detector

# def run(self):
#     for idx, filename in enumerate(self._filenames):
#         img_size, image_np = input_for_detecion(filename)
#         file_type = filename.split('/')[-1].split('.')[-1]
#         vehicle_box, vehicle_predict_lab = self.vehicle_detector.inference(image_np, img_size)
#         if vehicle_box:
#             image_result = draw_predictions(image_np, img_size, vehicle_box, vehicle_predict_lab)
#             image_result.save(filename.split(file_type)[0] + '_result.jpg')
#             # signal runing:car detected
#             self.statusSignal.emit([1, filename, idx, image_result])
#         else:
#             # signal runing:no car detected
#             self.statusSignal.emit([-1, filename, idx])
#     # signal finished
#     self.statusSignal.emit([0])


# class load_models_thread(QThread):
# 导入model线程
# finishSignal = pyqtSignal(predict.look_image())

# def __init__(self, parent=None):
#     super(load_models_thread, self).__init__(parent)

# def run(self):
#     # get models config
#     (DETECT_CONFIG, CLASSIFY_CONFIG) = get_models_config()
#     vehicle_detector = VehileDetectionModel(get_detector_mode(), detect_config=DETECT_CONFIG,
#                                             classify_config=CLASSIFY_CONFIG)
#     self.finishSignal.emit(vehicle_detector)


class PictureGui(QWidget):
    url = ''

    def __init__(self):
        super().__init__()
        self.show_wind_list = []
        self.path = './'
        self.setUI()


    # def setlog(LOG_PATH):
    #     LOG_FORMAT = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    #     DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    #     logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    #
    #     console = logging.StreamHandler()
    #     console.setLevel(logging.INFO)
    #     formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    #     console.setFormatter(formatter)
    #     logging.getLogger('').addHandler(console)

    # def get_log_dir():
    #     # path to save logs
    #     if not os.path.exists('./log'):
    #         os.mkdir('./log')
    #     log_name = datetime.now().strftime("log-%Y%m%d-%H%M%S.txt")
    #     LOG_PATH = './log/' + log_name
    #     return LOG_PATH


    def setUI(self):
        # set main window information
        self.setWindowIcon(QIcon("./ico/total.ico"))
        self.setWindowTitle(u"看图说话")
        self.setToolTip("<b>看图说话</b>")

        # add button to GUI
        btn_load = QPushButton("导入照片 开始描述", self)
        btn_load.setToolTip("点击导入需要描述的图片")
        btn_load.setDisabled(False)
        # btn_inference = QPushButton("描述图片", self)
        # btn_inference.setToolTip("点击开始描述导入的图片")
        # btn_inference.setDisabled(True)

        # add checkbox to GUI
        cbx_auto_open = QCheckBox("自动打开", self)
        cbx_auto_open.setToolTip("自动显示检测结果图片")
        cbx_auto_open.setChecked(True)

        # add list
        self.debug_info = QListWidget()
        self.debug_info.setToolTip("日志窗口")

        # add res text

        # horizon
        h_box = QHBoxLayout()
        h_box.addWidget(btn_load)
        # h_box.addWidget(btn_inference)
        h_box.addWidget(cbx_auto_open)

        # vertical
        # 设置垂直布局
        v_box = QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addWidget(self.debug_info)

        self.setLayout(v_box)
        self.resize(QSize(500, 400))

        # 设置导入图片按钮点击事件
        btn_load.clicked.connect(self.load_image)
        # 设置描述图片事件
        # btn_inference.clicked.connect(predict.look_image(os.system('start explorer ' + self.url)))
        # self.btn_inference = btn_inference
        self.btn_load = btn_load
        self.cbx_auto_open = cbx_auto_open
        self.center()
        self.show()
        # img = self.load_image()

        # setlog(get_log_dir())
        # self.debug_info.addItem('Status: BUSY : Set log dir:{}'.format(get_log_dir().split('/')[-1]))
        self.debug_info.addItem('Status: BUSY : Please choice you picture...')

    # def load_models_end(self, result):
    #     self.vehicle_detector = result
    #     self.btn_load.setDisabled(False)
    #     self.debug_info.addItem('Status: IDLE : Load detection model done!')

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
        # self._filenames = []
        # 得到输入图片路径名
        # print(filenames)
        self.url = filenames[0]
        # filenames list 类型
        self.path = filenames[0].split(filenames[0].split('/')[-1])[0]
        # self.im_num = len(filenames)
        for filename in filenames:
            # 图片类型辨别
            file_type = filename.split('/')[-1].split('.')[-1]
            if file_type in ['jpg', 'jpeg', 'png']:
                self.debug_info.addItem('Status: BUSY :Load image: ' + filename.split('/')[-1])
                # 正在进行图片类型的判断，未成功时，不会显示 描述图片按钮
                # self.btn_inference.setDisabled(False)
                # self._filenames.append(filename)
            elif file_type:
                # QMessageBox.information(self, "提示", "不支持的格式")
                self.debug_info.addItem('Not support file type of loaded file:' + filename.split('/')[-1])

        self.debug_info.addItem('Status: IDLE :Load images done!')
        # 文件路径标准化转化
        self.url = self.url.replace('/', '\\')
        print(self.url)
        # todo 使用文件路径，得到图片文件，作为参数传入
        # self.debug_info.addItem(predict.look_image(os.system("start explorer " + self.url)))

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
