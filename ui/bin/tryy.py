from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import cv2
import sys

class window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        img = cv2.imread('../ajisai.png')
        print(img.shape)
        # cv2.imshow('2', img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        qimage = QImage(img, img.shape[1], img.shape[0],
                        QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        pixmap = pixmap.scaled(320, 240, Qt.KeepAspectRatio)

        self.img_label = QLabel()
        self.img_label.setPixmap(pixmap)

        self.main_layout.addWidget(self.img_label)
        self.setWindowTitle('Red Rock')
        self.start_stream()

    def start_stream(self):
        self.stop_progress = False
        self.run_thread = RunThread(parent=None)
        self.run_thread.start()
        self.run_thread.single_frame.connect(self.show_image)

    def show_image(self, qimage):
        if not self.stop_progress:
            pixmap = QPixmap.fromImage(qimage)
            pixmap = pixmap.scaled(320, 240, Qt.KeepAspectRatio)
            self.img_label.setPixmap(pixmap)

class RunThread(QThread):
    single_frame = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(RunThread, self).__init__(parent)
        self.stop = False

    def run(self):
        stream = cv2.VideoCapture(0)
        while(not self.stop):
            next, frame = stream.read()
            if not next:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qimage = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.single_frame.emit(qimage)
            print('biu~')

    def stop(self):
        self.stop = True
        print('thread is sleeping~')
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = window()
    w.show()
    sys.exit(app.exec_())