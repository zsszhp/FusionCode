import cv2
import numpy as np

def warp_by_points(img, pts):
    pts = pts.astype("float32")
    x,y,w,h = cv2.boundingRect(pts.astype(int))
    dst = np.array([
        [0,0],[w,0],[w,h],[0,h]
    ], dtype="float32")
    M = cv2.getPerspectiveTransform(pts, dst)
    return cv2.warpPerspective(img, M, (w, h))
