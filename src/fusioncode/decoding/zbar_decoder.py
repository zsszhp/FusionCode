"""
ZBar 解码器（条码核心兜底）

优点：
- 对脏污、破损容忍度高
"""

from pyzbar import pyzbar

def decode_zbar(img):
    results = []
    decoded = pyzbar.decode(img)

    for d in decoded:
        results.append({
            "type": d.type,
            "data": d.data.decode("utf-8"),
            "engine": "zbar"
        })

    return results
