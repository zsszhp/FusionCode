"""
OpenCV QR 解码

优点：
- 无外部依赖
- 快速兜底
"""

import cv2

def decode_opencv_qr(img):
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if data:
        return [{
            "type": "QR",
            "data": data,
            "engine": "opencv"
        }]

    return []
