"""
传统视觉检测模块

功能：
- 基于梯度 + 形态学的条码定位
- OpenCV QRCodeDetector 二维码定位
- 作为 YOLO 的兜底方案
"""

import cv2
import numpy as np
from .barcode_roi import detect_barcode_rois as detect_barcode_traditional
from .qrcode_roi import detect_qrcode_rois as detect_qrcode_traditional


def detect_barcode_rois(image: np.ndarray, method: str = "traditional") -> list:
    """
    检测条码区域

    :param image: BGR 图像
    :param method: 检测方法 ("traditional" 或 "yolo_obb")
    :return: ROI 图像列表
    """
    if method == "traditional":
        return detect_barcode_traditional(image)
    else:
        raise ValueError(f"Unknown method: {method}")


def detect_qrcode_rois(image: np.ndarray, method: str = "traditional") -> list:
    """
    检测二维码区域

    :param image: BGR 图像
    :param method: 检测方法 ("traditional" 或 "yolo_obb")
    :return: ROI 图像列表
    """
    if method == "traditional":
        return detect_qrcode_traditional(image)
    else:
        raise ValueError(f"Unknown method: {method}")


def detect_all_rois(image: np.ndarray, method: str = "traditional") -> list:
    """
    检测所有条码和二维码区域

    :param image: BGR 图像
    :param method: 检测方法
    :return: 所有 ROI 图像列表
    """
    rois = []
    rois.extend(detect_barcode_rois(image, method))
    rois.extend(detect_qrcode_rois(image, method))
    return rois
