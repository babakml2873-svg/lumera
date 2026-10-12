"""Rebuild Output/Reports/*.csv for every processed brand (work/<slug>/plan_final.json + results.json),
validate every output file, and optionally build one brand's ZIP.

usage: python3 reports.py [--zip "<Brand>"]
"""
import csv, json, re, subprocess, sys, zipfile
from collections import defaultdict
from pathlib import Path

from PIL import Image

from common import OUT, WORK, brand_dir, slug

REP = OUT / "Reports"; REP.mkdir(parents=True, exist_ok=True)
order = [b["brand"] for b in json.load(open(WORK / "_all" / "brands.json"))]
DIRS = {"ABBA Lighting": WORK / "abba"}
F_IMG = ["List", "Brand", "SKU", "Image_Type", "Filename", "Source_URL", "Match_Confidence", "Status", "Notes",
         "Source_Page", "Source_Site", "Source_Pixels", "Output_Bytes", "JPEG_Quality", "Product"]


def wdir(b):
    return DIRS.get(b, WORK / slug(b))


def search_attempts(b):
    p = wdir(b) / "sources.txt"
    if p.exists():
        return p.read_text().strip()
    return ("abbalightingusa.com catalog (WooCommerce Store API: product SKU, product name, 467 variation SKUs/attributes); "
            "ABBA resellers sonicelectric.com, readyelectricsupply.com, kingsoutdoorlighting.com, lbclightingpro.com; web search")


img_rows, miss_rows, map_rows, prog_rows, problems = [], [], [], [], []
per_brand_rows = defaultdict(lambda: defaultdict(list))
for b in order:
    W = wdir(b)
    zipb = sys.argv[sys.argv.index("--zip") + 1] if "--zip" in sys.argv else None
    if not (W / "results.json").exists() or not ((W / "DONE").exists() or b == zipb):
        continue
    plan = json.load(open(W / "plan_final.json")); res = json.load(open(W / "results.json"))
    bd = brand_dir(b)
    by = defaultdict(list)
    for r in res:
        by[(r["list"], r["sku"])].append(r)
        if r["file"]:
            p = OUT / r["list"] / bd / r["file"]
            with Image.open(p) as im:
                ok = im.size == (800, 800) and im.format == "JPEG"
            r["bytes"] = p.stat().st_size
            if not ok or r["bytes"] > 100_000 or not re.match(rf"^{re.escape(r['nsku'])}-(V|G-\d\d)\.jpg$", r["file"]):
                problems.append(str(p))
            if "lumera" in (r["url"] + r["page"]).lower():
                problems.append("LUMERA SOURCE " + r["url"])
    v_ok = g_cnt = 0; any_img = 0
    for rec in plan:
        lst = "List_" + rec["list"].replace("List", "")
        imgs = by.get((lst, rec["sku"]), [])
        conf = rec.get("conf") or "None"
        hasV = False
        for r in imgs:
            i = r["info"]; st = i["status"]
            if st == "OK" and conf == "Medium":
                st = "OK-REVIEW-RECOMMENDED"
            if st == "OK" and conf == "Low":
                st = "REVIEW-FAMILY-IMAGE"
            notes = ([rec.get("note", "")] if r["type"] == "V" else [f"Gallery image of {rec.get('product', '')}"]) + i.get("notes", [])
            if i.get("why"):
                notes.append(i["why"])
            row = dict(List=lst, Brand=b, SKU=rec["sku"], Image_Type=r["type"], Filename=r["file"], Source_URL=r["url"],
                       Match_Confidence=conf, Status=st, Notes=" | ".join(n for n in notes if n), Source_Page=r["page"],
                       Source_Site=r["origin"], Source_Pixels="x".join(map(str, i.get("src_px", []))),
                       Output_Bytes=r.get("bytes", ""), JPEG_Quality=i.get("q", ""), Product=rec.get("product", ""))
            img_rows.append(row); per_brand_rows[b]["img"].append(row)
            if r["file"]:
                m = dict(Original_SKU=rec["sku"], Normalized_SKU=r["nsku"], Output_Filename=f"{lst}/{bd}/{r['file']}", Brand=b, List=lst)
                map_rows.append(m); per_brand_rows[b]["map"].append(m)
                if r["type"] == "V":
                    hasV = True
                else:
                    g_cnt += 1
        if hasV:
            v_ok += 1
        if any(r["file"] for r in imgs):
            any_img += 1
        why = rec.get("review") or rec.get("v_withheld") or next((r["info"].get("why") for r in imgs if r["type"] == "V" and not r["file"]), "") or "no verified variant image"
        if not hasV:
            row = dict(List=lst, Brand=b, SKU=rec["sku"], Image_Type="V", Filename="", Source_URL="", Match_Confidence=conf,
                       Status="MISSING-REVIEW", Notes=why, Source_Page=rec.get("page", ""), Source_Site="", Source_Pixels="",
                       Output_Bytes="", JPEG_Quality="", Product=rec.get("product", ""))
            img_rows.append(row); per_brand_rows[b]["img"].append(row)
            m = dict(List=lst, Brand=b, SKU=rec["sku"], Missing_Image_Type="V", Search_Attempts=search_attempts(b), Reason=why,
                     Status="NEEDS_MANUAL_REVIEW")
            miss_rows.append(m); per_brand_rows[b]["miss"].append(m)
        if not any(r["type"] == "G" and r["file"] for r in imgs):
            reason = rec.get("review") or ("no further usable images for this exact variant in the source" if rec.get("resolution") else "product not matched")
            m = dict(List=lst, Brand=b, SKU=rec["sku"], Missing_Image_Type="G", Search_Attempts=search_attempts(b), Reason=reason,
                     Status="NEEDS_MANUAL_REVIEW" if not rec.get("resolution") else "NO_SOURCE_AVAILABLE")
            miss_rows.append(m); per_brand_rows[b]["miss"].append(m)
    total = len(plan)
    prog = dict(Brand=b, Total_Products=total, Processed_Products=any_img, Variant_Images=v_ok, Gallery_Images=g_cnt,
                Missing_Images=total - v_ok, Failed_Products=total - any_img,
                Completion_Percentage=f"{100 * v_ok / total:.1f}" if total else "0.0")
    prog_rows.append(prog); per_brand_rows[b]["prog"].append(prog)


