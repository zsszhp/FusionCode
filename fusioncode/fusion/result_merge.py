"""
解码结果融合模块

工业核心思想：
❗ 同一个码，可能被多次、多引擎识别
❗ 目标不是“最多结果”，而是“最准结果”
"""

def merge_results(results: list):
    """
    根据 data 去重，保留最可信结果
    """

    merged = {}
    for r in results:
        key = r["data"]
        if key not in merged:
            merged[key] = r

    return list(merged.values())
