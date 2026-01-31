"""
解码模块测试
"""

import pytest
import numpy as np
from fusioncode.decoding.zbar_decoder import decode_zbar
from fusioncode.decoding.opencv_qr import decode_opencv_qr


def test_decode_zbar(sample_image):
    """
    测试 ZBar 解码
    """
    results = decode_zbar(sample_image)
    assert isinstance(results, list)


def test_decode_opencv_qr(sample_image):
    """
    测试 OpenCV QR 解码
    """
    results = decode_opencv_qr(sample_image)
    assert isinstance(results, list)


def test_decode_zbar_empty():
    """
    测试空图像的 ZBar 解码
    """
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    results = decode_zbar(img)
    assert isinstance(results, list)
    assert len(results) == 0


def test_decode_opencv_qr_empty():
    """
    测试空图像的 OpenCV QR 解码
    """
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    results = decode_opencv_qr(img)
    assert isinstance(results, list)
    assert len(results) == 0
