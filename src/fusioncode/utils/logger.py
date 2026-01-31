"""
统一日志系统（企业级必备）

设计目标：
- 控制台 + 文件双输出
- 可配置日志等级
- 面试官一看就知道你干过真实项目
"""

import logging
import os
from datetime import datetime

def setup_logger(log_dir="logs", level="INFO"):
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("FusionCode")
    logger.setLevel(getattr(logging, level.upper()))

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s"
    )

    # 控制台
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    # 文件
    filename = datetime.now().strftime("fusioncode_%Y%m%d.log")
    fh = logging.FileHandler(os.path.join(log_dir, filename))
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
