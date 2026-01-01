"""
图像拼接模块（OpenCV）

采用策略：
- 默认 PANORAMA 模式（容错更高）
- 失败直接抛异常，由 Pipeline 兜底
"""

import cv2

def stitch_images(images: list):
    """
    拼接多张图像

    :param images: List[np.ndarray]
    :return: 拼接后的图像
    """

    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, stitched = stitcher.stitch(images)

    if status != cv2.Stitcher_OK:
        raise RuntimeError(f"Stitch failed, status={status}")

    return stitched
