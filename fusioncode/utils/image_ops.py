"""
抽离通用图像操作，避免代码散落
通用图像工具函数
包含缩放、旋转、裁剪等基础能力
"""

import cv2
import numpy as np

def resize_keep_ratio(img, target_long_side=1024):
    """
    等比例缩放图像，保持长宽比
    工业实践中避免直接 resize 到固定尺寸
    """
    h, w = img.shape[:2]
    scale = target_long_side / max(h, w)
    return cv2.resize(img, (int(w * scale), int(h * scale)))

def rotate_image(img, angle):
    """
    图像旋转（用于多角度解码尝试）
    """
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))
