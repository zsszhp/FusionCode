from collections import defaultdict

def merge_results(results):
    bucket = defaultdict(int)
    for r in results:
        bucket[r["data"]] += 1

    final = []
    for data, cnt in bucket.items():
        final.append({
            "data": data,
            "confidence": cnt
        })
    return final
