"""
日志模块
统一管理系统日志输出格式、等级与文件保存策略
"""

from loguru import logger
import os

def setup_logger(log_dir="logs", level="INFO"):
    """
    初始化全局日志系统
    :param log_dir: 日志保存目录
    :param level: 日志等级
    """
    os.makedirs(log_dir, exist_ok=True)

    logger.remove()
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=level
    )
    logger.add(
        os.path.join(log_dir, "fusioncode.log"),
        level=level,
        rotation="10 MB",
        encoding="utf-8"
    )

    return logger
