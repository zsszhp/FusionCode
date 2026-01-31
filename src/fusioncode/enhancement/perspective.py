"""
透视矫正模块（预留）

工业中：
- 常用于倾斜二维码
- 通常结合检测模型使用
"""

import cv2
import numpy as np

def correct_perspective(img, pts):
    """
    透视矫正
    
    :param img: 输入图像
    :param pts: 四个角点 [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
    :return: 矫正后的图像
    """
    if pts is None or len(pts) != 4:
        return img
    
    pts = np.array(pts, dtype=np.float32)
    
    # 计算目标尺寸
    width_a = np.linalg.norm(pts[0] - pts[1])
    width_b = np.linalg.norm(pts[2] - pts[3])
    max_width = max(int(width_a), int(width_b))
    
    height_a = np.linalg.norm(pts[0] - pts[3])
    height_b = np.linalg.norm(pts[1] - pts[2])
    max_height = max(int(height_a), int(height_b))
    
    # 目标点
    dst_pts = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype=np.float32)
    
    # 计算透视变换矩阵
    M = cv2.getPerspectiveTransform(pts, dst_pts)
    
    # 应用变换
    warped = cv2.warpPerspective(img, M, (max_width, max_height))
    
    return warped
