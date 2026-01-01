from fusioncode.decoding.zbar_decoder import decode_zbar
from fusioncode.decoding.opencv_qr import decode_opencv_qr
from fusioncode.decoding.commercial_sdk import decode_commercial

def decode_with_all_engines(img):
    results = []
    for fn in [decode_zbar, decode_opencv_qr, decode_commercial]:
        try:
            results.extend(fn(img))
        except Exception:
            pass
    return results
