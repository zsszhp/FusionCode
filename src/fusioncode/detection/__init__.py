"""
检测模块
"""

from .yolo_obb import YoloOBBDetector, detect_with_yolo_obb
from .traditional import detect_barcode_rois, detect_qrcode_rois, detect_all_rois
from .barcode_roi import detect_barcode_rois as detect_barcode_traditional
from .qrcode_roi import detect_qrcode_rois as detect_qrcode_traditional

__all__ = [
    'YoloOBBDetector',
    'detect_with_yolo_obb',
    'detect_barcode_rois',
    'detect_qrcode_rois',
    'detect_all_rois',
    'detect_barcode_traditional',
    'detect_qrcode_traditional'
]
