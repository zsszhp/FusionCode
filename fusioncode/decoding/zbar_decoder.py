from pyzbar.pyzbar import decode

def decode_zbar(img):
    res = []
    for r in decode(img):
        res.append({
            "type": r.type,
            "data": r.data.decode(),
            "engine": "zbar"
        })
    return res
