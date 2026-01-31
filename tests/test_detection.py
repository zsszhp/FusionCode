"""
检测模块测试
"""

import pytest
import numpy as np
from fusioncode.detection.traditional import detect_barcode_rois, detect_qrcode_rois


def test_detect_barcode_rois(sample_barcode_image):
    """
    测试条码检测
    """
    rois = detect_barcode_rois(sample_barcode_image)
    assert isinstance(rois, list)


def test_detect_qrcode_rois(sample_qrcode_image):
    """
    测试二维码检测
    """
    rois = detect_qrcode_rois(sample_qrcode_image)
    assert isinstance(rois, list)


def test_detect_barcode_rois_empty():
    """
    测试空图像的条码检测
    """
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    rois = detect_barcode_rois(img)
    assert isinstance(rois, list)


def test_detect_qrcode_rois_empty():
    """
    测试空图像的二维码检测
    """
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    rois = detect_qrcode_rois(img)
    assert isinstance(rois, list)


def test_detect_barcode_rois_invalid_method():
    """
    测试无效的检测方法
    """
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    with pytest.raises(ValueError):
        detect_barcode_rois(img, method="invalid")


def test_detect_qrcode_rois_invalid_method():
    """
    测试无效的检测方法
    """
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    with pytest.raises(ValueError):
        detect_qrcode_rois(img, method="invalid")
