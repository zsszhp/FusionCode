"""
去模糊 / 锐化模块

适用场景：
- 轻微运动模糊
- 低清晰度摄像头
"""

import cv2
import numpy as np

def sharpen(img):
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    return cv2.filter2D(img, -1, kernel)
