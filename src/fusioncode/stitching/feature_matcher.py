"""
特征匹配模块

功能：
- SIFT / ORB 特征点检测与匹配
- 作为 OpenCV Stitcher 的兜底方案
- 支持跨图条码拼接

用途：
- 当 OpenCV Stitcher 失败时使用
- 确保跨图条码能被完整识别
"""

import cv2
import numpy as np


class FeatureMatcher:
    def __init__(self, method: str = "sift", min_match_count: int = 10):
        """
        初始化特征匹配器

        :param method: 特征检测方法 ("sift" 或 "orb")
        :param min_match_count: 最小匹配点数
        """
        self.method = method.lower()
        self.min_match_count = min_match_count

        if self.method == "sift":
            self.detector = cv2.SIFT_create()
            self.matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
        elif self.method == "orb":
            self.detector = cv2.ORB_create(nfeatures=5000)
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        else:
            raise ValueError(f"Unknown method: {method}")

    def detect_and_match(self, img1: np.ndarray, img2: np.ndarray) -> tuple:
        """
        检测特征点并匹配

        :param img1: 第一张图像
        :param img2: 第二张图像
        :return: (匹配点1, 匹配点2, 匹配掩码)
        """
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2

        # 检测特征点
        kp1, des1 = self.detector.detectAndCompute(gray1, None)
        kp2, des2 = self.detector.detectAndCompute(gray2, None)

        if des1 is None or des2 is None:
            return None, None, None

        # 特征匹配
        if self.method == "sift":
            matches = self.matcher.knnMatch(des1, des2, k=2)
            good_matches = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)
        else:
            matches = self.matcher.knnMatch(des1, des2, k=2)
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

        if len(good_matches) < self.min_match_count:
            return None, None, None

        # 提取匹配点
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算单应性矩阵
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        return src_pts, dst_pts, mask

    def stitch_two_images(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        拼接两张图像

        :param img1: 第一张图像
        :param img2: 第二张图像
        :return: 拼接后的图像
        """
        src_pts, dst_pts, mask = self.detect_and_match(img1, img2)

        if src_pts is None:
            raise RuntimeError("Not enough matches found")

        # 计算单应性矩阵
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # 计算输出图像大小
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]

        # 计算变换后的图像边界
        corners1 = np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)
        corners2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)

        corners1_transformed = cv2.perspectiveTransform(corners1, M)

        all_corners = np.concatenate((corners2, corners1_transformed), axis=0)

        [x_min, y_min] = np.int32(all_corners.min(axis=0).ravel() - 0.5)
        [x_max, y_max] = np.int32(all_corners.max(axis=0).ravel() + 0.5)

        # 平移矩阵
        translation = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]])

        # 变换第一张图像
        result = cv2.warpPerspective(img1, translation.dot(M), (x_max - x_min, y_max - y_min))

        # 将第二张图像放到结果中
        result[-y_min:h2 - y_min, -x_min:w2 - x_min] = img2

        return result

    def stitch_multiple_images(self, images: list) -> np.ndarray:
        """
        拼接多张图像

        :param images: 图像列表
        :return: 拼接后的图像
        """
        if len(images) < 2:
            return images[0] if images else None

        result = images[0]
        for i in range(1, len(images)):
            try:
                result = self.stitch_two_images(result, images[i])
            except RuntimeError as e:
                print(f"Warning: Failed to stitch image {i}: {e}")
                continue

        return result


def stitch_with_feature_matching(images: list, method: str = "sift") -> np.ndarray:
    """
    使用特征匹配拼接图像的便捷函数

    :param images: 图像列表
    :param method: 特征检测方法 ("sift" 或 "orb")
    :return: 拼接后的图像
    """
    matcher = FeatureMatcher(method=method)
    return matcher.stitch_multiple_images(images)
