"""
降噪模块

工业推荐：
- 保边降噪优于高斯模糊
"""

import cv2

def denoise(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
