"""
拼接前图像预处理模块

作用：
1. 提升特征点数量（工业拼接的关键）
2. 降低曝光/噪声对匹配的影响
3. 为 OpenCV Stitcher 提供“稳定输入”

工业经验：
❗ 拼接失败，80% 不是算法问题，而是输入质量问题
"""

import cv2

def preprocess_for_stitch(img):
    """
    拼接前增强

    :param img: BGR 图像
    :return: 预处理后图像
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 对比度受限自适应直方图均衡（工业常用）
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
