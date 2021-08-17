import sys
import cv2
import os
from sys import platform
import argparse
import datetime
import tensorflow as tf
import numpy as np

from utils.fileio import prepare_data

class PyOpenpose():
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))  # 括号里是当前脚本的绝对路径，加dirname之后是当前脚本所在文件夹的绝对路径
        try:
            # Windows Import
            if platform == "win32":  # 判断是windows系统
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append(self.dir_path + '/../build/python/openpose/Release')
                os.environ['PATH'] = os.environ[
                                         'PATH'] + ';' + self.dir_path + '/../build/x64/Release;' + self.dir_path + '/../build/bin;'
                import pyopenpose as op
            else:
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append('../build/python')
                # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
                # sys.path.append('/usr/local/python')
                from openpose import pyopenpose as op
        except ImportError as e:
            print(
                'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        # Flags
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--image_path", default="../examples/media/img246.jpg",
                            help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
        args = self.parser.parse_known_args()  # https://www.cnblogs.com/wanghui-garcia/p/11267160.html

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        self.params = dict()
        self.params["model_folder"] = "../models/"
        self.params["hand"] = True
        self.params["hand_detector"] = 2
        self.params["body"] = 0

        # Add others in path?
        for i in range(0, len(args[1])):  # args[1]'s len is 0
            curr_item = args[1][i]
            if i != len(args[1]) - 1:
                next_item = args[1][i + 1]
            else:
                next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-', '')
                if key not in self.params:  self.params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-', '')
                if key not in self.params: self.params[key] = next_item

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(self.params)
        self.opWrapper.start()
        print('读取模型成功')

        self.datum = op.Datum()
        self.datum.handRectangles = [
            [
                op.Rectangle(10, 30, 180, 180),
                op.Rectangle(130, 30, 180, 180),
            ]
        ]
