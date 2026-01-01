"""
条形码 ROI 定位模块

当前实现：
- 传统视觉兜底方案（形态学）
- 后续可直接接入 YOLO

为什么不用“只 YOLO”？
👉 工业中必须有非学习兜底方案
"""

import cv2
import numpy as np

def detect_barcode_rois(image):
    """
    基于梯度 + 形态学的条码定位

    :return: List[np.ndarray] ROI 图像
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    blurred = cv2.blur(gradient, (9, 9))
    _, thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    cnts, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rois = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w > 50 and h > 20:
            rois.append(image[y:y+h, x:x+w])

    return rois
