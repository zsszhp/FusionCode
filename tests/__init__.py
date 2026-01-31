"""
测试初始化文件
"""

import pytest
import numpy as np
import cv2


@pytest.fixture
def sample_image():
    """
    创建示例图像用于测试
    """
    return np.zeros((100, 100, 3), dtype=np.uint8)


@pytest.fixture
def sample_barcode_image():
    """
    创建示例条码图像
    """
    img = np.ones((100, 200, 3), dtype=np.uint8) * 255
    # 模拟条码
    for i in range(10, 190, 10):
        img[30:70, i:i+5] = 0
    return img


@pytest.fixture
def sample_qrcode_image():
    """
    创建示例二维码图像
    """
    img = np.ones((200, 200, 3), dtype=np.uint8) * 255
    # 模拟二维码定位点
    cv2.rectangle(img, (10, 10), (50, 50), 0, -1)
    cv2.rectangle(img, (15, 15), (45, 45), 255, -1)
    cv2.rectangle(img, (20, 20), (40, 40), 0, -1)

    cv2.rectangle(img, (140, 10), (180, 50), 0, -1)
    cv2.rectangle(img, (145, 15), (175, 45), 255, -1)
    cv2.rectangle(img, (150, 20), (170, 40), 0, -1)

    cv2.rectangle(img, (10, 140), (50, 180), 0, -1)
    cv2.rectangle(img, (15, 145), (45, 175), 255, -1)
    cv2.rectangle(img, (20, 150), (40, 170), 0, -1)
    return img
