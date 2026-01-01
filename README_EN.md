# 🚀 FusionCode

<p align="center">
  <strong>Industrial-Grade Barcode / QR Code Recognition Engine</strong><br/>
  Multi-Image Stitching · Multi-Engine Decoding · Industrial Scanner Robustness
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue"/>
  <img src="https://img.shields.io/badge/OpenCV-4.x-green"/>
  <img src="https://img.shields.io/badge/YOLOv8-Optional-orange"/>
  <img src="https://img.shields.io/badge/License-Apache--2.0-brightgreen"/>
</p>

<p align="center">
  <a href="./README.md">中文版本</a> | 
  <a href="#-quick-start">Quick Start</a> | 
  <a href="#-features">Features</a> | 
  <a href="#-architecture">Architecture</a>
</p>

---

## 📌 Project Introduction

**FusionCode** is an **industrial-grade barcode and QR code recognition system** designed for **manufacturing / logistics / pharmaceutical / state enterprise information system scenarios**.

This project does not pursue "optimal single recognition", but instead achieves through **system-level engineering design**:

> ✅ **Minimize missed codes rather than just pursuing single recognition success**

The overall design concept is aligned with **industrial barcode scanners and production line vision systems**.

---

## ✨ Core Features

- 🧩 **Multi-Image Stitching Recognition**  
  Supports stitching and unified recognition of multiple images with overlapping areas

- 🎯 **High-Recall ROI Localization**  
  - Traditional computer vision (morphology) fallback  
  - YOLOv8 deep learning model (optional)

- 🧠 **Multi-Strategy Image Enhancement**
  - Denoising / Sharpening / Morphological restoration
  - Designed for dirty, damaged, and blurry codes

- 🔓 **Parallel Multi-Decoding Engine**
  - OpenCV
  - ZBar
  - ZXing (interface reserved)
  - HALCON / Dynamsoft (commercial SDK)

- 🔁 **Industrial-Grade Fallback and Result Fusion**
  - Multiple attempts, parallel multi-engine
  - Automatic deduplication and result fusion

---

## 🏗️ System Architecture

```
Input Image
↓
Image Preprocessing & Stitching
↓
ROI Localization (Traditional / YOLO)
↓
Multi-Strategy Image Enhancement
↓
Parallel Multi-Decoding Engine
↓
Result Fusion & Deduplication
↓
Final Recognition Result
```

---

## 🚀 Quick Start

### Requirements

- Python >= 3.9
- OpenCV 4.x

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run Demo

```bash
python scripts/run_demo.py
```

### 3️⃣ Batch Image Recognition

```bash
python scripts/batch_infer.py data/samples
```

---

## 🧠 YOLO Model Notes (Optional)

- YOLO in this project is only used for locating barcode / QR code regions, not involved in decoding logic
- Significantly improves ROI recall rate in complex backgrounds
- Decoding is still performed by OpenCV / ZBar / Commercial SDK

---

## 🏭 Commercial SDK Support

This project supports the following commercial SDKs (authorization needs to be purchased separately):

- MVTec HALCON
- Dynamsoft Barcode Reader

> 👉 Interfaces are reserved and can be directly integrated into industrial production line systems

---

## 📁 Project Structure

```
fusioncode-vision/
├── fusioncode/        # Core algorithms and engines
├── scripts/           # Execution scripts
├── configs/           # Configuration parameters
├── docs/              # Design documentation
├── data/              # Sample data
└── tests/             # Test cases
```

---

## 🧪 Application Scenarios

- 🏭 **Manufacturing Production Line Vision Systems**
- 📦 **Warehouse / Logistics Scanning**
- 💊 **Pharmaceutical Traceability**
- 🏢 **State Enterprise Information Systems**

---

## 📄 License

This project is licensed under [Apache License 2.0](./LICENSE)

> Commercial SDKs are not included in the repository, please see NOTICE file for details.

---

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to help us improve the project!

---

## 📞 Support

For technical support or commercial cooperation, please contact: zsszhp@163.com