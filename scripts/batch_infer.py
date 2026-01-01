"""
批量推理脚本（工业必备）

典型应用：
- 产线图片文件夹
- 历史数据回溯
"""

import os
import cv2
import yaml
from fusioncode.pipeline.engine import FusionCodeEngine

def main(img_dir):
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)

    engine = FusionCodeEngine(config)

    for name in os.listdir(img_dir):
        path = os.path.join(img_dir, name)
        img = cv2.imread(path)
        if img is None:
            continue

        results = engine.run([img])
        print(name, results)

if __name__ == "__main__":
    main("data/samples")
