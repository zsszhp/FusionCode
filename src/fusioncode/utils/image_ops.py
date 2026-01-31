"""
图像通用工具函数

说明：
- 避免各模块重复造轮子
"""

import cv2

def resize_max(img, max_size=1600):
    h, w = img.shape[:2]
    scale = max(h, w) / max_size
    if scale > 1:
        img = cv2.resize(img, (int(w/scale), int(h/scale)))
    return img
