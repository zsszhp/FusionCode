"""
HALCON 解码器模块

功能：
- 集成 MVTec HALCON 商业 SDK
- 支持多种条码和二维码类型
- 作为高精度解码引擎

依赖：
- halcon-python (需单独安装)

条码类型支持：
- Code 128, Code 39, EAN, UPC, Data Matrix, QR Code 等
"""

import numpy as np

try:
    import halcon as ha
    HALCON_AVAILABLE = True
except ImportError:
    HALCON_AVAILABLE = False


class HalconDecoder:
    def __init__(self, barcode_types: list = None, qr_types: list = None):
        """
        初始化 HALCON 解码器

        :param barcode_types: 条码类型列表
        :param qr_types: 二维码类型列表
        """
        if not HALCON_AVAILABLE:
            raise ImportError("HALCON not installed. Install halcon-python package.")

        self.barcode_types = barcode_types or [
            'Code 128', 'Code 39', 'EAN-13', 'UPC-A', 'Data Matrix ECC 200'
        ]
        self.qr_types = qr_types or ['QR Code']

        self.handle = None

    def _create_barcode_model(self):
        """
        创建条码识别模型
        """
        handle = ha.CreateBarCodeModel([], [])
        for code_type in self.barcode_types:
            ha.SetBarCodeParam(handle, 'code_type', code_type)
        return handle

    def _create_qr_model(self):
        """
        创建二维码识别模型
        """
        handle = ha.CreateDataCode2dModel(self.qr_types[0], [], [])
        return handle

    def decode(self, image: np.ndarray) -> list:
        """
        解码条码和二维码

        :param image: BGR 图像
        :return: 解码结果列表
        """
        results = []

        try:
            # 转换为 HALCON 图像格式
            h, w = image.shape[:2]
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            halcon_image = ha.GenImage1(byte, w, h, image.tobytes())

            # 解码条码
            barcode_handle = self._create_barcode_model()
            try:
                decoded, _ = ha.FindBarCode(halcon_image, barcode_handle, [], [])
                for i in range(len(decoded)):
                    results.append({
                        "type": "BARCODE",
                        "data": decoded[i],
                        "engine": "halcon"
                    })
            finally:
                ha.ClearBarCodeModel(barcode_handle)

            # 解码二维码
            qr_handle = self._create_qr_model()
            try:
                decoded, _, _ = ha.FindDataCode2d(halcon_image, qr_handle, [], [], [], [], [], [])
                for i in range(len(decoded)):
                    results.append({
                        "type": "QR",
                        "data": decoded[i],
                        "engine": "halcon"
                    })
            finally:
                ha.ClearDataCode2dModel(qr_handle)

        except Exception as e:
            print(f"HALCON decode error: {e}")

        return results

    def decode_with_roi(self, image: np.ndarray, roi: tuple) -> list:
        """
        在指定 ROI 区域内解码

        :param image: BGR 图像
        :param roi: ROI 区域 (x, y, width, height)
        :return: 解码结果列表
        """
        x, y, w, h = roi
        roi_image = image[y:y+h, x:x+w]
        return self.decode(roi_image)


def decode_halcon(image: np.ndarray, barcode_types: list = None, qr_types: list = None) -> list:
    """
    使用 HALCON 解码的便捷函数

    :param image: BGR 图像
    :param barcode_types: 条码类型列表
    :param qr_types: 二维码类型列表
    :return: 解码结果列表
    """
    if not HALCON_AVAILABLE:
        return []

    decoder = HalconDecoder(barcode_types, qr_types)
    return decoder.decode(image)
