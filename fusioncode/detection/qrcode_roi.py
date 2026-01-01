import cv2

def detect_qrcode_rois(img):
    qr = cv2.QRCodeDetector()
    ok, _, points, _ = qr.detectAndDecodeMulti(img)
    rois = []

    if ok:
        for p in points:
            x, y, w, h = cv2.boundingRect(p.astype(int))
            rois.append(img[y:y+h, x:x+w])
    return rois
