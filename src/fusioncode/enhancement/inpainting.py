"""
缺失修复模块（Inpainting）

功能：
- 修复条码/二维码的缺失区域
- 处理脏污、遮挡等场景
- 基于 OpenCV 的 inpainting 算法

适用场景：
- 条码部分被遮挡
- 二维码定位点缺失
- 图像有划痕或污渍
"""

import cv2
import numpy as np


def inpaint_missing(img: np.ndarray, mask: np.ndarray = None, method: str = "telea") -> np.ndarray:
    """
    修复图像中的缺失区域

    :param img: 输入图像
    :param mask: 缺失区域掩码（None 时自动检测）
    :param method: 修复方法 ("telea" 或 "ns")
    :return: 修复后的图像
    """
    if mask is None:
        mask = _detect_missing_regions(img)

    if mask is None or np.sum(mask) == 0:
        return img

    if method == "telea":
        inpainted = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    elif method == "ns":
        inpainted = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
    else:
        raise ValueError(f"Unknown method: {method}")

    return inpainted


def _detect_missing_regions(img: np.ndarray) -> np.ndarray:
    """
    自动检测图像中的缺失区域

    :param img: 输入图像
    :return: 缺失区域掩码
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    # 检测黑色区域（可能是缺失）
    _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    # 形态学操作去除小噪点
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # 反转得到缺失区域
    mask = cv2.bitwise_not(binary)

    return mask


def repair_barcode_gaps(img: np.ndarray, gap_threshold: int = 5) -> np.ndarray:
    """
    修复条码中的间隙

    :param img: 条码图像
    :param gap_threshold: 间隙宽度阈值
    :return: 修复后的图像
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    # 水平方向闭运算修复横向间隙
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (gap_threshold, 1))
    repaired_h = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel_h)

    # 垂直方向闭运算修复纵向间隙
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, gap_threshold))
    repaired_v = cv2.morphologyEx(repaired_h, cv2.MORPH_CLOSE, kernel_v)

    if len(img.shape) == 3:
        return cv2.cvtColor(repaired_v, cv2.COLOR_GRAY2BGR)
    return repaired_v


def enhance_qr_finder_patterns(img: np.ndarray) -> np.ndarray:
    """
    增强二维码的定位点

    :param img: 二维码图像
    :return: 增强后的图像
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    # 自适应阈值
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # 形态学闭运算填充小孔
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    enhanced = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    if len(img.shape) == 3:
        return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
    return enhanced


def remove_dirt_and_scratches(img: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    去除图像中的污渍和划痕

    :param img: 输入图像
    :param kernel_size: 中值滤波核大小
    :return: 清理后的图像
    """
    # 中值滤波去除椒盐噪声
    cleaned = cv2.medianBlur(img, kernel_size)

    # 轻微的高斯模糊平滑
    cleaned = cv2.GaussianBlur(cleaned, (3, 3), 0)

    return cleaned


def adaptive_inpaint(img: np.ndarray, confidence_threshold: float = 0.3) -> np.ndarray:
    """
    自适应修复：根据图像质量选择修复策略

    :param img: 输入图像
    :param confidence_threshold: 质量置信度阈值
    :return: 修复后的图像
    """
    # 计算图像质量指标
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # 根据质量选择修复方法
    if laplacian_var < confidence_threshold * 1000:
        # 低质量：使用更强的修复
        repaired = inpaint_missing(img, method="ns")
        repaired = repair_barcode_gaps(repaired, gap_threshold=7)
    else:
        # 高质量：使用轻度修复
        repaired = remove_dirt_and_scratches(img, kernel_size=3)

    return repaired
