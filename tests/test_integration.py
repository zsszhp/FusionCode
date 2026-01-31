"""
集成测试
"""

import pytest
import numpy as np
from fusioncode.core.engine import FusionCodeEngine


def test_engine_initialization():
    """
    测试引擎初始化
    """
    config = {
        "logging": {
            "log_dir": "logs",
            "level": "INFO"
        },
        "pipeline": {
            "enable_stitching": True,
            "enable_enhancement": True,
            "enable_commercial_sdk": False
        },
        "engines": {
            "zbar": {"enable": True},
            "opencv_qr": {"enable": True},
            "zxing": {"enable": False},
            "commercial": {"enable": False},
            "halcon": {"enable": False}
        }
    }
    
    engine = FusionCodeEngine(config)
    assert engine is not None
    assert engine.config == config


def test_engine_run_single_image():
    """
    测试引擎运行（单张图像）
    """
    config = {
        "logging": {
            "log_dir": "logs",
            "level": "INFO"
        },
        "pipeline": {
            "enable_stitching": False,
            "enable_enhancement": True,
            "enable_commercial_sdk": False
        },
        "engines": {
            "zbar": {"enable": True},
            "opencv_qr": {"enable": True},
            "zxing": {"enable": False},
            "commercial": {"enable": False},
            "halcon": {"enable": False}
        }
    }
    
    engine = FusionCodeEngine(config)
    img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    results = engine.run([img])
    assert isinstance(results, list)
