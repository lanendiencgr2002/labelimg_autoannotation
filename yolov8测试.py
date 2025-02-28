# 导入YOLO模块和相关库
import time

import cv2
from matplotlib import pyplot as plt
from ultralytics import YOLO
import os
# 获取当前脚本的绝对路径
current_path = os.path.abspath(__file__)
# 获取脚本所在目录
script_dir = os.path.dirname(current_path)
# 切换到脚本所在目录
os.chdir(script_dir)
print('当前目录切换成功',script_dir)

def 检测并且显示图片(图片路径):
    yolo = YOLO("./last.pt", task="detect")
    result = yolo(source='uploaded_image_2.png',show=True)
    print(result[0].boxes)
    cv2.waitKey(0)
    # print(result)
if __name__ == '__main__':
    pass
