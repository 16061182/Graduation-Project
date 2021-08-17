from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import cv2
import sys
import tensorflow as tf
import numpy as np
import os
import datetime

from ui import template
from utils.fileio import prepare_data
from ui.eva import PyOpenpose

class MainWindow(object):
    def __init__(self):
        self.MainWindow = QMainWindow()
        self.ui = template.Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.initUi()

        self.MainWindow.setWindowTitle('基于第一人称视频的手部操作动作识别')
        self.startThread()

    def initUi(self):
        self.ui.show_skeleton.toggle()
        self.setCheckbox()

        self.scene = 0 # ['对接线缆', '器件切割、打孔等', '使用移液枪', '使用移液枪（有精度要求）', '使用胶枪（大）', '使用胶枪（小）']
        self.ui.scene_select.currentIndexChanged.connect(self.change_scene)

        qpixmap0 = QPixmap('./icon/status_0.png')
        qpixmap1 = QPixmap('./icon/status_1.png')
        qpixmap2 = QPixmap('./icon/status_2.png')
        qpixmap3 = QPixmap('./icon/status_3.png')
        self.qpixmap = [qpixmap0, qpixmap1, qpixmap2, qpixmap3]

    def change_scene(self, i): # i是条目索引
        self.scene = i

    def startThread(self):
        self.stop = False
        self.posenames = ['手持线缆', '扶/按压', '胶枪（小）', '胶枪（大）','移液枪（垂直）', '移液枪（倾斜）']
        self.threshold = 0.4
        self.thread = RunThread(parent=None)
        self.thread.start()
        self.thread.single_frame.connect(self.show_image)

    def judge_status(self, LPose, RPose): # 0-安全 1-警告 2-危险 3-未知
        if LPose == '未定义' and RPose == '未定义':
            return 3, '未知动作'
        if self.scene == 0: # 对接线缆
            if (LPose == '手持线缆' and RPose == '手持线缆') or (LPose == '手持线缆' and RPose == '扶/按压') or (LPose == '扶/按压' and RPose == '手持线缆'):
                return 0, '动作正确'
            else:
                return 1, '请拿好、扶稳线缆'
        elif self.scene == 1: # 器件切割、打孔等
            if (LPose == '扶/按压' and RPose == '扶/按压'):
                return 0, '动作正确'
            else:
                return 2, '请扶稳器件！'
        elif self.scene == 2: # 使用移液枪
            if LPose == '移液枪（垂直）' or RPose == '移液枪（垂直）' or LPose == '移液枪（倾斜）' or RPose == '移液枪（倾斜）':
                return 0, '动作正确'
            else:
                return 1, '请拿好移液枪'
        elif self.scene == 3: # 使用移液枪（有精度要求）
            if LPose == '移液枪（垂直）' or RPose == '移液枪（垂直）':
                return 0, '动作正确'
            else:
                return 1, '请垂直拿好移液枪'
        elif self.scene == 4: # 使用胶枪（大）
            if (LPose == '胶枪（大）' and RPose != '胶枪（小）') or (LPose != '胶枪（小）' and RPose == '胶枪（大）'):
                return 0, '动作正确'
            elif LPose == '胶枪（小）' or RPose == '胶枪（小）':
                return 1, '请用四指同时扣动扳机'
            else:
                return 1, '请拿好胶枪'
        else: # 使用胶枪（小）
            if LPose == '胶枪（小）' or RPose == '胶枪（小）':
                return 0, '动作正确'
            else:
                return 1, '请拿好胶枪'

    def show_image(self, qimage, fps, infer):
        if not self.stop:
            pixmap = QPixmap.fromImage(qimage)
            self.ui.image.setPixmap(pixmap)
            self.ui.statusbar.showMessage('fps:{}'.format(fps))
            Lmax_index, Rmax_index = np.argmax(infer[0]), np.argmax(infer[1])
            Lscore_index = Lmax_index if infer[0][Lmax_index] >= self.threshold else -1
            Rscore_index = Rmax_index if infer[1][Rmax_index] >= self.threshold else -1
            LPose = '未定义' if Lscore_index == -1 else self.posenames[Lscore_index]
            RPose = '未定义' if Rscore_index == -1 else self.posenames[Rscore_index]

            self.ui.left_pose.setText('左手动作：' + LPose)
            self.ui.duijie_lbar.setValue(infer[0][0] * 100)
            self.ui.duijie_lnum.display('%.2f' % infer[0][0])
            self.ui.fuzhe_lbar.setValue(infer[0][1] * 100)
            self.ui.fuzhe_lnum.display('%.2f' % infer[0][1])
            self.ui.jq_danzhi_lbar.setValue(infer[0][2] * 100)
            self.ui.jq_danzhi_lnum.display('%.2f' % infer[0][2])
            self.ui.jq_sizhi_lbar.setValue(infer[0][3] * 100)
            self.ui.jq_sizhi_lnum.display('%.2f' % infer[0][3])
            self.ui.yyq_chuizhi_lbar.setValue(infer[0][4] * 100)
            self.ui.yyq_chuizhi_lnum.display('%.2f' % infer[0][4])
            self.ui.yyq_qingxie_lbar.setValue(infer[0][5] * 100)
            self.ui.yyq_qingxie_lnum.display('%.2f' % infer[0][5])

            self.ui.right_pose.setText('右手动作：' + RPose)
            self.ui.duijie_rbar.setValue(infer[1][0] * 100)
            self.ui.duijie_rnum.display('%.2f' % infer[1][0])
            self.ui.fuzhe_rbar.setValue(infer[1][1] * 100)
            self.ui.fuzhe_rnum.display('%.2f' % infer[1][1])
            self.ui.jq_danzhi_rbar.setValue(infer[1][2] * 100)
            self.ui.jq_danzhi_rnum.display('%.2f' % infer[1][2])
            self.ui.jq_sizhi_rbar.setValue(infer[1][3] * 100)
            self.ui.jq_sizhi_rnum.display('%.2f' % infer[1][3])
            self.ui.yyq_chuizhi_rbar.setValue(infer[1][4] * 100)
            self.ui.yyq_chuizhi_rnum.display('%.2f' % infer[1][4])
            self.ui.yyq_qingxie_rbar.setValue(infer[1][5] * 100)
            self.ui.yyq_qingxie_rnum.display('%.2f' % infer[1][5])

            status, message = self.judge_status(LPose, RPose)
            self.ui.icon.setPixmap(self.qpixmap[status])
            self.ui.icon_text.setText(message)

    def setCheckbox(self):
        self.ui.show_skeleton.stateChanged.connect(self.showSkeleton)
        self.ui.show_box.stateChanged.connect(self.showBox)

    def showSkeleton(self, state):
        if state == Qt.Checked:
            self.thread.show_skeleton = True
        else:
            self.thread.show_skeleton = False

    def showBox(self, state):
        if state == Qt.Checked:
            self.thread.show_box = True
        else:
            self.thread.show_box = False


