def decode_commercial(img):
    """
    Unified entry for commercial SDKs.
    """
    results = []

    try:
        import dbr
        # Dynamsoft example
        # reader = BarcodeReader()
        # results.extend(...)
    except ImportError:
        pass

    try:
        import halcon
        # HALCON example
    except ImportError:
        pass

    return results
