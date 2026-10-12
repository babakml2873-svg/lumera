"""Flag variant images that the source re-uses for *different* products (series/family photos).

A V image whose pHash equals the V image of another SKU taken from a different source page is not
proof of that exact SKU (e.g. one breaker photo for 15-100 A ratings), so it is downgraded to Medium
(OK-REVIEW-RECOMMENDED) with a note naming the other SKUs.  Same-page sharing (variants that differ only
in non-visual options) is left alone.

Enabled per brand with config.json {"shared_v_check": true}.
usage: python3 shared_v.py "<Brand>" [--apply]   (run_brand.py calls flag_shared() itself)
"""
import json, sys
from collections import defaultdict

import imagehash
from PIL import Image

from common import OUT, WORK, brand_dir, slug

NOTE = "source uses this same photo for other products"


def flag_shared(plan, results, bdir, max_dist=2):
    v = [r for r in results if r["type"] == "V" and r["file"]]
    hs = {id(r): imagehash.phash(Image.open(OUT / r["list"] / bdir / r["file"])) for r in v}
    groups = defaultdict(list)
    for r in v:  # bucket by exact hash first, then merge near-identical buckets
        groups[str(hs[id(r)])].append(r)
    keys = list(groups)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if groups[a] and groups[b] and imagehash.hex_to_hash(a) - imagehash.hex_to_hash(b) <= max_dist:
                groups[a] += groups[b]; groups[b] = []
    pl = {("List_" + p["list"].replace("List", ""), p["sku"]): p for p in plan}
    n = 0
    for g in groups.values():
        if len({r["page"].split("?")[0] for r in g}) < 2:
            continue
        for r in g:
            others = sorted({x["sku"] for x in g if x["page"].split("?")[0] != r["page"].split("?")[0]})
            rec = pl[(r["list"], r["sku"])]
            if NOTE in rec["note"]:
                continue
            shown = ", ".join(others[:5]) + (f" +{len(others) - 5} more" if len(others) > 5 else "")
            rec["note"] += f"; {NOTE} ({shown}) - series/family photo, printed ratings or details may differ"
            if rec["conf"] == "High":
                rec["conf"] = "Medium"
            n += 1
    return n


if __name__ == "__main__":
    b = sys.argv[1]
    W = WORK / ("abba" if b == "ABBA Lighting" else slug(b))
    plan = json.load(open(W / "plan_final.json")); res = json.load(open(W / "results.json"))
    n = flag_shared(plan, res, brand_dir(b))
    print(b, "flagged", n, "of", sum(1 for r in res if r["type"] == "V" and r["file"]))
    if "--apply" in sys.argv:
        json.dump(plan, open(W / "plan_final.json", "w"), indent=1)