class RunThread(QThread):
    single_frame = pyqtSignal(QImage, float, list)

    def __init__(self, parent=None):
        super(RunThread, self).__init__(parent)
        self.stop = False
        self.openpose = PyOpenpose()
        self.show_skeleton = True
        self.show_box = False
        print('线程初始化完成')

    def run(self):
        # Start Webcam
        source = 'C:\\Users\\98341\\Pictures\\Camera Roll\\WIN_20200603_15_41_58_Pro.mp4'
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
        count = 0
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # 屏蔽tensorflow通知信息

        print('进入循环')
        total_fps = 0
        # Start Evaluation
        while (not self.stop):
            start = datetime.datetime.now()
            # print('推理开始')
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

            if self.show_box:
                cv2.rectangle(image, (10, 30), (190, 210), (255, 0, 0), 2)
                cv2.rectangle(image, (130, 30), (310, 210), (0, 0, 255), 2)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # print(image.shape)
            qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)

            end = datetime.datetime.now()
            # print('推理：{}'.format((end-start).total_seconds()))
            fps = 1 / (end - start).total_seconds()

            self.single_frame.emit(qimage, float(fps), [Loutputs, Routputs])

            count += 1
            total_fps += fps
            if count == 100:
                print('平均fps: {}'.format(total_fps / 100))
            # print('biu{}~'.format(count))

    def stop(self):
        self.stop = True
        print('停止')
        self.terminate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    with open('qss/MaterialDark.qss') as file:
        str = file.readlines()
        str = ''.join(str).strip('\n')
        app.setStyleSheet(str)
    win.MainWindow.show()
    sys.exit(app.exec_())
