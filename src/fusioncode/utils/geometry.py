"""
几何计算工具模块

功能：
- 旋转框（OBB）相关计算
- 点集几何操作
- 变换矩阵计算

用途：
- 处理 YOLOv8_OBB 的旋转框
- 透视矫正
- ROI 提取
"""

import cv2
import numpy as np


def get_rotated_rect_corners(center: tuple, size: tuple, angle: float) -> np.ndarray:
    """
    获取旋转矩形的四个角点

    :param center: 中心点 (x, y)
    :param size: 尺寸 (width, height)
    :param angle: 旋转角度（度）
    :return: 四个角点坐标 (4, 2)
    """
    center = tuple(map(float, center))
    size = tuple(map(float, size))
    angle = float(angle)

    rect = cv2.RotatedRect(center, size, angle)
    box = cv2.boxPoints(rect)
    return np.int0(box)


def get_min_area_rect(points: np.ndarray) -> dict:
    """
    获取点集的最小外接旋转矩形

    :param points: 点集 (N, 2)
    :return: 旋转矩形信息字典
    """
    rect = cv2.minAreaRect(points)
    center, size, angle = rect

    return {
        "center": (float(center[0]), float(center[1])),
        "width": float(size[0]),
        "height": float(size[1]),
        "angle": float(angle)
    }


def get_bounding_rect(points: np.ndarray) -> tuple:
    """
    获取点集的最小外接矩形（非旋转）

    :param points: 点集 (N, 2)
    :return: (x, y, width, height)
    """
    x, y, w, h = cv2.boundingRect(points)
    return int(x), int(y), int(w), int(h)


def get_perspective_transform(src_points: np.ndarray, dst_points: np.ndarray) -> np.ndarray:
    """
    计算透视变换矩阵

    :param src_points: 源点集 (4, 2)
    :param dst_points: 目标点集 (4, 2)
    :return: 3x3 透视变换矩阵
    """
    src = np.float32(src_points)
    dst = np.float32(dst_points)
    return cv2.getPerspectiveTransform(src, dst)


def apply_perspective_transform(image: np.ndarray, M: np.ndarray, 
                                dsize: tuple = None) -> np.ndarray:
    """
    应用透视变换

    :param image: 输入图像
    :param M: 透视变换矩阵
    :param dsize: 输出图像大小 (width, height)
    :return: 变换后的图像
    """
    if dsize is None:
        dsize = (image.shape[1], image.shape[0])

    return cv2.warpPerspective(image, M, dsize)


def get_affine_transform(src_points: np.ndarray, dst_points: np.ndarray) -> np.ndarray:
    """
    计算仿射变换矩阵

    :param src_points: 源点集 (3, 2)
    :param dst_points: 目标点集 (3, 2)
    :return: 2x3 仿射变换矩阵
    """
    src = np.float32(src_points)
    dst = np.float32(dst_points)
    return cv2.getAffineTransform(src, dst)


def apply_affine_transform(image: np.ndarray, M: np.ndarray, 
                         dsize: tuple = None) -> np.ndarray:
    """
    应用仿射变换

    :param image: 输入图像
    :param M: 仿射变换矩阵
    :param dsize: 输出图像大小 (width, height)
    :return: 变换后的图像
    """
    if dsize is None:
        dsize = (image.shape[1], image.shape[0])

    return cv2.warpAffine(image, M, dsize)


def rotate_image(image: np.ndarray, angle: float, center: tuple = None) -> np.ndarray:
    """
    旋转图像

    :param image: 输入图像
    :param angle: 旋转角度（度）
    :param center: 旋转中心（默认为图像中心）
    :return: 旋转后的图像
    """
    h, w = image.shape[:2]

    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated


def crop_rotated_rect(image: np.ndarray, center: tuple, 
                     size: tuple, angle: float) -> np.ndarray:
    """
    裁剪旋转矩形区域

    :param image: 输入图像
    :param center: 中心点 (x, y)
    :param size: 尺寸 (width, height)
    :param angle: 旋转角度（度）
    :return: 裁剪并矫正后的图像
    """
    # 获取旋转矩形的四个角点
    corners = get_rotated_rect_corners(center, size, angle)

    # 计算目标尺寸
    width = int(max(size[0], size[1]))
    height = int(max(size[0], size[1]))

    # 目标点
    dst_corners = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype=np.float32)

    # 计算透视变换矩阵
    M = get_perspective_transform(corners.astype(np.float32), dst_corners)

    # 应用变换
    warped = apply_perspective_transform(image, M, (width, height))

    return warped


def calculate_iou(rect1: dict, rect2: dict) -> float:
    """
    计算两个旋转矩形的 IoU

    :param rect1: 旋转矩形1
    :param rect2: 旋转矩形2
    :return: IoU 值
    """
    corners1 = get_rotated_rect_corners(rect1["center"], 
                                       (rect1["width"], rect1["height"]), 
                                       rect1["angle"])
    corners2 = get_rotated_rect_corners(rect2["center"], 
                                       (rect2["width"], rect2["height"]), 
                                       rect2["angle"])

    # 使用 OpenCV 的 intersectConvexConvex 计算交集
    intersection_area = cv2.intersectConvexConvex(corners1, corners2)[0]

    # 计算面积
    area1 = rect1["width"] * rect1["height"]
    area2 = rect2["width"] * rect2["height"]

    union_area = area1 + area2 - intersection_area

    if union_area == 0:
        return 0.0

    return intersection_area / union_area


def nms_rotated_rects(rects: list, iou_threshold: float = 0.45) -> list:
    """
    对旋转矩形进行非极大值抑制

    :param rects: 旋转矩形列表，每个元素为字典格式
    :param iou_threshold: IoU 阈值
    :return: 抑制后的矩形列表
    """
    if len(rects) == 0:
        return []

    # 按置信度排序
    rects = sorted(rects, key=lambda x: x.get("confidence", 0), reverse=True)

    keep = []
    while rects:
        current = rects.pop(0)
        keep.append(current)

        rects = [r for r in rects if calculate_iou(current, r) < iou_threshold]

    return keep


def order_points_clockwise(points: np.ndarray) -> np.ndarray:
    """
    将四个点按顺时针顺序排列

    :param points: 四个点 (4, 2)
    :return: 排序后的点
    """
    points = points.reshape((4, 2))

    # 计算中心点
    center = np.mean(points, axis=0)

    # 计算每个点相对于中心的角度
    angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])

    # 按角度排序
    sorted_indices = np.argsort(angles)
    return points[sorted_indices]
