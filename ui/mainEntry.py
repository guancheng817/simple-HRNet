import sys
import os
sys.path.insert(1, os.getcwd())
import torch
print(sys.path)
from scripts.sit_ups import sitUps
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication,QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from openCamera import Ui_Mainwindow, Ui_Dialog
from opts import parse_opts

class PyQtMainEntry(QMainWindow, Ui_Mainwindow, sitUps):
    def __init__(self, args):
        super().__init__()
        # self.main_ui = Ui_Mainwindow()
        # self.main_ui.setupUi(self)
        self.setupUi(self)

        self.args = args
        #self.main(self.args)
        self.count_down = args.timer
        self.num_of_before_click = 0

        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)
        self.btn_start = False

        self.is_camera_opened = False  # 摄像头有没有打开标记
        # self.timer_open_camera = QtCore.QTimer(self)
        # self.timer_open_camera.timeout.connect(self._queryFrame)
        # self.timer_open_camera.setInterval(30)
        self.starting_button = False
        self.reset_button = False
        self.flag = False  ## 计时开始 flag
    def start_testing(self):
        '''
        start testing
        '''
        # if self.btnOpenCamera.isEnabled():
        #     QtWidgets.QMessageBox.warning(self, "警告", "请先打开摄像头", QtWidgets.QMessageBox.Cancel)

        # else:
        self.starting_button = True
        self.starting.setEnabled(False)
        #self.btnOpenCamera.setEnabled(False)
        self.flag = True
        # if self.reset_button:
        #     self.count_down = args.timer
        self.count_down = args.timer

    def Reset(self):
        '''
        reset and restart
        :return:
        '''
        # if self.btnOpenCamera.isEnabled():
        #     QtWidgets.QMessageBox.warning(self, "警告", "请先打开摄像头", QtWidgets.QMessageBox.Cancel)
        #else:
        self.starting_button = False
        self.starting.setEnabled(True)
        #self.btnOpenCamera.setEnabled(True)
        self.Counter(num_of_std=' ')  # counter clear
        self.timer_box.setText(' ')  # timer clear
        self.time.stop()

    def btnOpenCamera_Clicked(self):
        '''
        打开和关闭摄像头
        '''
        frame_generator = self.main(self.args)

        # if self.flag:
        #     self.Action()
        self.btnOpenCamera.setEnabled(False)
        while True:
            if self.flag:
                self.Action()
                self.flag = False

            #if self.starting.isEnabled():
            if not self.starting_button:
                state_box_text, error_box_text, self.frame, num_of_std = next(frame_generator)
                self.num_of_before_click = num_of_std
            else:
                state_box_text, error_box_text, self.frame, num_of_std = next(frame_generator)
                num_of_std = num_of_std - self.num_of_before_click
                self.State_Box(state_box_text)
                self.Error_Box(error_box_text)
                self.Counter(num_of_std)


            img_rows, img_cols, channels = self.frame.shape
            bytesPerLine = channels * img_cols
            cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
            QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)

            self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            QApplication.processEvents()

    def Close(self):
        #self.done(0)
        os._exit()

    def Action(self):
        #print(self.starting.isEnabled())
        #if self.btnOpenCamera.isEnabled():
        if self.starting_button:
            self.time.start()
            #self.btnOpenCamera.setEnabled(False)


    def Refresh(self):
        if self.count_down > 0:
            self.timer_box.setText('剩余时间/s：'+ str(self.count_down))
            self.count_down -= 1
            #print(self.count_down)
        else:
            print('debug in count less than 0',self.count_down)
            self.time.stop()
            #time.sleep(5)

    def Counter(self, num_of_std):
        self.counter_box.setText('标准数：' + str(num_of_std))


    def State_Box(self, state_box_text):
        #print(self.count_down)
        if self.count_down <= 0:
            self.state_box.setText('测试结束')
            self.timer_box.setText('剩余时间(s)：0' )
            self.starting_button = False
            #self.starting.setEnabled(True)
            #time.sleep(5)
        else:
            self.state_box.setText(state_box_text)

    def Error_Box(self, error_box_text):
        self.error_box.setText(error_box_text)


    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()

    # def setArgs(self):
    #     dialog = QtWidgets.QDialog()
    #     btn = QPushButton("ok", dialog)
    #     btn.move(50, 50)
    #     self.arg1= QtWidgets.QLineEdit(dialog)
    #     self.arg1.setGeometry(QRect(70, 70, 81, 50))
    #     self.arg1.setObjectName("arg_1")
    #     self.arg1.textChanged.connect(self.getArgs)
    #     dialog.setWindowTitle("Dialog")
    #     dialog.setWindowModality(Qt.ApplicationModal)
    #     dialog.exec_()
    #
    # def getArgs(self):
    #     args.stg = int(self.lineEdit.text())
    #     print(type(self.lineEdit_2.text()))
    #     args.sew = int(self.lineEdit_2.text())


    # @QtCore.pyqtSlot()
    # def _queryFrame(self):
    #     '''
    #     循环捕获图片
    #     '''
    #     ret, self.frame = self.camera.read()
    #     img_rows, img_cols, channels = self.frame.shape
    #     bytesPerLine = channels * img_cols
    #     cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
    #     QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
    #     self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
    #         self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

class childWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        #super().__init__()
        QtWidgets.QDialog.__init__(self)
        #self.args = args
        self.setupUi(self)
        # self.child=Ui_Dialog()
        # self.child.setupUi(self)

    def getArgs(self):

        self.stg = self.stgText.text()
        self.sew = self.sewText.text()
        self.raise_feet = self.raiseFeetText.text()
        self.hks = self.hksText.text()
        self.ratio_distance = self.ratioDistanceText.text()
        # args.stg = int(stg) if stg != '' else args.stg
        # args.sew = int(sew) if sew != '' else args.sew
        # args.raise_feet = int(raise_feet) if raise_feet != '' else args.raise_feet
        # args.hks = int(hks) if hks != '' else args.hks
        # args.ratio_distance = float(ratio_distance) if ratio_distance != '' else args.ratio_distance

        print('stg', args.stg)
        print('ratio', args.ratio_distance)

    def save(self):

        try:
            if not self.stg.isdigit() or not self.sew.isdigit() or not self.raise_feet.isdigit() or \
                not self.hks.isdigit() or not type(eval(self.ratio_distance)) == float:
                QtWidgets.QMessageBox.warning(self, "警告", "出现非法字符或者未准确填写参数表", QtWidgets.QMessageBox.Cancel)
            elif not  5<=int(self.stg)<=10 or not 90<=int(self.sew)<=100 or not 5<=int(self.raise_feet)<=10 \
                or not 60<=int(self.hks)<=80 or not 0.2<=float(self.ratio_distance)<=0.4:
                QtWidgets.QMessageBox.warning(self, "警告", "请准确填写参数范围", QtWidgets.QMessageBox.Cancel)
            else:
                args.stg = int(self.stg) if self.stg != '' else args.stg
                args.sew = int(self.sew) if self.sew != '' else args.sew
                args.raise_feet = int(self.raise_feet) if self.raise_feet != '' else args.raise_feet
                args.hks = int(self.hks) if self.hks != '' else args.hks
                args.ratio_distance = float(self.ratio_distance) if self.ratio_distance != '' else args.ratio_distance
                QtWidgets.QMessageBox.information(self, "提示", "保存成功", QtWidgets.QMessageBox.Cancel)
        except AttributeError:
            QtWidgets.QMessageBox.warning(self, "警告", "请填写参数表", QtWidgets.QMessageBox.Cancel)


    def cancel(self):
        self.done(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    args = parse_opts()
    child = childWindow()
    window = PyQtMainEntry(args)


    btn=window.toolButton
    btn.clicked.connect(child.show)

    window.show()
    window.btnOpenCamera_Clicked()

    sys.exit(app.exec_())

