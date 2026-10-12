"""Write Output/README.md: one overview of all finished brands from Output/Reports/brand_progress.csv.

usage: python3 make_overview.py
"""
import csv, re
from collections import Counter

from common import OUT, WORK, brand_dir, slug

BR = "claude/product-image-crawling-git-h0756k"
RAW = f"https://github.com/babakml2873-svg/lumera/raw/{BR}/Output/Archives/"
P = list(csv.DictReader(open(OUT / "Reports" / "brand_progress.csv")))
img = list(csv.DictReader(open(OUT / "Reports" / "image_report.csv")))
st = Counter(r["Status"] for r in img if r["Image_Type"] == "V")
t = sum(int(p["Total_Products"]) for p in P); v = sum(int(p["Variant_Images"]) for p in P)
g = sum(int(p["Gallery_Images"]) for p in P)


def wdir(b):
    return WORK / ("abba" if b == "ABBA Lighting" else slug(b))


FIXED = {"Lutron": "reseller: LightingSupply.com, Buy Rite Electric", "Panasonic": "reseller: Buy Rite Electric",
         "Westgate": "reseller: Sonic Electric, LightingSupply.com"}  # sources.txt wording the regex can't parse


def source(b):
    if b in FIXED:
        return FIXED[b]
    s = (wdir(b) / "sources.txt").read_text() if (wdir(b) / "sources.txt").exists() else "abbalightingusa.com (official)"
    off = re.match(r"\s*([\w.-]+\.\w+)[^.]*?\(official", s)
    used = re.search(r"Used ([^.;(]+?)\s*\(", s)
    if used and re.search(r"blocked|403|429|no per-|only|fails|small", s[:used.start()]):
        return "reseller: " + re.sub(r"\s+whose.*|:.*", "", used.group(1).strip())[:40]
    return f"official: {off.group(1)}" if off else s.split(" ")[0]


def reason(b):
    r = (wdir(b) / "README.md").read_text()
    m = re.findall(r"^\| (.+?) \| (\d+) \|$", r.split("reasons", 1)[1], re.M) if "reasons" in r else []
    return m[0][0] if m else ""


zipname = lambda b: ("FIRST_BRAND_" if b == "ABBA Lighting" else "BRAND_") + brand_dir(b) + "_Images.zip"
L = ["# Product images — all brands", "",
     f"**{len(P)} brands, {t:,} list SKUs.** Variant images (`SKU-V.jpg`) were delivered for **{v:,} SKUs ({100 * v / t:.1f}%)**, "
     f"plus **{g:,} gallery images** (`SKU-G-NN.jpg`).", "",
     f"* Variant image status: {st['OK']:,} `OK` (exact SKU, High confidence), {st['OK-REVIEW-RECOMMENDED']:,} `OK-REVIEW-RECOMMENDED` "
     f"(Medium: alias/suffix match, family/series photo or upscaled source), {st['MISSING-REVIEW']:,} SKUs without a variant image "
     "(`missing_images.csv` gives the reason for each).",
     "* Every file is 800×800 px JPEG, ≤ 100,000 bytes, padded with its own border colour (no background removal); checked by script.",
     "* **No Lumera Electric site, CDN or mirrored asset was used as an image source** (every URL asserted). "
     "The brand named *Lumera Electric* in the lists was sourced from the official Kuzco Group store.",
     "* Images are third-party manufacturer/retailer photos and remain their owners' copyright.", "",
     "## Reports (all brands)", "",
     "`Reports/image_report.csv`, `missing_images.csv`, `sku_filename_mapping.csv`, `brand_progress.csv`, `review_queue.csv` "
     "(Medium-confidence and missing variant images, for manual review). Each brand ZIP holds its own subset and a README.", "",
     "## Brands", "",
     "| Brand | SKUs | Variant images | % | Gallery | Main image source | ZIP |", "|---|---|---|---|---|---|---|"]
for p in P:
    b = p["Brand"]
    L.append(f"| {b} | {int(p['Total_Products']):,} | {int(p['Variant_Images']):,} | {p['Completion_Percentage']} | "
             f"{int(p['Gallery_Images']):,} | {source(b)} | [{zipname(b)}]({RAW}{zipname(b)}) |")
L += ["", "## Lower coverage (< 75% variant images) — main reason", "", "| Brand | % | Main reason (count in brand README) |", "|---|---|---|"]
for p in sorted(P, key=lambda p: float(p["Completion_Percentage"])):
    if float(p["Completion_Percentage"]) < 75:
        L.append(f"| {p['Brand']} | {p['Completion_Percentage']} | {reason(p['Brand'])} |")
L += ["", "Each brand's `README.md` (inside its ZIP, and `work/<brand>/README.md`) lists sources searched, matching rules and all "
      "missing-image reasons. `README_ABBA_first_brand.md` is the detailed write-up of the first brand.", "",
      "## Pipeline", "", "`scripts/brands/*` harvest each source into `work/<brand>/catalog*.json`; `scripts/pipeline/run_brand.py` matches, "
      "downloads and processes; `shared_v.py` checks re-used series photos; `reports.py` validates and builds reports and ZIPs; "
      "`finish_brand.sh` commits each brand."]
(OUT / "README.md").write_text("\n".join(L) + "\n")
print("\n".join(L[:8]))
