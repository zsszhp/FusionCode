"""
二维码 ROI 定位模块

策略：
- OpenCV 内置 QRDetector（轻量、稳定）
- 只做“定位”，不直接信任其解码
"""

import cv2

def detect_qrcode_rois(image):
    """
    定位二维码区域

    :return: List[np.ndarray]
    """

    detector = cv2.QRCodeDetector()
    retval, points = detector.detect(image)

    rois = []

    if retval and points is not None:
        pts = points[0].astype(int)
        x, y, w, h = cv2.boundingRect(pts)
        rois.append(image[y:y+h, x:x+w])

    return rois
