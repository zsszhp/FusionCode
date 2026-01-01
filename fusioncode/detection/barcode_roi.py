import cv2

def detect_barcode_rois(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    grad = cv2.convertScaleAbs(grad)

    _, bw = cv2.threshold(grad, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 7))
    closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    cnts, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

    rois = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w / h > 2:
            rois.append(img[y:y+h, x:x+w])
    return rois
