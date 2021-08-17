from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QMainWindow, QGridLayout, QStatusBar, QCheckBox, QProgressBar
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMetaObject
import cv2
import sys

class MainUi(object):
    def setupUi(self, main_window):
        # main_window = QMainWindow()
        # 主窗口
        main_window.setFixedSize(800, 400)
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.statusbar = QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        main_window.setObjectName('MainWindow')
        self.main_widget.setObjectName('main_widget')
        self.statusbar.setObjectName("statusbar")

        # 上侧部分，下侧部分
        ## 上侧部分
        self.top_widget = QWidget()
        self.top_layout = QGridLayout()
        self.top_widget.setLayout(self.top_layout)

        self.main_layout.addWidget(self.top_widget, 0, 0, 4, 8)

        self.top_widget.setObjectName('top_widget')

        ### 上侧左
        self.topleft_widget = QWidget()
        self.topleft_layout = QGridLayout()
        self.topleft_widget.setLayout(self.topleft_layout)
        self.show_label = QLabel()
        self.show_label.setAlignment(Qt.AlignTop)
        self.show_label.setAlignment(Qt.AlignLeft)
        #### 显示图片
        img = cv2.imread('bin/img0.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        # pixmap = pixmap.scaled(320, 240, Qt.KeepAspectRatio)
        self.show_label.setPixmap(pixmap)

        self.top_layout.addWidget(self.topleft_widget, 0, 0, 1, 1)
        self.topleft_layout.addWidget(self.show_label)

        self.topleft_widget.setObjectName('topleft_widget')
        self.show_label.setObjectName('show_label')

        ### 上侧右
        self.topright_widget = QWidget()
        self.topright_layout = QGridLayout()
        # self.topright_layout.setAlignment(Qt.AlignTop)
        # self.topright_layout.setSpacing(0) # 去掉间隔
        self.topright_widget.setLayout(self.topright_layout)
        self.currentWork0_label = QLabel()
        self.currentWork0_label.setAlignment(Qt.AlignRight)
        self.currentWork0_label.setText('当前工作:')
        self.currentWork1_label = QLabel()
        self.currentWork1_label.setAlignment(Qt.AlignLeft)
        self.currentWork1_label.setText('对接管子')
        self.leftPose_label = QLabel()
        self.leftPose_label.setText('左手动作')
        self.leftPose0_label = QLabel()
        self.leftPose0_label.setText('手持管子')
        self.leftPose1_label = QLabel()
        self.leftPose1_label.setText('扶/按')
        self.leftBelief0_label = QLabel()
        self.leftBelief0_label.setText('0.0')
        self.leftBelief1_label = QLabel()
        self.leftBelief1_label.setText('0.0')
        self.rightPose_label = QLabel()
        self.rightPose_label.setText('右手动作')
        self.rightPose0_label = QLabel()
        self.rightPose0_label.setText('手持管子')
        self.rightPose1_label = QLabel()
        self.rightPose1_label.setText('扶/按')
        self.rightBelief0_label = QLabel()
        self.rightBelief0_label.setText('0.0')
        self.rightBelief1_label = QLabel()
        self.rightBelief1_label.setText('0.0')
        #### 进度条
        self.leftClass0_bar = QProgressBar()
        self.leftClass0_bar.setProperty('lc0', 0)
        self.leftClass0_bar.setTextVisible(False)
        self.leftClass1_bar = QProgressBar()
        self.leftClass1_bar.setProperty('lc1', 0)
        self.leftClass1_bar.setTextVisible(False)
        self.rightClass0_bar = QProgressBar()
        self.rightClass0_bar.setProperty('rc0', 0)
        self.rightClass0_bar.setTextVisible(False)
        self.rightClass1_bar = QProgressBar()
        self.rightClass1_bar.setProperty('rc1', 0)
        self.rightClass1_bar.setTextVisible(False)

        self.top_layout.addWidget(self.topright_widget, 0, 1, 1, 1)
        self.topright_layout.addWidget(self.currentWork0_label, 0, 0, 1, 2)
        self.topright_layout.addWidget(self.currentWork1_label, 0, 2, 1, 2)

        self.topright_layout.addWidget(self.leftPose_label, 1, 0, 1, 4)
        self.topright_layout.addWidget(self.leftPose0_label, 2, 0, 1, 1)
        self.topright_layout.addWidget(self.leftClass0_bar, 2, 1, 1, 2)
        self.topright_layout.addWidget(self.leftBelief0_label, 2, 3, 1, 1)
        self.topright_layout.addWidget(self.leftPose1_label, 3, 0, 1, 1)
        self.topright_layout.addWidget(self.leftClass1_bar, 3, 1, 1, 2)
        self.topright_layout.addWidget(self.leftBelief1_label, 3, 3, 1, 1)

        self.topright_layout.addWidget(self.rightPose_label, 4, 0, 1, 4)
        self.topright_layout.addWidget(self.rightPose0_label, 5, 0, 1, 1)
        self.topright_layout.addWidget(self.rightClass0_bar, 5, 1, 1, 2)
        self.topright_layout.addWidget(self.rightBelief0_label, 5, 3, 1, 1)
        self.topright_layout.addWidget(self.rightPose1_label, 6, 0, 1, 1)
        self.topright_layout.addWidget(self.rightClass1_bar, 6, 1, 1, 2)
        self.topright_layout.addWidget(self.rightBelief1_label, 6, 3, 1, 1)

        self.topright_widget.setObjectName('topright_widget')
        self.currentWork0_label.setObjectName('currentWork0_label')
        self.currentWork1_label.setObjectName('currentWork1_label')
        self.leftPose_label.setObjectName('leftPose_label')
        self.leftPose0_label.setObjectName('leftPose0_label')
        self.leftPose1_label.setObjectName('leftPose1_label')
        self.leftClass0_bar.setObjectName('leftClass0_bar')
        self.leftClass1_bar.setObjectName('leftClass1_bar')
        self.leftBelief0_label.setObjectName('leftBelief0_label')
        self.leftBelief1_label.setObjectName('leftBelief1_label')
        self.rightPose_label.setObjectName('rightPose_label')
        self.rightPose0_label.setObjectName('rightPose0_label')
        self.rightPose1_label.setObjectName('rightPose1_label')
        self.rightClass0_bar.setObjectName('rightClass0_bar')
        self.rightClass1_bar.setObjectName('rightClass1_bar')
        self.rightBelief0_label.setObjectName('rightBelief0_label')
        self.rightBelief1_label.setObjectName('rightBelief1_label')


        ## 下侧部分
        self.bottom_widget = QWidget()
        self.bottom_layout = QGridLayout()
        self.bottom_widget.setLayout(self.bottom_layout)
        self.editArea_label = QLabel()
        self.editArea_label.setText('设置')
        #### 设置当前工作下拉框
        self.editCurrentWork_label = QLabel()
        self.editCurrentWork_label.setText('设置当前工作')
        #### 显示骨骼，隐藏骨骼radiobutton
        self.showSkeleton_checkbox = QCheckBox('显示骨骼', self.bottom_widget)
        #### 显示置信度，隐藏置信度radiobutton
        self.showBelief_checkbox = QCheckBox('显示置信度', self.bottom_widget)

        self.main_layout.addWidget(self.bottom_widget, 4, 0, 2, 8)
        self.bottom_layout.addWidget(self.editArea_label, 0, 0, 1, 3)
        self.bottom_layout.addWidget(self.editCurrentWork_label, 1, 0, 1, 1)
        self.bottom_layout.addWidget(self.showSkeleton_checkbox, 1, 1, 1, 1)
        self.bottom_layout.addWidget(self.showBelief_checkbox, 1, 2, 1, 1)

        self.bottom_widget.setObjectName('bottom_widget')
        self.editArea_label.setObjectName('editArea_label')
        self.editCurrentWork_label.setObjectName('editCurrentWork_label')
        self.showSkeleton_checkbox.setObjectName('showSkeleton_checkbox')
        self.showBelief_checkbox.setObjectName('showBelief_checkbox')

        # 整合
        main_window.setCentralWidget(self.main_widget)
        QMetaObject.connectSlotsByName(main_window)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('qss/ElegantDark.qss') as file:
        str = file.readlines()
        str = ''.join(str).strip('\n')
        app.setStyleSheet(str)
    MainWindow = QMainWindow()
    Ui = MainUi()
    Ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())







