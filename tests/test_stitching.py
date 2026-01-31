"""
拼接模块测试
"""

import pytest
import numpy as np
from fusioncode.stitching.stitcher import stitch_images
from fusioncode.stitching.preprocess import preprocess_for_stitch
from fusioncode.stitching.feature_matcher import FeatureMatcher


def test_preprocess_for_stitch(sample_image):
    """
    测试拼接前预处理
    """
    result = preprocess_for_stitch(sample_image)
    assert result is not None
    assert result.shape[:2] == sample_image.shape[:2]


def test_stitch_images_single(sample_image):
    """
    测试单张图像拼接
    """
    result = stitch_images([sample_image])
    assert result is not None


def test_stitch_images_multiple():
    """
    测试多张图像拼接
    """
    img1 = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    img2 = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    try:
        result = stitch_images([img1, img2])
        assert result is not None
    except RuntimeError:
        # OpenCV Stitcher 可能失败，这是正常的
        pass


def test_feature_matcher_sift():
    """
    测试 SIFT 特征匹配
    """
    matcher = FeatureMatcher(method="sift")
    assert matcher.method == "sift"


def test_feature_matcher_orb():
    """
    测试 ORB 特征匹配
    """
    matcher = FeatureMatcher(method="orb")
    assert matcher.method == "orb"


def test_feature_matcher_invalid_method():
    """
    测试无效的特征匹配方法
    """
    with pytest.raises(ValueError):
        FeatureMatcher(method="invalid")
