"""
商业 SDK 解码接口

支持：
- HALCON
- Dynamsoft

说明：
- 真实工业项目就是这样“条件启用”
"""

def decode_commercial(img):
    """
    示例结构，真实项目中接 SDK
    """
    results = []

    # if HALCON_AVAILABLE:
    #     results.extend(halcon_decode(img))

    # if DYNAMSOFT_AVAILABLE:
    #     results.extend(dynamsoft_decode(img))

    return results
