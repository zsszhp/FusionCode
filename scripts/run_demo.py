import cv2
from fusioncode.pipeline.engine import FusionCodeEngine

imgs = [
    cv2.imread("data/samples/img1.jpg"),
    cv2.imread("data/samples/img2.jpg"),
]

engine = FusionCodeEngine()
results = engine.run(imgs)

print("Final Results:")
for r in results:
    print(r)
