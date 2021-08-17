from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import cv2
import sys
import tensorflow as tf
import numpy as np
import os
import datetime

from ui import ex_template
from utils.fileio import prepare_data
from ui.eva import PyOpenpose

class MainWindow(object):
    def __init__(self):
        self.MainWindow = QMainWindow()
        self.ui = ex_template.MainUi()
        self.ui.setupUi(self.MainWindow)
        self.initUi()

        self.MainWindow.setWindowTitle('基于第一人称视角的手部操作动作识别')
        self.startThread()

    def initUi(self):
        self.ui.showSkeleton_checkbox.toggle()
        self.ui.showBelief_checkbox.toggle()
        self.setCheckbox()

    def startThread(self):
        self.stop = False
        self.posenames = ['对接', '扶/按压']
        self.threashold = 0.4
        self.thread = RunThread(parent=None)
        self.thread.start()
        self.thread.single_frame.connect(self.show_image)

    def show_image(self, qimage, fps, infer):
        if not self.stop:
            pixmap = QPixmap.fromImage(qimage)
            self.ui.show_label.setPixmap(pixmap)
            self.ui.statusbar.showMessage('fps:{}'.format(fps))
            # self.ui.leftPose1_label.setText(infer[0])
            # self.ui.rightPose1_label.setText(infer[1])
            Lmax_index, Rmax_index = np.argmax(infer[0]), np.argmax(infer[1])
            Lscore_index = Lmax_index if infer[0][Lmax_index] >= self.threashold else -1
            Rscore_index = Rmax_index if infer[1][Rmax_index] >= self.threashold else -1
            LPose = 'Undefined' if Lscore_index == -1 else self.posenames[Lscore_index]
            RPose = 'Undefined' if Rscore_index == -1 else self.posenames[Rscore_index]

            self.ui.leftPose_label.setText('左手动作: ' + LPose)
            self.ui.leftClass0_bar.setValue(infer[0][0] * 100)
            self.ui.leftBelief0_label.setText('{}'.format(infer[0][0]))
            self.ui.leftClass1_bar.setValue(infer[0][1] * 100)
            self.ui.leftBelief1_label.setText('{}'.format(infer[0][1]))

            self.ui.rightPose_label.setText('右手动作: ' + RPose)
            self.ui.rightClass0_bar.setValue(infer[1][0] * 100)
            self.ui.rightBelief0_label.setText('{}'.format(infer[1][0]))
            self.ui.rightClass1_bar.setValue(infer[1][1] * 100)
            self.ui.rightBelief1_label.setText('{}'.format(infer[1][1]))

    def setCheckbox(self):
        self.ui.showSkeleton_checkbox.stateChanged.connect(self.showSkeleton)
        self.ui.showBelief_checkbox.stateChanged.connect(self.showBelief)

    def showSkeleton(self, state):
        if state == Qt.Checked:
            self.thread.show_skeleton = True
        else:
            self.thread.show_skeleton = False

    def showBelief(self, state):
        if state == Qt.Checked:
            self.thread.show_belief = True
        else:
            self.thread.show_belif = False

class RunThread(QThread):
    single_frame = pyqtSignal(QImage, float, list)

    def __init__(self, parent=None):
        super(RunThread, self).__init__(parent)
        self.stop = False
        self.openpose = PyOpenpose()
        self.show_skeleton = True
        self.show_belief = True
        print('线程初始化完成')

    def run(self):
        # Start Webcam
        source = "D:/openpose-master/data/wl2.mp4"
        stream = cv2.VideoCapture(0)
        stream.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        # Load graph
        pb_file = '../checkpoint/graph.pb'
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(pb_file, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        # Initialize
        fps = 0
        # threashold = 0.4
        count = 0
        # posenames = ['对接', '扶/按压']
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # 屏蔽tensorflow通知信息

        print('进入循环')
        # Start Evaluation
        while (not self.stop):
            start = datetime.datetime.now()
            next, imageToProcess = stream.read()
            if not next:
                cv2.destroyAllWindows()
                stream.release()
                self.stop = True
                continue

            self.openpose.datum.cvInputData = imageToProcess

            # Process and display image
            self.openpose.opWrapper.emplaceAndPop([self.openpose.datum])
            Lresult, Rresult = prepare_data(self.openpose.datum.handKeypoints[0], self.openpose.datum.handKeypoints[1])

            with tf.Session(graph=detection_graph) as sess:
                input_tensor = detection_graph.get_tensor_by_name('input:0')
                output_tensor = detection_graph.get_tensor_by_name('output:0')

                Lflat_keypoint, Rflat_keypoint = np.array(
                    [entry for sublist in Lresult for entry in sublist]), np.array(
                    [entry for sublist in Rresult for entry in sublist])
                Lflat_keypoint, Rflat_keypoint = np.expand_dims(Lflat_keypoint, axis=0), np.expand_dims(Rflat_keypoint,
                                                                                                        axis=0)
                Loutputs = sess.run(output_tensor, feed_dict={input_tensor: Lflat_keypoint})[0]
                Routputs = sess.run(output_tensor, feed_dict={input_tensor: Rflat_keypoint})[0]  # [0] because batch维为1

            if self.show_skeleton:
                image = self.openpose.datum.cvOutputData.copy()
            else:
                image = imageToProcess.copy()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            print(image.shape)
            qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)

            end = datetime.datetime.now()
            fps = 1 / (end - start).total_seconds()

            self.single_frame.emit(qimage, float(fps), [Loutputs, Routputs])

            count += 1
            # print('biu{}~'.format(count))

    def stop(self):
        self.stop = True
        print('thread is sleeping~')
        self.terminate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    with open('qss/Ubuntu.qss') as file:
        str = file.readlines()
        str = ''.join(str).strip('\n')
        app.setStyleSheet(str)
    win.MainWindow.show()
    sys.exit(app.exec_())

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = template.MainUi()
#         self.ui.setupUi(self)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = MainWindow()
#     win.show()
#     sys.exit(app.exec_())