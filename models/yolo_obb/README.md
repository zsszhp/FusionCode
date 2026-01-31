# 模型说明

本目录用于存放 YOLOv8_OBB 模型文件。

## 模型文件

### barcode_qrcode.pt

用于检测条形码和二维码的 YOLOv8_OBB 模型。

- **模型类型**: YOLOv8-OBB (Oriented Bounding Box)
- **输入尺寸**: 640x640
- **检测类别**: 
  - 0: 条形码
  - 1: 二维码

## 模型下载

如果模型文件不存在，请从以下方式获取：

### 方式 1: 使用预训练模型

```bash
# 从 Ultralytics 下载预训练模型
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-obb.pt -O models/yolo_obb/barcode_qrcode.pt
```

### 方式 2: 训练自定义模型

```bash
# 准备数据集
# 参考 docs/training.md

# 训练模型
python scripts/train_yolo.py --data data/train.yaml --model yolov8n-obb.pt --epochs 100
```

## 模型配置

在 `configs/detection.yaml` 中配置模型路径：

```yaml
detection:
  yolo_obb:
    model_path: models/yolo_obb/barcode_qrcode.pt
    conf_threshold: 0.5
    iou_threshold: 0.45
    enable: true
```

## 模型性能

| 模型 | mAP@50 | 推理速度 (ms) | 参数量 |
|-------|---------|---------------|--------|
| YOLOv8n-OBB | 45.2 | 1.5 | 3.2M |
| YOLOv8s-OBB | 53.7 | 2.5 | 11.2M |
| YOLOv8m-OBB | 59.8 | 5.0 | 25.9M |

推荐使用 YOLOv8n-OBB 以获得最佳的速度-精度平衡。

## 注意事项

1. 模型文件较大（约 6MB），请确保有足够的磁盘空间
2. 首次运行时会自动下载模型（如果配置了自动下载）
3. 可以根据实际需求调整置信度阈值和 IoU 阈值
