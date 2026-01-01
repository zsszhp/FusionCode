import cv2

def repair(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
