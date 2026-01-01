from fusioncode.stitching.stitcher import stitch_images
from fusioncode.detection.barcode_roi import detect_barcode_rois
from fusioncode.detection.qrcode_roi import detect_qrcode_rois
from fusioncode.pipeline.orchestrator import decode_with_all_engines
from fusioncode.fusion.result_merge import merge_results

class FusionCodeEngine:

    def run(self, images):
        stitched = stitch_images(images)

        bar_rois = detect_barcode_rois(stitched)
        qr_rois = detect_qrcode_rois(stitched)

        all_results = []

        for roi in bar_rois + qr_rois:
            all_results.extend(decode_with_all_engines(roi))

        return merge_results(all_results)
