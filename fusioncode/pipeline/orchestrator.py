"""
多引擎调度器（Orchestrator）

职责说明：
1. 决定“用哪些方法去尝试识别”
2. 管理 ROI 检测 → 增强 → 多解码引擎
3. 实现“失败可重试、成功可叠加”的工业策略

这是整个系统鲁棒性的核心
"""

from fusioncode.detection.barcode_roi import detect_barcode_rois
from fusioncode.detection.qrcode_roi import detect_qrcode_rois

from fusioncode.enhancement.denoise import denoise
from fusioncode.enhancement.deblur import sharpen
from fusioncode.enhancement.morphology import repair

from fusioncode.decoding.zbar_decoder import decode_zbar
from fusioncode.decoding.opencv_qr import decode_opencv_qr
from fusioncode.decoding.zxing_decoder import decode_zxing
from fusioncode.decoding.commercial_sdk import decode_commercial

from fusioncode.fusion.result_merge import merge_results


class Orchestrator:
    def __init__(self, config: dict, logger):
        """
        初始化调度器

        :param config: 全局配置
        :param logger: 日志实例
        """
        self.config = config
        self.logger = logger

    def _generate_variants(self, roi):
        """
        为单个 ROI 生成多种增强版本
        工业实践：不要指望一次解码成功
        """
        variants = [roi]

        try:
            variants.append(denoise(roi))
            variants.append(sharpen(roi))
            variants.append(repair(roi))
        except Exception as e:
            self.logger.debug(f"Enhancement skipped: {e}")

        return variants

    def _decode_with_engines(self, img):
        """
        使用所有启用的解码引擎尝试解码
        """
        results = []

        if self.config["engines"]["zbar"]:
            results.extend(decode_zbar(img))

        if self.config["engines"]["opencv_qr"]:
            results.extend(decode_opencv_qr(img))

        if self.config["engines"]["zxing"]:
            results.extend(decode_zxing(img))

        if self.config["engines"]["commercial"]:
            results.extend(decode_commercial(img))

        return results

    def process(self, image):
        """
        主调度流程

        :param image: 拼接后的完整图像
        :return: 融合后的最终解码结果
        """

        self.logger.info("Orchestrator started")

        # ---------- Step 1: ROI 定位 ----------
        rois = []
        rois.extend(detect_barcode_rois(image))
        rois.extend(detect_qrcode_rois(image))

        self.logger.info(f"ROI detected: {len(rois)}")

        # ---------- Step 2: 对每个 ROI 多策略尝试 ----------
        all_results = []

        for idx, roi in enumerate(rois):
            self.logger.debug(f"Processing ROI {idx}")

            variants = self._generate_variants(roi)

            for v in variants:
                try:
                    decoded = self._decode_with_engines(v)
                    all_results.extend(decoded)
                except Exception as e:
                    self.logger.debug(f"Decode failed on variant: {e}")

        # ---------- Step 3: 结果融合 ----------
        final = merge_results(all_results)

        self.logger.info("Orchestrator finished")
        return final
