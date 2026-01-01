# 🚀 FusionCode

<p align="center">
  <strong>工业级条码 / 二维码识别引擎</strong><br/>
  多图拼接 · 多引擎解码 · 扫码枪级鲁棒性
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue"/>
  <img src="https://img.shields.io/badge/OpenCV-4.x-green"/>
  <img src="https://img.shields.io/badge/YOLOv8-Optional-orange"/>
  <img src="https://img.shields.io/badge/License-Apache--2.0-brightgreen"/>
</p>

<p align="center">
  <a href="./README_EN.md">English Version</a> | 
  <a href="#-快速开始">快速开始</a> | 
  <a href="#-特性">特性</a> | 
  <a href="#-架构">架构</a>
</p>

---

## 📌 项目简介

**FusionCode** 是一个面向 **制造业 / 物流 / 医药 / 国企信息化场景** 的  
**工业级条码与二维码识别系统**。

本项目并不追求"单次识别最优"，而是通过 **系统级工程设计**，实现：

> ✅ **尽量不漏码，而不是只追求一次识别成功**

整体设计思想对标 **工业扫码枪与产线视觉系统**。

---

## ✨ 核心特性

- 🧩 **多图拼接识别**  
  支持多张存在重叠区域的图像拼接后统一识别

- 🎯 **高召回 ROI 定位**  
  - 传统视觉（形态学）兜底  
  - YOLOv8 深度学习模型（可选）

- 🧠 **多策略图像增强**
  - 降噪 / 锐化 / 形态学修复
  - 针对脏污、破损、模糊码设计

- 🔓 **多解码引擎并行**
  - OpenCV
  - ZBar
  - ZXing（接口预留）
  - HALCON / Dynamsoft（商业 SDK）

- 🔁 **工业级兜底与结果融合**
  - 多次尝试、多引擎并行
  - 自动去重与结果融合

---

## 🏗️ 系统架构

```
输入图像
↓
图像预处理 & 拼接
↓
ROI 定位（传统 / YOLO）
↓
多策略图像增强
↓
多解码引擎并行
↓
结果融合 & 去重
↓
最终识别结果
```

---

## 🚀 快速开始

### 环境要求

- Python >= 3.9
- OpenCV 4.x

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 运行 Demo

```bash
python scripts/run_demo.py
```

### 3️⃣ 批量图片识别

```bash
python scripts/batch_infer.py data/samples
```

---

## 🧠 YOLO 模型说明（可选）

- YOLO 在本项目中仅用于定位条码 / 二维码区域，不参与解码逻辑
- 可显著提升复杂背景下的 ROI 召回率
- 解码仍由 OpenCV / ZBar / 商业 SDK 完成

---

## 🏭 商业 SDK 支持

本项目支持以下商业 SDK（需自行购买授权）：

- MVTec HALCON
- Dynamsoft Barcode Reader

> 👉 接口已预留，可直接接入工业产线系统

---

## 📁 项目结构

```
fusioncode-vision/
├── fusioncode/        # 核心算法与引擎
├── scripts/           # 运行脚本
├── configs/           # 参数配置
├── docs/              # 设计文档
├── data/              # 示例数据
└── tests/             # 测试用例
```

---

## 🧪 适用场景

- 🏭 **制造业产线视觉系统**
- 📦 **仓储 / 物流扫码**
- 💊 **医药追溯**
- 🏢 **国企信息化项目**

---

## 📄 开源协议

本项目采用 [Apache License 2.0](./LICENSE)

> 商业 SDK 不包含在仓库中，详见 NOTICE 文件。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助我们改进项目！

---

## 📞 支持

如需技术支持或商业合作，请联系：zsszhp@163.com