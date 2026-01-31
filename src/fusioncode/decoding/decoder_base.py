"""
解码器基类

功能：
- 定义统一的解码器接口
- 提供解码器的基础功能
- 方便扩展新的解码引擎
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import numpy as np


class BaseDecoder(ABC):
    """
    解码器基类
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化解码器

        :param config: 解码器配置
        """
        self.config = config or {}
        self.name = self.__class__.__name__

    @abstractmethod
    def decode(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        解码图像中的条码/二维码

        :param image: 输入图像
        :return: 解码结果列表，每个元素包含 type, data, engine 等字段
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        检查解码器是否可用

        :return: 是否可用
        """
        pass

    def decode_with_retry(self, image: np.ndarray, max_retries: int = 3) -> List[Dict[str, Any]]:
        """
        带重试的解码

        :param image: 输入图像
        :param max_retries: 最大重试次数
        :return: 解码结果列表
        """
        results = []
        for _ in range(max_retries):
            try:
                results = self.decode(image)
                if results:
                    break
            except Exception as e:
                print(f"{self.name} decode error: {e}")
                continue

        return results

    def normalize_result(self, data: str, code_type: str) -> Dict[str, Any]:
        """
        标准化解码结果

        :param data: 解码数据
        :param code_type: 码类型
        :return: 标准化的结果字典
        """
        return {
            "type": code_type,
            "data": data,
            "engine": self.name.lower(),
            "confidence": 1.0
        }


class BarcodeDecoder(BaseDecoder):
    """
    条码解码器基类
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.supported_types = self.config.get("supported_types", [])

    def supports_type(self, code_type: str) -> bool:
        """
        检查是否支持指定的码类型

        :param code_type: 码类型
        :return: 是否支持
        """
        return code_type in self.supported_types or len(self.supported_types) == 0


class QRCodeDecoder(BaseDecoder):
    """
    二维码解码器基类
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.supported_types = self.config.get("supported_types", [])

    def supports_type(self, code_type: str) -> bool:
        """
        检查是否支持指定的码类型

        :param code_type: 码类型
        :return: 是否支持
        """
        return code_type in self.supported_types or len(self.supported_types) == 0


class DecoderFactory:
    """
    解码器工厂类
    """

    _decoders = {}

    @classmethod
    def register(cls, name: str, decoder_class: type):
        """
        注册解码器

        :param name: 解码器名称
        :param decoder_class: 解码器类
        """
        cls._decoders[name] = decoder_class

    @classmethod
    def create(cls, name: str, config: Dict[str, Any] = None) -> BaseDecoder:
        """
        创建解码器实例

        :param name: 解码器名称
        :param config: 解码器配置
        :return: 解码器实例
        """
        if name not in cls._decoders:
            raise ValueError(f"Unknown decoder: {name}")

        decoder_class = cls._decoders[name]
        return decoder_class(config)

    @classmethod
    def get_available_decoders(cls) -> List[str]:
        """
        获取所有可用的解码器名称

        :return: 解码器名称列表
        """
        return list(cls._decoders.keys())
