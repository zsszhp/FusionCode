"""
单次 Demo 运行入口

一行命令跑完整流程：
python scripts/run_demo.py
"""

import cv2
import yaml
from fusioncode.pipeline.engine import FusionCodeEngine

def main():
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)

    engine = FusionCodeEngine(config)

    images = [
        cv2.imread("data/samples/img1.jpg"),
        cv2.imread("data/samples/img2.jpg"),
        cv2.imread("data/samples/img3.jpg"),
    ]

    results = engine.run(images)

    print("\n==== Final Results ====")
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
