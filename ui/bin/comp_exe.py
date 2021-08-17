from ui.bin import comp
from PyQt5 import QtCore, QtWidgets
import sys
import time

class MainWindow(object):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        with open('../qss/ElegantDark.qss') as file:
            str = file.readlines()
            str = ''.join(str).strip('\n')
            app.setStyleSheet(str)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = comp.Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.update_date() # 保证初始对应正确 接收者，先调用
        self.update_calendar() # 设置信号槽 发出者，后调用

        self.set_lcd()
        self.set_dial()

        self.update_progressbar()
        self.progressbar_counter()

        self.set_font()

        MainWindow.show()
        sys.exit(app.exec_())

    def update_date(self):
        self.ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())

    def update_calendar(self):
        self.ui.calendarWidget.selectionChanged.connect(self.update_date)

    # 设置LCD数字
    def set_lcd(self):
        self.ui.lcdNumber.display(self.ui.dial.value())

    # 刻度盘信号槽
    def set_dial(self):
        self.ui.dial.valueChanged['int'].connect(self.set_lcd)

    # 按钮信号槽
    def update_progressbar(self):
        self.ui.radioButton.clicked.connect(self.start_progressbar)
        self.ui.radioButton_2.clicked.connect(self.stop_progressbar)
        self.ui.radioButton_3.clicked.connect(self.reset_progressbar)
        self.progress_value = 0
        self.stop_progress = False


    # # 启动进度栏
    # def start_progressbar(self):
    #     self.stop_progress = False
    #     self.progress_value = self.ui.progressBar.value()
    #     # self.progress_value = 0
    #
    #     while (self.progress_value <= 100.1) and not (self.stop_progress):
    #         self.ui.progressBar.setValue(self.progress_value)
    #         self.progress_value += 0.0001
    #         QtWidgets.QApplication.processEvents()
    #         print('gggg')

    def start_progressbar(self):
        self.stop_progress = False
        self.progress_value = self.ui.progressBar.value()
        self.progressbar_counter(self.progress_value)


    # # 停止进度栏
    # def stop_progressbar(self):
    #     self.stop_progress = True

    def stop_progressbar(self):
        self.stop_progress = True
        try:
            self.run_thread.stop()
        except:
            pass

    # 重设进度栏
    def reset_progressbar(self):
        self.progress_value = 0
        self.ui.progressBar.reset()
        self.stop_progress = False
        self.stop_progressbar()

    # 显示字体
    def set_font(self):
        self.ui.fontComboBox.activated['QString'].connect(self.ui.label.setText)

    # 启动线程管理器
    def progressbar_counter(self, start_value=0):
        self.run_thread = RunThread(parent=None, counter_start=start_value)
        self.run_thread.start()
        self.run_thread.counter_value.connect(self.set_progressbar) # counter_value信号在发送时就带了一个int参数

    def set_progressbar(self, counter): # counter: conter_value信号携带的int值
        if not self.stop_progress:
            self.ui.progressBar.setValue(counter)

class RunThread(QtCore.QThread):
    # 自定义信号
    counter_value = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, counter_start=0):
        super(RunThread, self).__init__(parent)
        self.counter = counter_start
        self.is_running = True

    def run(self):
        while self.counter < 100 and self.is_running:
            time.sleep(0.1)
            self.counter += 1
            print(self.counter)
            self.counter_value.emit(self.counter) # 发射信号

    def stop(self):
        self.is_running = False # 退出循环，停止线程
        print('线程停止中。。。')
        self.terminate() # 手动确保线程停止



if __name__ == "__main__":
    MainWindow()