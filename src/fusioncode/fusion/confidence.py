"""
置信度评估模块（预留）

工业项目中：
- 不同引擎可信度不同
- 商业 SDK > 开源 > 传统
"""

ENGINE_CONFIDENCE = {
    "commercial": 0.95,
    "halcon": 0.95,
    "zbar": 0.85,
    "opencv": 0.75,
    "zxing": 0.80
}

def score(result):
    return ENGINE_CONFIDENCE.get(result["engine"], 0.5)
