"""
FusionCode 主引擎

职责说明（非常重要）：
1. 作为系统唯一对外入口
2. 串联拼接、检测、增强、解码、融合各阶段
3. 控制配置、生效策略与异常兜底
4. 保证系统“尽量不漏码，而不是追求单次完美”

设计原则：
- 所有模块“可插拔”
- 任意模块失败，不导致系统整体崩溃
"""

from fusioncode.utils.logger import setup_logger
from fusioncode.stitching.stitcher import stitch_images
from fusioncode.stitching.preprocess import preprocess_for_stitch
from fusioncode.pipeline.orchestrator import Orchestrator

class FusionCodeEngine:
    def __init__(self, config: dict):
        """
        初始化主引擎

        :param config: 来自 yaml 的全局配置字典
        """
        self.config = config
        self.logger = setup_logger(
            log_dir=config["logging"]["log_dir"],
            level=config["logging"]["level"]
        )
        self.orchestrator = Orchestrator(config, self.logger)

        self.logger.info("FusionCodeEngine initialized\n")

    def run(self, images: list):
        """
        系统主执行入口

        :param images: 输入图片列表（BGR 格式，OpenCV 读取）
        :return: 最终解码结果（已融合、去重）
        """

        self.logger.info(f"Pipeline started, input images: {len(images)}")

        # ---------- Step 1: 预处理（拼接前） ----------
        processed_imgs = []
        for idx, img in enumerate(images):
            try:
                p = preprocess_for_stitch(img)
                processed_imgs.append(p)
            except Exception as e:
                self.logger.warning(f"Preprocess failed on image {idx}: {e}")

        if not processed_imgs:
            raise RuntimeError("All input images failed preprocessing")

        # ---------- Step 2: 图像拼接 ----------
        if self.config["pipeline"]["enable_stitching"]:
            try:
                stitched = stitch_images(processed_imgs)
                self.logger.info("Image stitching succeeded")
            except Exception as e:
                self.logger.warning(f"Stitching failed, fallback to first image: {e}")
                stitched = processed_imgs[0]
        else:
            stitched = processed_imgs[0]

        # ---------- Step 3: 交给调度器处理 ----------
        final_results = self.orchestrator.process(stitched)

        self.logger.info(f"Pipeline finished, results count: {len(final_results)}")
        return final_results
