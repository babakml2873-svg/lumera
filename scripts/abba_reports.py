"""Write Output/Reports/*.csv for the ABBA Lighting brand from work/abba/results.json + plan_final.json,
validating every output file (800x800, JPEG, <=100 KB, filename convention)."""
import csv, json, re
from collections import Counter, defaultdict
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
W = ROOT / "work" / "abba"; OUT = ROOT / "Output"; REP = OUT / "Reports"; REP.mkdir(parents=True, exist_ok=True)
BRAND = "ABBA Lighting"; BDIR = "ABBA_Lighting"
res = json.load(open(W / "results.json")); plan = json.load(open(W / "plan_final.json"))
SEARCH = ("abbalightingusa.com catalog (WooCommerce Store API: product SKU, product name, 467 variation SKUs/attributes); "
          "ABBA resellers sonicelectric.com, readyelectricsupply.com, kingsoutdoorlighting.com, lbclightingpro.com; web search")

# ---- validation of every written file
problems = []
for r in res:
    if not r["file"]:
        continue
    p = OUT / r["list"] / BDIR / r["file"]
    with Image.open(p) as im:
        ok = im.size == (800, 800) and im.format == "JPEG"
    size = p.stat().st_size
    pat = rf"^{re.escape(r['nsku'])}-(V|G-\d\d)\.jpg$"
    if not ok or size > 100_000 or not re.match(pat, r["file"]):
        problems.append((str(p), ok, size))
    r["bytes"] = size
assert "lumera" not in json.dumps(res).lower()
print("validation problems:", problems)

def conf_of(rec):
    return rec["conf"] or "None"

# ---- image_report.csv
rows = []
by_row = defaultdict(list)
for r in res:
    by_row[(r["list"], r["sku"])].append(r)
for rec in plan:
    lst = "List_" + rec["list"].replace("List", "")
    imgs = by_row.get((lst, rec["sku"]), [])
    for r in imgs:
        i = r["info"]
        status = i["status"]
        if status == "OK" and rec["conf"] == "Medium":
            status = "OK-REVIEW-RECOMMENDED"
        notes = [rec["note"]] if r["type"] == "V" else [f"Gallery image of {rec['product']}"]
        notes += i.get("notes", [])
        if i.get("why"): notes.append(i["why"])
        rows.append(dict(List=lst, Brand=BRAND, SKU=rec["sku"], Image_Type=r["type"], Filename=r["file"],
                         Source_URL=r["url"], Match_Confidence=conf_of(rec), Status=status, Notes=" | ".join(n for n in notes if n),
                         Source_Page=r["page"], Source_Site=r["origin"],
                         Source_Pixels="x".join(map(str, i.get("src_px", []))), Output_Bytes=r.get("bytes", ""),
                         JPEG_Quality=i.get("q", ""), Product=rec["product"]))
    if not any(r["type"] == "V" and r["file"] for r in imgs):
        why = rec.get("review") or rec.get("v_withheld") or next((r["info"].get("why") for r in imgs if r["type"] == "V"), "") or "no verified variant image"
        rows.append(dict(List=lst, Brand=BRAND, SKU=rec["sku"], Image_Type="V", Filename="", Source_URL="",
                         Match_Confidence=conf_of(rec), Status="MISSING-REVIEW", Notes=why, Source_Page=rec.get("page", ""),
                         Source_Site="", Source_Pixels="", Output_Bytes="", JPEG_Quality="", Product=rec["product"]))
F = ["List", "Brand", "SKU", "Image_Type", "Filename", "Source_URL", "Match_Confidence", "Status", "Notes",
     "Source_Page", "Source_Site", "Source_Pixels", "Output_Bytes", "JPEG_Quality", "Product"]
with open(REP / "image_report.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, F); w.writeheader(); w.writerows(rows)

# ---- missing_images.csv
miss = []
for rec in plan:
    lst = "List_" + rec["list"].replace("List", "")
    imgs = by_row.get((lst, rec["sku"]), [])
    hasV = any(r["type"] == "V" and r["file"] for r in imgs)
    nG = sum(1 for r in imgs if r["type"] == "G" and r["file"])
    if not hasV:
        why = rec.get("review") or rec.get("v_withheld") or next((r["info"].get("why") for r in imgs if r["type"] == "V"), "")
        miss.append(dict(List=lst, Brand=BRAND, SKU=rec["sku"], Missing_Image_Type="V", Search_Attempts=SEARCH,
                         Reason=why, Status="NEEDS_MANUAL_REVIEW"))
    if nG == 0:
        why = rec.get("review") or ("no official gallery images beyond the variant image" if rec["resolution"] else "product not matched")
        miss.append(dict(List=lst, Brand=BRAND, SKU=rec["sku"], Missing_Image_Type="G", Search_Attempts=SEARCH,
                         Reason=why, Status="NEEDS_MANUAL_REVIEW" if not rec["resolution"] else "NO_SOURCE_AVAILABLE"))
with open(REP / "missing_images.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["List", "Brand", "SKU", "Missing_Image_Type", "Search_Attempts", "Reason", "Status"])
    w.writeheader(); w.writerows(miss)

# ---- sku_filename_mapping.csv
with open(REP / "sku_filename_mapping.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["Original_SKU", "Normalized_SKU", "Output_Filename", "Brand", "List"])
    w.writeheader()
    for r in res:
        if r["file"]:
            w.writerow(dict(Original_SKU=r["sku"], Normalized_SKU=r["nsku"], Output_Filename=f"{r['list']}/{BDIR}/{r['file']}",
                            Brand=BRAND, List=r["list"]))

# ---- brand_progress.csv
total = len(plan)
v_ok = {(r["list"], r["sku"]) for r in res if r["type"] == "V" and r["file"]}
g_cnt = sum(1 for r in res if r["type"] == "G" and r["file"])
processed = {(r["list"], r["sku"]) for r in res if r["file"]}
failed = sum(1 for rec in plan if ("List_" + rec["list"].replace("List", ""), rec["sku"]) not in processed)
prog = dict(Brand=BRAND, Total_Products=total, Processed_Products=len(processed), Variant_Images=len(v_ok),
            Gallery_Images=g_cnt, Missing_Images=total - len(v_ok), Failed_Products=failed,
            Completion_Percentage=f"{100 * len(v_ok) / total:.1f}")
with open(REP / "brand_progress.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(prog)); w.writeheader(); w.writerow(prog)
print(prog)
print("missing rows", Counter(m["Missing_Image_Type"] for m in miss))
json.dump(prog, open(W / "progress.json", "w"))
