"""Flag variant images that the source re-uses for *different* products (series/family photos).

A V image whose pHash equals the V image of another SKU taken from a different source page is not
proof of that exact SKU (e.g. one breaker photo for 15-100 A ratings), so it is downgraded to Medium
(OK-REVIEW-RECOMMENDED) with a note naming the other SKUs.  When exactly one SKU of the group has the photo under its own
file name it is kept as that SKU's photo; when it names a different SKU (e.g. the blue variant's photo on the green SKU) the V is withheld.  Same-page sharing (variants that differ only
in non-visual options) is left alone.

Enabled per brand with config.json {"shared_v_check": true}.
usage: python3 shared_v.py "<Brand>" [--apply]   (run_brand.py calls flag_shared() itself)
"""
import json, sys
from collections import defaultdict

import imagehash
from PIL import Image, ImageStat

from common import OUT, WORK, brand_dir, match_key, slug

NOTE = "source uses this same photo for other products"


def flag_shared(plan, results, bdir, max_dist=2, delete=True):
    v = [r for r in results if r["type"] == "V" and r["file"]]
    sig = {}
    for r in v:  # pHash is colour-blind, so the mean colour must match too (blue vs green variant photos)
        with Image.open(OUT / r["list"] / bdir / r["file"]) as im:
            sig[id(r)] = (imagehash.phash(im), ImageStat.Stat(im.convert("RGB").resize((64, 64))).mean)
    groups = defaultdict(list)
    for r in v:  # bucket by exact hash + coarse colour, then merge near-identical buckets
        h, m = sig[id(r)]
        groups[(str(h), tuple(round(c / 16) for c in m))].append(r)
    keys = list(groups)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if groups[a] and groups[b]:
                (ha, ma), (hb, mb) = sig[id(groups[a][0])], sig[id(groups[b][0])]
                if ha - hb <= max_dist and max(abs(x - y) for x, y in zip(ma, mb)) <= 12:
                    groups[a] += groups[b]; groups[b] = []
    pl = {("List_" + p["list"].replace("List", ""), p["sku"]): p for p in plan}
    n = 0
    fk = lambda r: match_key(r["url"].split("?")[0].split("/")[-1].rsplit(".", 1)[0])
    for g in groups.values():
        if len({r["page"].split("?")[0] for r in g}) < 2:
            continue
        # the file named after its own SKU is that SKU's photo - unless the source copied the photo under several
        # SKU-named files (then nobody's ownership is proven)
        self_named = {r["sku"] for r in g if match_key(r["sku"]) in fk(r)}
        owner = next(iter(self_named)) if len(self_named) == 1 else None
        for r in g:
            if r["sku"] == owner:
                continue
            others = sorted({x["sku"] for x in g if x["page"].split("?")[0] != r["page"].split("?")[0]})
            rec = pl[(r["list"], r["sku"])]
            if NOTE in rec["note"] or rec.get("v_withheld"):
                continue
            named = [o for o in others if len(match_key(o)) >= 4 and match_key(o) in fk(r)]
            if r["sku"] not in self_named and named:  # explicitly another variant's photo -> never substitute
                why = f"source photo is of {named[0]} (re-used by the source for this SKU) - not used"
                if delete:
                    (OUT / r["list"] / bdir / r["file"]).unlink(missing_ok=True)
                r["file"] = ""; r["info"] = dict(r["info"], status="WITHHELD", why=why)
                rec["v_withheld"] = why
            else:
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
    n = flag_shared(plan, res, brand_dir(b), delete="--apply" in sys.argv)
    print(b, "flagged", n, "of", sum(1 for r in res if r["type"] == "V" and r["file"]))
    if "--apply" in sys.argv:
        json.dump(plan, open(W / "plan_final.json", "w"), indent=1)
        json.dump(res, open(W / "results.json", "w"), indent=1)