def write(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields); w.writeheader(); w.writerows(rows)


write(REP / "image_report.csv", F_IMG, img_rows)
write(REP / "missing_images.csv", ["List", "Brand", "SKU", "Missing_Image_Type", "Search_Attempts", "Reason", "Status"], miss_rows)
write(REP / "sku_filename_mapping.csv", ["Original_SKU", "Normalized_SKU", "Output_Filename", "Brand", "List"], map_rows)
write(REP / "brand_progress.csv", ["Brand", "Total_Products", "Processed_Products", "Variant_Images", "Gallery_Images",
                                   "Missing_Images", "Failed_Products", "Completion_Percentage"], prog_rows)
rq = [dict(Brand=r["Brand"], List=r["List"], SKU=r["SKU"], Status=r["Status"], Match_Confidence=r["Match_Confidence"],
           Filename=r["Filename"], Reason=r["Notes"], Source_Page=r["Source_Page"])
      for r in img_rows if r["Image_Type"] == "V" and r["Status"] in ("OK-REVIEW-RECOMMENDED", "MISSING-REVIEW")]
write(REP / "review_queue.csv", ["Brand", "List", "SKU", "Status", "Match_Confidence", "Filename", "Reason", "Source_Page"], rq)
print("validation problems:", problems[:10], len(problems))
for p in prog_rows:
    print(p)

# ---------------------------------------------------------------- per-brand ZIP
if "--zip" in sys.argv:
    b = sys.argv[sys.argv.index("--zip") + 1]
    assert not problems
    bd = brand_dir(b); W = wdir(b)
    stage = W / "zip_reports"; stage.mkdir(exist_ok=True)
    pr = per_brand_rows[b]
    write(stage / "image_report.csv", F_IMG, pr["img"])
    write(stage / "missing_images.csv", ["List", "Brand", "SKU", "Missing_Image_Type", "Search_Attempts", "Reason", "Status"], pr["miss"])
    write(stage / "sku_filename_mapping.csv", ["Original_SKU", "Normalized_SKU", "Output_Filename", "Brand", "List"], pr["map"])
    write(stage / "brand_progress.csv", list(pr["prog"][0]), pr["prog"])
    write(stage / "review_queue.csv", ["Brand", "List", "SKU", "Status", "Match_Confidence", "Filename", "Reason", "Source_Page"],
          [x for x in rq if x["Brand"] == b])
    z = OUT / "Archives" / f"BRAND_{bd}_Images.zip"; z.parent.mkdir(exist_ok=True)
    if z.exists():
        z.unlink()
    with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:
        zf.write(W / "README.md", "README.md")
        for f in sorted(stage.glob("*.csv")):
            zf.write(f, f"Reports/{f.name}")
        for lst in ("List_1", "List_2", "List_3", "List_4"):
            d = OUT / lst / bd
            files = sorted(d.glob("*")) if d.exists() else []
            if not files:
                zf.writestr(f"{lst}/{bd}/_NO_{bd}_PRODUCTS_IN_THIS_LIST.txt", f"{lst} contains no {b} SKUs with images.\n")
            for f in files:
                zf.write(f, f"{lst}/{bd}/{f.name}")
    with zipfile.ZipFile(z) as zf:
        assert zf.testzip() is None
        n = len(zf.namelist())
    print("ZIP", z, z.stat().st_size, "entries", n)
