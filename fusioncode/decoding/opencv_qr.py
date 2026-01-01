import cv2

def decode_opencv_qr(img):
    qr = cv2.QRCodeDetector()
    data, pts, _ = qr.detectAndDecode(img)
    if data:
        return [{
            "type": "QR",
            "data": data,
            "engine": "opencv"
        }]
    return []
