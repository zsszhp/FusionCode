import cv2

def preprocess_for_stitch(img):
    """
    Enhance image quality before stitching.
    Industrial practice: improve contrast, suppress illumination noise.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(2.0, (8, 8))
    enhanced = clahe.apply(gray)
    return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
