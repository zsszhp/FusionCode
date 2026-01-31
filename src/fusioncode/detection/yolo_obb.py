"""
YOLOv8_OBB 检测器

功能：
- 支持旋转框检测（Oriented Bounding Box）
- 适用于横竖条码、二维码检测
- 与传统视觉方法结合使用

依赖：
- ultralytics >= 8.0
"""

import cv2
import numpy as np

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False


class YoloOBBDetector:
    def __init__(self, model_path: str, conf_threshold: float = 0.5, iou_threshold: float = 0.45):
        """
        初始化 YOLOv8_OBB 检测器

        :param model_path: 模型文件路径 (.pt)
        :param conf_threshold: 置信度阈值
        :param iou_threshold: IoU 阈值
        """
        if not YOLO_AVAILABLE:
            raise ImportError("ultralytics not installed. Install with: pip install ultralytics")

        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

    def detect(self, image: np.ndarray) -> list:
        """
        检测条码/二维码区域

        :param image: BGR 图像
        :return: 检测结果列表，每个元素包含旋转框信息
        """
        results = self.model.predict(
            image,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            verbose=False
        )

        detections = []
        for result in results:
            if result.obb is not None:
                boxes = result.obb.cpu().numpy()
                for box in boxes:
                    # OBB 格式: [x_center, y_center, width, height, rotation_angle]
                    x_center, y_center, width, height, angle = box[:5]
                    conf = box[5] if len(box) > 5 else self.conf_threshold
                    cls = int(box[6]) if len(box) > 6 else 0

                    detections.append({
                        "type": "obb",
                        "x_center": float(x_center),
                        "y_center": float(y_center),
                        "width": float(width),
                        "height": float(height),
                        "angle": float(angle),
                        "confidence": float(conf),
                        "class": cls
                    })

        return detections

    def extract_rois(self, image: np.ndarray, detections: list) -> list:
        """
        从检测结果中提取 ROI 图像

        :param image: 原始图像
        :param detections: 检测结果列表
        :return: ROI 图像列表
        """
        rois = []

        for det in detections:
            # 计算旋转矩形的四个角点
            center = (det["x_center"], det["y_center"])
            size = (det["width"], det["height"])
            angle = det["angle"]

            # 创建旋转矩形
            rect = cv2.RotatedRect(center, size, angle)

            # 获取四个角点
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # 计算最小外接矩形用于裁剪
            x, y, w, h = cv2.boundingRect(box)

            # 提取 ROI（带 padding）
            padding = 10
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(image.shape[1], x + w + padding)
            y2 = min(image.shape[0], y + h + padding)

            roi = image[y1:y2, x1:x2]
            rois.append(roi)

        return rois

    def get_corners(self, detection: dict) -> np.ndarray:
        """
        获取旋转框的四个角点坐标

        :param detection: 检测结果
        :return: 四个角点坐标 (4, 2)
        """
        center = (detection["x_center"], detection["y_center"])
        size = (detection["width"], detection["height"])
        angle = detection["angle"]

        rect = cv2.RotatedRect(center, size, angle)
        box = cv2.boxPoints(rect)
        return np.int0(box)


def detect_with_yolo_obb(image: np.ndarray, model_path: str, 
                          conf_threshold: float = 0.5, 
                          iou_threshold: float = 0.45) -> list:
    """
    使用 YOLOv8_OBB 检测条码/二维码的便捷函数

    :param image: BGR 图像
    :param model_path: 模型路径
    :param conf_threshold: 置信度阈值
    :param iou_threshold: IoU 阈值
    :return: ROI 图像列表
    """
    detector = YoloOBBDetector(model_path, conf_threshold, iou_threshold)
    detections = detector.detect(image)
    rois = detector.extract_rois(image, detections)
    return rois
