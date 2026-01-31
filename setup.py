"""
FusionCode 安装脚本

使用方法：
pip install -e .
"""

from setuptools import setup, find_packages
import os

# 读取 README 文件
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="fusioncode",
    version="1.0.0",
    description="工业级条码/二维码识别系统",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="FusionCode Team",
    author_email="zsszhp@163.com",
    url="https://github.com/yourusername/fusioncode",
    license="Apache-2.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "opencv-python>=4.8",
        "numpy>=1.23",
        "pyzbar>=0.1.9",
        "pyyaml>=6.0",
        "tqdm>=4.66",
        "torch>=2.0",
        "torchvision>=0.15",
        "ultralytics>=8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
        "halcon": [
            "halcon-python>=23.11",
        ],
        "dynamsoft": [
            "dynamsoft-barcode-reader>=10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fusioncode-demo=scripts.run_demo:main",
            "fusioncode-batch=scripts.batch_infer:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="barcode qrcode yolo halcon opencv computer-vision",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/fusioncode/issues",
        "Source": "https://github.com/yourusername/fusioncode",
    },
)
